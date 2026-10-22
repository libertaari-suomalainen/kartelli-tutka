from pathlib import Path
import tempfile
import unittest
import zipfile

from kartelli_tutka.build_all import build_and_verify_all
from kartelli_tutka.engine import (
    BASELINE_HILMA_TENDERS,
    BASELINE_INHOUSE_FLOWS,
    PUBLIC_BUYER_DIRECTORY,
    HilmaTenderRecord,
    PeerCategorySpend,
    compute_category_arbitrage_breakdown,
    compute_inhouse_leakage,
    compute_price_spread_arbitrage,
    detect_single_bid_cartels,
    validate_ytunnus_checksum,
)
from kartelli_tutka.legal_generator import (
    generate_hankintaoikaisu,
    generate_hilma_spec_challenge,
    generate_julkisuuslaki_foia,
    generate_kkv_complaint,
)


class TestKartelliTutkaEngine(unittest.TestCase):
    def test_all_ytunnus_checksums_valid(self) -> None:
        self.assertEqual(len(BASELINE_INHOUSE_FLOWS), 15)
        self.assertEqual(len(PUBLIC_BUYER_DIRECTORY), 43)
        for f in BASELINE_INHOUSE_FLOWS:
            self.assertTrue(
                validate_ytunnus_checksum(f.inhouse_y_tunnus),
                f"Invalid Modulo-11 Y-tunnus on in-house flow {f.inhouse_vendor}: {f.inhouse_y_tunnus}",
            )
        for b in PUBLIC_BUYER_DIRECTORY:
            self.assertTrue(
                validate_ytunnus_checksum(b.y_tunnus),
                f"Invalid Modulo-11 Y-tunnus on public buyer {b.entity_name}: {b.y_tunnus}",
            )

    def test_inhouse_sidosyksikko_leakage(self) -> None:
        res = compute_inhouse_leakage()
        self.assertAlmostEqual(res["total_inhouse_spend_m_eur"], 1963.40, places=2)
        self.assertGreater(res["illegal_token_share_spend_m_eur"], 1200.0)
        self.assertAlmostEqual(res["illegal_under_10pct_spend_m_eur"], 1254.70, places=2)
        self.assertAlmostEqual(res["recoverable_annual_saving_m_eur"], 230.99, places=2)

    def test_price_spread_arbitrage(self) -> None:
        sample = [
            PeerCategorySpend("Pirha", "85121000-LocumMD", "hour", 100000, 115.0),
            PeerCategorySpend("Pohde", "85121000-LocumMD", "hour", 100000, 125.0),
            PeerCategorySpend("Lapha", "85121000-LocumMD", "hour", 100000, 210.0),
            PeerCategorySpend("Vake",  "85121000-LocumMD", "hour", 100000, 185.0),
        ]
        res = compute_price_spread_arbitrage(sample)
        self.assertEqual(res["baseline_category_spend_eur"], 63500000.0)
        self.assertGreater(res["p25_arbitrage_saving_eur"], 14000000.0)

        breakdown = compute_category_arbitrage_breakdown()
        self.assertGreaterEqual(len(breakdown), 30)

    def test_single_bid_cartel_detector(self) -> None:
        tenders = [
            HilmaTenderRecord("MAO:500/2024", "Varsinais-Suomen HVA", "79940000-Collections", 1900000.0, 0, True, 18),
            HilmaTenderRecord("HILMA-OPEN", "Tampere", "45233120-Infra", 5000000.0, 6, False, 25),
        ]
        flagged = detect_single_bid_cartels(tenders)
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged[0]["tender_id"], "MAO:500/2024")
        self.assertEqual(flagged[0]["expected_annual_saving_eur"], 475000.0)

    def test_zero_fee_legal_generators(self) -> None:
        istekki_flow = BASELINE_INHOUSE_FLOWS[1]
        kkv = generate_kkv_complaint(istekki_flow)
        self.assertEqual(kkv["recipient_email"], "kirjaamo@kkv.fi")
        self.assertEqual(kkv["filing_fee_eur"], "0.00")
        self.assertIn("MAO:154/2024", kkv["body"])
        self.assertIn("KHO 8.10.2025 taltio 2250", kkv["body"])
        self.assertIn("2292633-0", kkv["body"])

        # Verify >=10% monopoly flows (Apotti & Valtori) challenge subcontracting chain / lock-in instead of <10% ownership
        valtori_flow = BASELINE_INHOUSE_FLOWS[6]
        kkv_valtori = generate_kkv_complaint(valtori_flow)
        self.assertIn("1226/2013", kkv_valtori["body"])
        self.assertNotIn("ainoastaan 100.00 %", kkv_valtori["body"])

        oikaisu = generate_hankintaoikaisu(istekki_flow, istekki_flow.buyer_kirjaamo_email)
        self.assertIn("133 §", oikaisu["subject"])
        self.assertNotIn("RL 40:9", oikaisu["body"])

        foia = generate_julkisuuslaki_foia("Tampereen kaupunki", "kirjaamo@tampere.fi")
        self.assertIn("14 vuorokauden", foia["body"])
        self.assertIn("ostolaskudata", foia["body"])
        self.assertNotIn("kaupunkin", foia["body"])

        hilma = generate_hilma_spec_challenge(BASELINE_HILMA_TENDERS[0])
        self.assertIn("67 §", hilma["subject"])
        self.assertIn("75 §", hilma["body"])

    def test_atomic_build_all_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary = build_and_verify_all(root, enrich_live_prh=False)
            self.assertTrue((root / summary["snapshot_path"]).exists())
            self.assertTrue((root / summary["xlsx_path"]).exists())
            self.assertTrue((root / summary["html_path"]).exists())
            html_text = (root / summary["html_path"]).read_text(encoding="utf-8")
            self.assertIn("230,99 milj. €/v", html_text)
            self.assertIn("594,40 milj. €/v", html_text)
            self.assertIn("MAO:611/2025", html_text)
            self.assertNotIn("MAO:412/2023", html_text)
            with zipfile.ZipFile(root / summary["xlsx_path"], "r") as zf:
                sheet2 = zf.read("xl/worksheets/sheet2.xml").decode("utf-8")
                sheet5 = zf.read("xl/worksheets/sheet5.xml").decode("utf-8")
                self.assertIn("Istekki Oy", sheet2)
                self.assertIn("<f>ROUND(", sheet2)
                self.assertIn("KAIKKI 43 SUURINTA JULKISTA OSTAJAA", sheet5)


if __name__ == "__main__":
    unittest.main()
