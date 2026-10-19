"""
Atomic Build & SSOT Verification Pipeline for Kartelli-Tutka.
Compiles from the Single Source of Truth (engine.py):
  1. data/finland_procurement_snapshot.json
  2. dist/Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx
  3. dist/index.html
  4. dist/kartelli_purkaja_static_drop.zip
"""

import json
from pathlib import Path
import zipfile

from .excel_exporter import export_cartel_workbook
from .ingest import write_ssot_snapshot
from .web_builder import build_static_web_app

# Superseded placeholder Y-tunnus IDs replaced by live PRH Open Data IDs
SUPERSEDED_Y_TUNNUS = [
    "2267617-6",
    "2181290-4",
    "2926350-9",
    "2446810-2",
    "2342126-4",
]


def build_and_verify_all(repo_root: Path, enrich_live_prh: bool = True) -> dict:
    snapshot_path = repo_root / "data" / "finland_procurement_snapshot.json"
    xlsx_path = repo_root / "dist" / "Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx"
    html_path = repo_root / "dist" / "index.html"
    bundle_zip_path = repo_root / "dist" / "kartelli_purkaja_static_drop.zip"

    ssot = write_ssot_snapshot(snapshot_path, enrich_live_prh=enrich_live_prh)
    export_cartel_workbook(xlsx_path)
    build_static_web_app(html_path)

    html_text = html_path.read_text(encoding="utf-8")
    json_text = snapshot_path.read_text(encoding="utf-8")
    for old_id in SUPERSEDED_Y_TUNNUS:
        if old_id in html_text or old_id in json_text:
            raise AssertionError(f"Superseded Y-tunnus '{old_id}' found in generated artifacts!")

    with zipfile.ZipFile(xlsx_path, "r") as zf:
        names = zf.namelist()
        assert "xl/workbook.xml" in names
        assert "xl/worksheets/sheet1.xml" in names
        assert "xl/worksheets/sheet4.xml" in names
        for info in zf.infolist():
            assert info.date_time == (2026, 1, 1, 0, 0, 0), "Non-deterministic ZIP timestamp in XLSX!"
            assert info.create_system == 0 and info.external_attr == 0x80, "Non-neutral OS marker in XLSX!"

    with zipfile.ZipFile(bundle_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as bzf:
        for fpath in (html_path, xlsx_path):
            zi = zipfile.ZipInfo(filename=fpath.name, date_time=(2026, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 0
            zi.external_attr = 0x80
            with bzf.open(zi, "w") as entry:
                entry.write(fpath.read_bytes())

    return {
        "snapshot_path": str(snapshot_path.relative_to(repo_root)),
        "xlsx_path": str(xlsx_path.relative_to(repo_root)),
        "html_path": str(html_path.relative_to(repo_root)),
        "bundle_zip_path": str(bundle_zip_path.relative_to(repo_root)),
        "inhouse_total_m_eur": ssot["inhouse_summary"]["total_inhouse_spend_m_eur"],  # type: ignore[index]
        "inhouse_saving_m_eur": ssot["inhouse_summary"]["recoverable_annual_saving_m_eur"],  # type: ignore[index]
        "arbitrage_saving_m_eur": round(ssot["arbitrage_summary"]["p25_arbitrage_saving_eur"] / 1e6, 2),  # type: ignore[index]
    }


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    summary = build_and_verify_all(root, enrich_live_prh=True)
    print("Atomic Build & Verification Complete:")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
