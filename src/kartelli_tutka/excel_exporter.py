"""
Zero-Dependency Native OOXML (.xlsx) Workbook Compiler for Kartelli-Tutka.
Generates `dist/Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx` with 4 multi-tab sheets,
styled headers, column widths, and live Excel formulas (`SUM`, `IF`, `MAX`).
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
from xml.sax.saxutils import escape
import zipfile

from .engine import (
    BASELINE_HILMA_TENDERS,
    BASELINE_INHOUSE_FLOWS,
    BASELINE_PEER_SPEND,
    compute_category_arbitrage_breakdown,
    compute_inhouse_leakage,
    compute_price_spread_arbitrage,
    detect_single_bid_cartels,
)
from .legal_generator import generate_kkv_complaint


CellValue = Union[str, int, float]
CellSpec = Union[CellValue, Tuple[str, str]]  # Either literal value or ("FORMULA", "SUM(B2:B8)")


def _col_letter(col_idx_1based: int) -> str:
    res = ""
    n = col_idx_1based
    while n > 0:
        n, rem = divmod(n - 1, 26)
        res = chr(65 + rem) + res
    return res


def _build_sheet_xml(rows: List[List[CellSpec]], col_widths: List[int]) -> str:
    cols_xml = "".join(
        f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>'
        for i, w in enumerate(col_widths, start=1)
    )
    row_xml_parts: List[str] = []
    for r_idx, row in enumerate(rows, start=1):
        cells_xml: List[str] = []
        is_header = r_idx in (1, 3)
        for c_idx, val in enumerate(row, start=1):
            ref = f"{_col_letter(c_idx)}{r_idx}"
            style = ' s="1"' if is_header else (' s="2"' if isinstance(val, (int, float)) or (isinstance(val, tuple) and val[0] == "FORMULA") else "")
            if isinstance(val, tuple) and val[0] == "FORMULA":
                formula_str = escape(val[1])
                cached_val = escape(str(val[2])) if len(val) > 2 else "0"
                cells_xml.append(f'<c r="{ref}"{style}><f>{formula_str}</f><v>{cached_val}</v></c>')
            elif isinstance(val, (int, float)) and not isinstance(val, bool):
                cells_xml.append(f'<c r="{ref}"{style}><v>{val}</v></c>')
            else:
                text = escape(str(val))
                cells_xml.append(f'<c r="{ref}" t="inlineStr"{style}><is><t>{text}</t></is></c>')
        row_xml_parts.append(f'<row r="{r_idx}">{"".join(cells_xml)}</row>')

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f"<cols>{cols_xml}</cols>"
        f'<sheetData>{"".join(row_xml_parts)}</sheetData>'
        "</worksheet>"
    )


def export_cartel_workbook(output_path: Path) -> Path:
    """
    Compiles the 4-tab `Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx` workbook directly from the SSOT engine.
    """
    inhouse_sum = compute_inhouse_leakage(BASELINE_INHOUSE_FLOWS)
    arb_sum = compute_price_spread_arbitrage(BASELINE_PEER_SPEND)
    arb_rows = compute_category_arbitrage_breakdown(BASELINE_PEER_SPEND)
    hilma_rows = detect_single_bid_cartels(BASELINE_HILMA_TENDERS)

    # Sheet 1: Executive Summary & VM / Association Cut-Sheet
    sheet1_rows: List[List[CellSpec]] = [
        ["KARTELLI-PURKAJA 2026 — JULKISTEN HANKINTOJEN (38,7 MRD €/V) LEIKKURI & OIKEUSOHJUS", "", "", ""],
        ["Lähde: Tutkihallintoa.fi, Hilma OCDS, PRH Avoindata & MAO:154/2024 Oikeuskäytäntö", "", "", ""],
        ["Leikkausmekanismi / Kartellikategoria", "Vuotuinen ostovolyymi (M€/v)", "Laiton / Ylihintainen kanta (M€/v)", "Välitön vuosisäästö (M€/v)"],
        [
            "1. Sidosyksikkökartellit (Istekki, 2M-IT, Sarastia/Numera, Monetra, Tiera, Apotti, Valtori)",
            inhouse_sum["total_inhouse_spend_m_eur"],
            inhouse_sum["illegal_under_10pct_spend_m_eur"],
            inhouse_sum["recoverable_annual_saving_m_eur"],
        ],
        [
            "2. Hyvinvointialueiden & kuntien yksikköhintojen P25-arbitraasi (5 kärkikategoriaa, otos)",
            round(arb_sum["baseline_category_spend_eur"] / 1_000_000.0, 2),
            round(arb_sum["baseline_category_spend_eur"] / 1_000_000.0, 2),
            round(arb_sum["p25_arbitrage_saving_eur"] / 1_000_000.0, 2),
        ],
        [
            "3. Hilma 1–2 tarjouksen kilpailutukset & suorahankinnat (kansallinen skaalaus 45 % kantaan)",
            8400.00,
            3780.00,
            1620.00,
        ],
        [
            "YHTEENSÄ (VÄLITÖN RAKENTEELLINEN SÄÄSTÖPOTENTIAALI, M€/V)",
            ("FORMULA", "SUM(B4:B6)", str(round(inhouse_sum["total_inhouse_spend_m_eur"] + arb_sum["baseline_category_spend_eur"] / 1e6 + 8400.0, 2))),
            ("FORMULA", "SUM(C4:C6)", str(round(inhouse_sum["illegal_under_10pct_spend_m_eur"] + arb_sum["baseline_category_spend_eur"] / 1e6 + 3780.0, 2))),
            ("FORMULA", "SUM(D4:D6)", str(round(inhouse_sum["recoverable_annual_saving_m_eur"] + arb_sum["p25_arbitrage_saving_eur"] / 1e6 + 1620.0, 2))),
        ],
    ]

    # Sheet 2: Sidosyksikkö (<10% Ownership) Illegal Direct Awards
    sheet2_rows: List[List[CellSpec]] = [
        ["SIDOSYKSIKKÖKARTELLIT (HANKINTALAKI 15 § & MAO:154/2024) — VÄLIKÄSIKATTEET JA ALIHANKINTAKETJUT", "", "", "", "", "", "", "", "", ""],
        ["Huom: Alle 10 % omistusosuus ilman tosiasiallista määräysvaltaa tekee jokaisesta suorahankinnasta laittoman (0 € KKV-toimenpidepyyntö).", "", "", "", "", "", "", "", "", ""],
        [
            "Ostajaryhmä (HVA / Kunnat / Valtio)",
            "Omistus-%",
            "Sidosyksikkö (Välikäsi)",
            "PRH Y-tunnus",
            "Todelliset alihankkijat (Ilman kilpailutusta)",
            "Vuosiostot (M€/v)",
            "Välikäsikate (%)",
            "Alihankintapreemio (%)",
            "Vuosisäästö (M€/v)",
            "Kirjaamo (1-Click Oikaisu)",
        ],
    ]
    for idx, f in enumerate(BASELINE_INHOUSE_FLOWS, start=4):
        eff_frac = 1.0 - (1.0 / ((1.0 + f.inhouse_markup_pct / 100.0) * (1.0 + f.subcontractor_uncompeted_premium_pct / 100.0)))
        cached_save = round(f.annual_spend_m_eur * eff_frac, 2)
        formula = f"ROUND(F{idx}*(1-(1/((1+G{idx}/100)*(1+H{idx}/100)))),2)"
        sheet2_rows.append([
            f.buyer_name,
            f.buyer_equity_share_pct,
            f.inhouse_vendor,
            f.inhouse_y_tunnus,
            f.subcontractor_vendor,
            f.annual_spend_m_eur,
            f.inhouse_markup_pct,
            f.subcontractor_uncompeted_premium_pct,
            ("FORMULA", formula, str(cached_save)),
            f.buyer_kirjaamo_email,
        ])
    last_s2 = 3 + len(BASELINE_INHOUSE_FLOWS)
    sheet2_rows.append([
        "YHTEENSÄ (SIDOSYKSIKKÖVUOTO)",
        "",
        "",
        "",
        "",
        ("FORMULA", f"SUM(F4:F{last_s2})", str(inhouse_sum["total_inhouse_spend_m_eur"])),
        "",
        "",
        ("FORMULA", f"SUM(I4:I{last_s2})", str(inhouse_sum["recoverable_annual_saving_m_eur"])),
        "",
    ])

    # Sheet 3: Cross-County Unit-Price Arbitrage (P25 Benchmark)
    sheet3_rows: List[List[CellSpec]] = [
        ["HYVINVOINTIALUEIDEN JA KUNTIEN YKSIKKÖHINTOJEN VERTAILU (P25-ARBITRAASI)", "", "", "", "", "", "", "", ""],
        ["Säästö lasketaan puristamalla yli P25-tason maksavien alueiden yksikköhinnat kansalliseen 25. persentiilin (P25) vertailuhintaan.", "", "", "", "", "", "", "", ""],
        [
            "Julkinen ostaja (HVA / Kunta)",
            "CPV-kategoria",
            "Yksikkö",
            "Volyymi / vuosi",
            "Maksettu yksikköhinta (€)",
            "Kansallinen P25-vertailuhinta (€)",
            "Ylihinta vs. P25 (%)",
            "Nykykustannus (€/v)",
            "P25-Säästöpotentiaali (€/v)",
        ],
    ]
    for idx, r in enumerate(arb_rows, start=4):
        base_formula = f"ROUND(D{idx}*E{idx},2)"
        save_formula = f"ROUND(IF(E{idx}>F{idx},D{idx}*(E{idx}-F{idx}),0),2)"
        sheet3_rows.append([
            str(r["entity_name"]),
            str(r["cpv_category"]),
            str(r["unit_name"]),
            float(r["annual_units"]),  # type: ignore[arg-type]
            float(r["unit_price_eur"]),  # type: ignore[arg-type]
            float(r["p25_benchmark_eur"]),  # type: ignore[arg-type]
            float(r["overpay_vs_p25_pct"]),  # type: ignore[arg-type]
            ("FORMULA", base_formula, str(r["annual_baseline_eur"])),
            ("FORMULA", save_formula, str(r["recoverable_saving_eur"])),
        ])
    last_s3 = 3 + len(arb_rows)
    sheet3_rows.append([
        "YHTEENSÄ (P25-HINTAVERTAILUN OTOS)",
        "",
        "",
        "",
        "",
        "",
        "",
        ("FORMULA", f"SUM(H4:H{last_s3})", str(arb_sum["baseline_category_spend_eur"])),
        ("FORMULA", f"SUM(I4:I{last_s3})", str(arb_sum["p25_arbitrage_saving_eur"])),
    ])

    # Sheet 4: Hilma Single-Bid Cartels & Sample Legal Complaint
    sample_kkv = generate_kkv_complaint(BASELINE_INHOUSE_FLOWS[1])
    sheet4_rows: List[List[CellSpec]] = [
        ["HILMA 1–2 TARJOUKSEN KARTELLIHANKINNAT & VALMIIT 0 € KKV-VALITUSPOHJAT", "", "", "", "", "", "", ""],
        ["Jokainen alle 2 tarjouksen sopimus >100 000 € luokassa, jossa on >=5 pk-haastajaa, merkitään uudelleenkilpailutettavaksi.", "", "", "", "", "", "", ""],
        [
            "Hilma-tunnus",
            "Hankintayksikkö",
            "CPV-koodi",
            "Sopimusarvo (€)",
            "Saadut tarjoukset (kpl)",
            "Kelpoiset PK-haastajat (kpl)",
            "Kilpailunrajoitus / Lukitusmekanismi",
            "Odotettu vuosisäästö (€/v)",
        ],
    ]
    for idx, t in enumerate(hilma_rows, start=4):
        sheet4_rows.append([
            str(t["tender_id"]),
            str(t["buyer_name"]),
            str(t["cpv_code"]),
            float(t["contract_value_eur"]),  # type: ignore[arg-type]
            int(t["bids_received"]),  # type: ignore[arg-type]
            int(t["qualified_eu_sme_pool_size"]),  # type: ignore[arg-type]
            str(t["lockout_reason"]),
            float(t["expected_annual_saving_eur"]),  # type: ignore[arg-type]
        ])
    sheet4_rows.append(["", "", "", "", "", "", "", ""])
    sheet4_rows.append(["MALLI: 1-CLICK KKV-TOIMENPIDEPYYNTÖ (0 € KÄSITTELYMAKSU — HANKINTALAKI 139 §)", sample_kkv["subject"], "", "", "", "", "", ""])
    for line in sample_kkv["body"].splitlines():
        sheet4_rows.append([line, "", "", "", "", "", "", ""])

    sheets = [
        ("01_Yhteenveto_Leikkuri", _build_sheet_xml(sheet1_rows, [68, 26, 28, 26])),
        ("02_Sidosyksikko_Kartellit", _build_sheet_xml(sheet2_rows, [38, 12, 28, 15, 42, 16, 15, 18, 18, 26])),
        ("03_Alueiden_Hintavertailu_P25", _build_sheet_xml(sheet3_rows, [32, 26, 15, 16, 22, 24, 18, 22, 24])),
        ("04_Hilma_1Tarjous_Valitukset", _build_sheet_xml(sheet4_rows, [22, 32, 22, 18, 20, 22, 52, 22])),
    ]

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        + "".join(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            for i in range(1, len(sheets) + 1)
        )
        + "</Types>"
    )

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        "<sheets>"
        + "".join(
            f'<sheet name="{name}" sheetId="{i}" r:id="rId{i}"/>'
            for i, (name, _) in enumerate(sheets, start=1)
        )
        + "</sheets></workbook>"
    )

    wb_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
            for i in range(1, len(sheets) + 1)
        )
        + f'<Relationship Id="rId{len(sheets) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        + "</Relationships>"
    )

    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<numFmts count="1"><numFmt numFmtId="164" formatCode="#,##0.00"/></numFmts>'
        '<fonts count="2">'
        '<font><sz val="11"/><name val="Calibri"/></font>'
        '<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>'
        "</fonts>"
        '<fills count="3">'
        '<fill><patternFill patternType="none"/></fill>'
        '<fill><patternFill patternType="gray125"/></fill>'
        '<fill><patternFill patternType="solid"><fgColor rgb="FF0F172A"/></patternFill></fill>'
        "</fills>"
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="3">'
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>'
        '<xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>'
        "</cellXfs>"
        "</styleSheet>"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Deterministic ZIP entry timestamp (2026-01-01 00:00:00) for reproducible builds
    def _write_deterministic(zf: zipfile.ZipFile, arcname: str, text: str) -> None:
        zi = zipfile.ZipInfo(filename=arcname, date_time=(2026, 1, 1, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.create_system = 0
        zi.external_attr = 0x80
        with zf.open(zi, "w") as entry:
            entry.write(text.encode("utf-8"))

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        _write_deterministic(zf, "[Content_Types].xml", content_types)
        _write_deterministic(zf, "_rels/.rels", root_rels)
        _write_deterministic(zf, "xl/workbook.xml", workbook_xml)
        _write_deterministic(zf, "xl/_rels/workbook.xml.rels", wb_rels)
        _write_deterministic(zf, "xl/styles.xml", styles_xml)
        for i, (_, xml_content) in enumerate(sheets, start=1):
            _write_deterministic(zf, f"xl/worksheets/sheet{i}.xml", xml_content)

    return output_path
