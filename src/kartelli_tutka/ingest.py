"""
Kartelli-Tutka Live Open-Data Connector & Deterministic Snapshot Builder.
Connects to:
  - PRH / YTJ Open Data v3 API (https://avoindata.prh.fi/opendata-ytj-api/v3/companies)
  - Tilastokeskus StatFin PxWeb API (https://pxdata.stat.fi/PxWeb/api/v1/fi/StatFin)
  - Deterministic offline SSOT snapshot generator (data/finland_procurement_snapshot.json)
"""

import json
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Optional

from .engine import build_ssot_payload


def fetch_prh_company_metadata(y_tunnus_or_name: str, timeout_sec: float = 4.0) -> Optional[Dict[str, str]]:
    """
    Queries the official Finnish Patent and Registration Office (PRH / YTJ) v3 Open API
    with zero API keys required. Gracefully returns None if offline.
    """
    is_ytunnus = len(y_tunnus_or_name) == 9 and y_tunnus_or_name[7] == "-"
    param = "businessId" if is_ytunnus else "name"
    url = f"https://avoindata.prh.fi/opendata-ytj-api/v3/companies?{param}={urllib.parse.quote(y_tunnus_or_name)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "KartelliTutka-OpenCore/2026.10"})
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            if resp.status != 200:
                return None
            payload = json.loads(resp.read().decode("utf-8"))
            companies = payload.get("companies", [])
            if not companies:
                return None
            c = companies[0]
            names = c.get("names", [])
            primary_name = names[0].get("name", y_tunnus_or_name) if names else y_tunnus_or_name
            return {
                "business_id": c.get("businessId", {}).get("value", y_tunnus_or_name),
                "registration_date": c.get("businessId", {}).get("registrationDate", ""),
                "official_name": primary_name,
                "eu_id": c.get("euId", {}).get("value", ""),
            }
    except Exception:
        return None


def write_ssot_snapshot(output_path: Path, enrich_live_prh: bool = False) -> Dict[str, object]:
    """
    Writes the canonical SSOT JSON snapshot to `data/finland_procurement_snapshot.json`.
    """
    payload = build_ssot_payload()
    if enrich_live_prh:
        for flow in payload.get("inhouse_flows", []):  # type: ignore[union-attr]
            meta = fetch_prh_company_metadata(flow["inhouse_vendor"])
            if meta:
                flow["prh_verified_business_id"] = meta["business_id"]
                flow["prh_registration_date"] = meta["registration_date"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload
