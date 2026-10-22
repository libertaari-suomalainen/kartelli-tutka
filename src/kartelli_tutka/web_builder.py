"""
Kartelli-Tutka — Suomen Talousinstituutti (STI) Editorial Research Report & Interactive Case Explorer.
Compiles the canonical SSOT payload and pre-generated legal filings into a self-contained,
mobile-first editorial web application (`dist/index.html`) where every KPI, flow step,
15 in-house companies, 31 regional price benchmarks, 10 Market Court (MAO) / Hilma cases,
and all 43 major Finnish public buyers (21 Wellbeing Counties + HUS + 21 largest municipalities)
are interactive, sortable, deep-linkable, and exportable to CSV/.txt/PDF.
"""

import json
from pathlib import Path
from typing import Dict

from .engine import (
    BASELINE_HILMA_TENDERS,
    BASELINE_INHOUSE_FLOWS,
    build_ssot_payload,
)
from .legal_generator import (
    generate_hankintaoikaisu,
    generate_hilma_spec_challenge,
    generate_julkisuuslaki_foia,
    generate_kkv_complaint,
)


def build_static_web_app(output_path: Path) -> Path:
    ssot = build_ssot_payload()

    kkv_filings: Dict[str, Dict[str, str]] = {}
    oikaisu_filings: Dict[str, Dict[str, str]] = {}
    for f in BASELINE_INHOUSE_FLOWS:
        kkv_filings[f.inhouse_y_tunnus] = generate_kkv_complaint(f)
        oikaisu_filings[f.inhouse_y_tunnus] = generate_hankintaoikaisu(f, f.buyer_kirjaamo_email)

    hilma_filings: Dict[str, Dict[str, str]] = {}
    for t in BASELINE_HILMA_TENDERS:
        hilma_filings[t.tender_id] = generate_hilma_spec_challenge(t, t.buyer_email)

    foia_filings: Dict[str, Dict[str, str]] = {}
    for b in ssot["public_buyer_directory"]:  # type: ignore[union-attr]
        foia_filings[b["y_tunnus"]] = generate_julkisuuslaki_foia(b["entity_name"], b["kirjaamo_email"])

    embedded_data = {
        "ssot": ssot,
        "kkv_filings": kkv_filings,
        "oikaisu_filings": oikaisu_filings,
        "hilma_filings": hilma_filings,
        "foia_filings": foia_filings,
    }
    json_blob = json.dumps(embedded_data, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="fi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Suomen Talousinstituutti — Julkisten Hankintojen (38,7 Mrd €) Tutkimusraportti 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #FAF8F7;
    --surface: #FFFFFF;
    --stone: #F2EEEE;
    --stone-hover: #EAE3E3;
    --border: #E5E0DF;
    --border-strong: #D5CECC;
    --text: #18181B;
    --body: #3F3F46;
    --muted: #6B7280;
    --accent: #1C9770;
    --accent-dark: #027D56;
    --accent-soft: #E8F5F0;
    --red: #B91C1C;
    --red-soft: #FEF2F2;
    --red-border: #FECACA;
    --amber: #B45309;
    --amber-soft: #FFFBEB;
    --amber-border: #FDE68A;
    --shadow: 0 4px 16px -2px rgba(24, 24, 27, 0.06), 0 2px 6px -1px rgba(24, 24, 27, 0.04);
    --shadow-hover: 0 12px 28px -4px rgba(28, 151, 112, 0.14), 0 4px 10px -2px rgba(24, 24, 27, 0.06);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }}
  body {{
    background: var(--bg);
    color: var(--body);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.62;
    font-size: 16px;
  }}
  h1, h2, h3, h4 {{
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text);
    letter-spacing: -0.02em;
  }}
  .topbar {{
    position: sticky;
    top: 0;
    z-index: 90;
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border);
    padding: 10px 20px;
  }}
  .topbar-inner {{
    max-width: 1180px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: nowrap;
  }}
  .brand {{
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    color: var(--text);
    min-width: 0;
  }}
  .brand-mark {{
    width: 36px;
    height: 36px;
    border-radius: 6px;
    background: var(--accent);
    color: #fff;
    font-family: 'DM Sans', sans-serif;
    font-weight: 800;
    font-size: 13.5px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}
  .brand-text {{ min-width: 0; }}
  .brand-text strong {{
    display: block;
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    font-weight: 700;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .brand-text span {{
    display: block;
    font-size: 11.5px;
    color: var(--muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .nav-actions {{ display: flex; align-items: center; gap: 6px; flex-shrink: 0; }}
  .lang-btn {{
    background: var(--stone);
    border: 1px solid var(--border-strong);
    color: var(--text);
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 12.5px;
    font-weight: 600;
    cursor: pointer;
    min-height: 36px;
    white-space: nowrap;
  }}
  .lang-btn.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
  .btn-primary {{
    background: var(--accent);
    color: #fff;
    text-decoration: none;
    padding: 7px 13px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    min-height: 36px;
    border: none;
    cursor: pointer;
    white-space: nowrap;
  }}
  .btn-primary:hover {{ background: var(--accent-dark); }}
  .btn-secondary {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border-strong);
    text-decoration: none;
    padding: 7px 12px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    min-height: 36px;
    cursor: pointer;
    white-space: nowrap;
  }}
  .btn-secondary:hover {{ background: var(--stone); }}
  .container {{ max-width: 1180px; margin: 0 auto; padding: 28px 20px 80px; }}
  .hero-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 38px 40px;
    box-shadow: var(--shadow);
    margin-bottom: 28px;
  }}
  .kicker {{
    display: inline-block;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent-dark);
    background: var(--accent-soft);
    padding: 5px 12px;
    border-radius: 4px;
    margin-bottom: 16px;
  }}
  .hero-title {{ font-size: clamp(26px, 4vw, 38px); line-height: 1.16; font-weight: 800; margin-bottom: 16px; }}
  .hero-lead {{ font-size: clamp(16px, 2vw, 18px); color: var(--body); max-width: 900px; margin-bottom: 22px; }}
  .callout-stone {{
    background: var(--stone);
    border-left: 4px solid var(--accent);
    padding: 18px 22px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 24px;
  }}
  .callout-stone h3 {{ font-size: 16.5px; margin-bottom: 6px; }}
  .callout-stone p {{ font-size: 15px; color: var(--body); }}
  .clickable-card {{
    cursor: pointer;
    transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;
    position: relative;
  }}
  .clickable-card:hover {{
    transform: translateY(-3px);
    box-shadow: var(--shadow-hover);
    border-color: var(--accent);
  }}
  .click-hint {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 700;
    color: var(--accent-dark);
    margin-top: 12px;
  }}
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
    margin-top: 10px;
  }}
  .kpi-card {{
    background: var(--bg);
    border: 1px solid var(--border-strong);
    border-radius: 8px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .kpi-label {{ font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); margin-bottom: 6px; }}
  .kpi-val {{ font-family: 'DM Sans', sans-serif; font-size: 25px; font-weight: 800; color: var(--text); line-height: 1.2; margin-bottom: 6px; }}
  .kpi-val.red {{ color: var(--red); }}
  .kpi-val.green {{ color: var(--accent-dark); }}
  .kpi-sub {{ font-size: 13.5px; color: var(--body); }}

  /* Search & Quick-Filter Hub */
  .search-hub {{
    background: var(--surface);
    border: 2px solid var(--accent);
    border-radius: 10px;
    padding: 22px 26px;
    box-shadow: var(--shadow);
    margin-bottom: 28px;
  }}
  .search-hub label {{
    display: block;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent-dark);
    margin-bottom: 6px;
  }}
  .input-box {{
    width: 100%;
    min-height: 46px;
    padding: 10px 14px;
    border-radius: 6px;
    border: 1px solid var(--border-strong);
    background: var(--bg);
    color: var(--text);
    font-size: 15.5px;
    font-family: inherit;
  }}
  .input-box:focus {{
    outline: 2px solid var(--accent);
    background: #fff;
  }}
  .quick-chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
    align-items: center;
  }}
  .chip-label {{
    font-size: 12.5px;
    font-weight: 600;
    color: var(--muted);
    margin-right: 4px;
  }}
  .chip {{
    background: var(--stone);
    border: 1px solid var(--border-strong);
    color: var(--text);
    padding: 5px 11px;
    border-radius: 99px;
    font-size: 12.5px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
  }}
  .chip:hover, .chip.active {{
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
  }}
  .search-status {{
    margin-top: 12px;
    padding: 10px 14px;
    background: var(--accent-soft);
    border-left: 4px solid var(--accent);
    border-radius: 4px;
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
    display: none;
  }}

  .section-block {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 34px;
    box-shadow: var(--shadow);
    margin-bottom: 28px;
  }}
  .section-head {{ margin-bottom: 22px; padding-bottom: 16px; border-bottom: 1px solid var(--border); }}
  .section-head h2 {{ font-size: clamp(20px, 2.8vw, 26px); margin-bottom: 6px; }}
  .section-head p {{ font-size: 15.5px; color: var(--muted); max-width: 860px; }}
  .flow-steps {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 12px; }}
  .flow-step {{ background: var(--stone); border: 1px solid var(--border-strong); border-radius: 8px; padding: 18px; }}
  .flow-step.danger {{ background: var(--red-soft); border-color: var(--red-border); }}
  .flow-badge {{
    display: inline-block;
    background: var(--accent);
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 9px;
    border-radius: 99px;
    margin-bottom: 8px;
  }}
  .flow-step.danger .flow-badge {{ background: var(--red); }}
  .flow-step h4 {{ font-size: 16px; margin-bottom: 6px; }}
  .flow-step p {{ font-size: 14px; color: var(--body); }}
  .cards-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 18px; }}
  .story-card {{
    background: var(--bg);
    border: 1px solid var(--border-strong);
    border-radius: 8px;
    padding: 20px 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .story-card.red-accent {{ border-left: 4px solid var(--red); }}
  .story-card.amber-accent {{ border-left: 4px solid var(--amber); }}
  .story-card.green-accent {{ border-left: 4px solid var(--accent); }}
  .story-top {{ margin-bottom: 14px; }}
  .card-kicker-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 10px;
  }}
  .card-id-pill {{
    font-size: 11.5px;
    font-weight: 600;
    color: var(--muted);
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 3px 8px;
    border-radius: 4px;
    white-space: nowrap;
  }}
  .story-card h3 {{
    font-size: 18px;
    line-height: 1.28;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
    word-break: normal;
  }}
  .story-subtitle {{
    font-size: 13px;
    font-weight: 600;
    color: var(--accent-dark);
    margin-bottom: 8px;
    line-height: 1.38;
  }}
  .story-commentary {{ font-size: 14px; color: var(--body); line-height: 1.52; margin-bottom: 4px; }}
  .metrics-strip {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 12px;
  }}
  .metrics-strip div {{ min-width: 0; }}
  .metrics-strip div span {{
    display: block;
    font-size: 11px;
    color: var(--muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 2px;
  }}
  .metrics-strip div strong {{
    display: block;
    font-family: 'DM Sans', sans-serif;
    font-size: 14.5px;
    font-weight: 700;
    color: var(--text);
    white-space: nowrap;
  }}
  .badge {{ display: inline-block; padding: 4px 10px; border-radius: 99px; font-size: 11.5px; font-weight: 700; white-space: nowrap; }}
  .badge-red {{ background: var(--red-soft); color: var(--red); border: 1px solid var(--red-border); }}
  .badge-amber {{ background: var(--amber-soft); color: var(--amber); border: 1px solid var(--amber-border); }}
  .badge-green {{ background: var(--accent-soft); color: var(--accent-dark); border: 1px solid #A7F3D0; }}
  .empty-box {{
    background: var(--stone);
    border: 1px dashed var(--border-strong);
    border-radius: 8px;
    padding: 16px 20px;
    font-size: 14px;
    color: var(--body);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    grid-column: 1 / -1;
  }}

  /* Sortable Full Registry Tables */
  .table-wrap {{
    margin-top: 26px;
    border-top: 1px solid var(--border);
    padding-top: 22px;
  }}
  .table-scroll {{
    overflow-x: auto;
    border: 1px solid var(--border-strong);
    border-radius: 8px;
    background: var(--surface);
    max-height: 520px;
    overflow-y: auto;
    margin-top: 12px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13.5px;
  }}
  th, td {{
    text-align: left;
    padding: 11px 13px;
    border-bottom: 1px solid var(--border);
  }}
  th {{
    position: sticky;
    top: 0;
    background: var(--stone);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 12px;
    text-transform: uppercase;
    z-index: 2;
    user-select: none;
  }}
  th.sortable {{
    cursor: pointer;
    transition: background 0.14s;
  }}
  th.sortable:hover {{
    background: var(--stone-hover);
    color: var(--accent-dark);
  }}
  tr.clickable-row {{ cursor: pointer; }}
  tr.clickable-row:hover td {{ background: var(--accent-soft); }}

  .modal-backdrop {{
    position: fixed;
    inset: 0;
    background: rgba(24, 24, 27, 0.55);
    backdrop-filter: blur(4px);
    z-index: 200;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }}
  .modal-backdrop.open {{ display: flex; }}
  .modal-card {{
    background: var(--surface);
    border: 1px solid var(--border-strong);
    border-radius: 12px;
    max-width: 780px;
    width: 100%;
    max-height: 88vh;
    overflow-y: auto;
    padding: 32px;
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.22);
    position: relative;
  }}
  .modal-close {{
    position: sticky;
    top: 0;
    float: right;
    background: var(--stone);
    border: 1px solid var(--border-strong);
    color: var(--text);
    border-radius: 99px;
    width: 38px;
    height: 38px;
    font-size: 18px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .modal-card h2 {{ font-size: 23px; margin-bottom: 8px; padding-right: 44px; }}
  .modal-sub {{ font-size: 14px; color: var(--muted); margin-bottom: 16px; }}
  .modal-toolbar {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
  }}
  .modal-section {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px 20px;
    margin-bottom: 16px;
  }}
  .modal-section h4 {{ font-size: 13.5px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent-dark); margin-bottom: 8px; }}
  .modal-section p, .modal-section li {{ font-size: 15px; color: var(--body); line-height: 1.6; }}
  .modal-section ul {{ padding-left: 20px; }}
  .modal-section li {{ margin-bottom: 6px; }}
  .customizer-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 10px 0;
  }}
  .customizer-grid input {{
    width: 100%;
    padding: 8px 11px;
    border-radius: 6px;
    border: 1px solid var(--border-strong);
    background: var(--surface);
    font-size: 13.5px;
    color: var(--text);
  }}
  .legal-box {{
    width: 100%;
    min-height: 220px;
    padding: 14px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 13px;
    line-height: 1.5;
    background: var(--surface);
    border: 1px solid var(--border-strong);
    border-radius: 6px;
    color: var(--text);
    margin: 10px 0 12px;
  }}
  footer {{
    max-width: 1180px;
    margin: 0 auto;
    padding: 28px 20px 60px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: 14px;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
  }}
  footer a {{ color: var(--accent-dark); font-weight: 600; text-decoration: none; }}
  @media print {{
    body * {{ visibility: hidden; }}
    #detail-modal, #detail-modal * {{ visibility: visible; }}
    #detail-modal {{ position: absolute; left: 0; top: 0; width: 100%; background: #fff; padding: 0; display: block !important; }}
    .modal-card {{ max-height: none; box-shadow: none; border: none; width: 100%; max-width: 100%; padding: 0; }}
    .modal-close, .modal-toolbar {{ display: none !important; }}
  }}
  @media (max-width: 960px) {{
    .topbar {{ position: relative; }}
    .topbar-inner {{ flex-wrap: wrap; }}
    .nav-actions {{ width: 100%; justify-content: flex-start; flex-wrap: wrap; }}
    .flow-steps, .customizer-grid {{ grid-template-columns: minmax(0, 1fr); }}
    .hero-card, .section-block {{ padding: 22px 18px; }}
  }}
  @media (max-width: 640px) {{
    html, body {{ overflow-x: hidden; max-width: 100vw; width: 100%; }}
    .topbar {{ position: relative; padding: 10px 12px; max-width: 100vw; overflow: hidden; }}
    .brand-text strong {{ white-space: normal; font-size: 14px; line-height: 1.22; }}
    .brand-text span {{ display: none; }}
    .btn-primary, .btn-secondary, .lang-btn {{ white-space: normal; font-size: 12px; padding: 6px 10px; min-height: 34px; }}
    .container {{ padding: 14px 12px 56px; max-width: 100vw; overflow-x: hidden; }}
    .hero-card, .section-block, .search-hub {{ padding: 18px 14px; min-width: 0; max-width: 100%; overflow: hidden; }}
    .hero-title {{ font-size: 22px; line-height: 1.22; word-wrap: break-word; }}
    .kpi-grid, .cards-grid, .flow-steps, .customizer-grid {{ grid-template-columns: minmax(0, 1fr); }}
    .story-card, .kpi-card {{ min-width: 0; max-width: 100%; }}
    .input-box {{ max-width: 100%; min-width: 0; font-size: 14px; }}
    .modal-backdrop {{ padding: 10px; align-items: flex-end; }}
    .modal-card {{ padding: 22px 18px; max-height: 92vh; border-radius: 12px 12px 0 0; }}
  }}
</style>
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <a href="#" class="brand">
      <div class="brand-mark">STI</div>
      <div class="brand-text">
        <strong data-i18n="brand_title">Suomen Talousinstituutti · Julkisten Hankintojen Tutkimus</strong>
        <span data-i18n="brand_sub">Tutkimusraportti 2026 · 15 sidosyksikköä, kaikki 21 hyvinvointialuetta + HUS + 21 kaupunkia</span>
      </div>
    </a>
    <div class="nav-actions">
      <button class="lang-btn active" id="btn-fi" onclick="setLang('fi')">Suomi</button>
      <button class="lang-btn" id="btn-en" onclick="setLang('en')">English</button>
      <a class="btn-secondary" href="https://libertaari-suomalainen.github.io/tukipalkkio-purku/" data-i18n="nav_sister">← Tutkimus I: Yritys- &amp; järjestötuet (11,5 mrd. €)</a>
      <a class="btn-primary" href="Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx" download data-i18n="nav_xlsx">⬇ Lataa Excel-aineisto (.xlsx)</a>
    </div>
  </div>
</header>

<main class="container">
  <section class="hero-card">
    <div class="kicker" data-i18n="hero_kicker">JULKISET HANKINNAT · TUTKIMUSRAPORTTI 2026 · 38,7 MRD. €/V</div>
    <h1 class="hero-title" data-i18n="hero_title">Julkisten hankintojen (38,7 mrd. €/v) rakenteellinen tehokkuus- ja sidosyksikköanalyysi</h1>
    <p class="hero-lead" data-i18n="hero_lead">
      Valtio, kaikki 21 hyvinvointialuetta, HUS ja 308 kuntaa ostavat ulkopuolisilta toimittajilta IT-järjestelmiä, hoivapalveluita, laboratoriotutkimuksia ja urakoita <strong>38,7 miljardilla eurolla vuodessa</strong> (Tilastokeskus S.13). Virallisiin tilinpäätöksiin (2024–2025), THL:n ja HALI ry:n yksikkökustannusvertailuihin sekä markkinaoikeuden (MAO) ja korkeimman hallinto-oikeuden (KHO) ratkaisuihin perustuva analyysimme osoittaa <strong>844 miljoonan euron suoraan mallinnetun vuotuisen tehostamispotentiaalin</strong> (ja koko 38,7 mrd. € hankintakantaan suhteutettuna <strong>1,1–2,2 mrd. €/v</strong>). <em>Huom: Yksityiset sopimustoimittajat toimivat laillisesti; tarkastelu kohdistuu julkisen sektorin omiin hankintarakenteisiin (Hankintalaki 15 § ja 75 §).</em>
    </p>
    <div class="callout-stone">
      <h3 data-i18n="summary_box_title">Miten luet tätä julkaisua? (Kaikki 15 sidosyksikköä, 31 yksikkökustannusvertailua, 10 MAO/KHO-ratkaisua ja 43 viranomaista ovat klikattavia)</h3>
      <p data-i18n="summary_box_body">
        <strong>Klikkaa mitä tahansa lukukorttia, sidosyksikköä tai palvelukeskusta (Istekki, Apotti, Sarastia/Numera, 2M-IT, Monetra, Tiera, Valtori, Fimlab, Tuomi, Meita, Kaarea, Polkka, ISLAB, Sansia, Hetapalvelut), alueellista yksikkökustannusvertailua, Finlex/KKV MAO-oikeustapausta tai mitä tahansa Suomen 21 hyvinvointialueesta ja 21 suurimmasta kaupungista</strong>. Voit ladata jokaisesta kohteesta valmiin hallinto-oikeudellisen tietopyynnön tai selvityspyynnön (.txt tai PDF).
      </p>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card clickable-card" onclick="openKpiModal('total_spend')">
        <div>
          <div class="kpi-label" data-i18n="kpi1_lbl">Julkiset ulkoiset ostot</div>
          <div class="kpi-val">38,70 mrd. €/v</div>
          <div class="kpi-sub" data-i18n="kpi1_sub">Valtion, 21 hyvinvointialueen, HUS:n ja kuntien vuotuiset ostot (Tilastokeskus S.13)</div>
        </div>
        <div class="click-hint" data-i18n="click_1">Klikkaa: Minne 38,7 mrd. € menee? →</div>
      </div>

      <div class="kpi-card clickable-card" onclick="openKpiModal('inhouse_leak')">
        <div>
          <div class="kpi-label" data-i18n="kpi2_lbl">15 Sidosyksikköä &amp; TVT-keskus</div>
          <div class="kpi-val red">1,96 mrd. €/v</div>
          <div class="kpi-sub" data-i18n="kpi2_sub">Tilinpäätösten (2024–2025) mukainen liikevaihto — kilpailupotentiaali 230,99 M€/v (KKV/VATT-malli)</div>
        </div>
        <div class="click-hint" data-i18n="click_2">Klikkaa: Hankintalain 15 § &amp; KHO 8.10.2025 →</div>
      </div>

      <div class="kpi-card clickable-card" onclick="openKpiModal('price_spread')">
        <div>
          <div class="kpi-label" data-i18n="kpi3_lbl">Alueellinen P25-kustannusvertailu</div>
          <div class="kpi-val green">594,40 milj. €/v</div>
          <div class="kpi-sub" data-i18n="kpi3_sub">Säästöpotentiaali, kun kalleimmat alueet saavuttavat edullisimman neljänneksen (P25) yksikkökustannuksen</div>
        </div>
        <div class="click-hint" data-i18n="click_3">Klikkaa: THL / HALI yksikkökustannuserot →</div>
      </div>

      <div class="kpi-card clickable-card" onclick="openKpiModal('single_bid')">
        <div>
          <div class="kpi-label" data-i18n="kpi4_lbl">Yhden tarjouksen kilpailutukset</div>
          <div class="kpi-val red">~15–16 % (KKV)</div>
          <div class="kpi-sub" data-i18n="kpi4_sub">KKV:n mukaan n. 15–16 % tarjouskilpailuista saa vain 1 tarjouksen (~1,5 mrd. €/v) — osiin jakaminen (75 §) lisää kilpailua</div>
        </div>
        <div class="click-hint" data-i18n="click_4">Klikkaa: 10 MAO/KHO-ratkaisua (Finlex) →</div>
      </div>
    </div>
  </section>

  <!-- GLOBAL SEARCH & QUICK FILTERS -->
  <section class="search-hub" id="haku">
    <div>
      <label for="search-box" data-i18n="lbl_search">Hae sidosyksikköä (15 kpl), hyvinvointialuetta tai kaupunkia (43 kpl), MAO-tapausta tai palvelua</label>
      <input id="search-box" type="search" class="input-box" placeholder="Kokeile esim. Istekki, Apotti, Sarastia, Fimlab, Tuomi, Meita, HUS, Pirha, Varha, Lapha, Kuopio, Oulu..." />
    </div>
    <div class="quick-chips">
      <span class="chip-label" data-i18n="chip_lbl">Pikavalinnat:</span>
      <button type="button" class="chip active" onclick="setSearch('')" data-i18n="chip_all">Näytä kaikki</button>
      <button type="button" class="chip" onclick="setSearch('Istekki')">Istekki Oy</button>
      <button type="button" class="chip" onclick="setSearch('Apotti')">Oy Apotti Ab</button>
      <button type="button" class="chip" onclick="setSearch('Sarastia')">Sarastia / Numera</button>
      <button type="button" class="chip" onclick="setSearch('2M-IT')">2M-IT Oy</button>
      <button type="button" class="chip" onclick="setSearch('Fimlab')">Fimlab &amp; ISLAB</button>
      <button type="button" class="chip" onclick="setSearch('Tuomi')">Tuomi Logistiikka</button>
      <button type="button" class="chip" onclick="setSearch('Pirha')">Pirha (Pirkanmaa)</button>
      <button type="button" class="chip" onclick="setSearch('HUS')">HUS &amp; Vake</button>
      <button type="button" class="chip" onclick="setSearch('Varha')">Varha (Varsinais-Suomi)</button>
      <button type="button" class="chip" onclick="setSearch('Lapha')">Lapha (Lappi)</button>
    </div>
    <div class="search-status" id="search-status"></div>
  </section>

  <section class="section-block" id="sec-inhouse">
    <div class="section-head">
      <h2 data-i18n="s1_title">1. Sidosyksikköjärjestelmä ja Hankintalain 15 § (15 yksikköä = 1,96 mrd. €/v tilinpäätösliikevaihto)</h2>
      <p data-i18n="s1_sub">
        Korkein hallinto-oikeus (KHO 8.10.2025 taltio 2250) ja markkinaoikeus (MAO:154/2024 &amp; MAO:500/2024) vahvistivat, ettei julkinen hankintayksikkö voi tehdä suorahankintoja sidosyksikköpoikkeuksella (Hankintalaki 15 §), jos sen omistusosuus on muodollinen (esim. 0,04–0,09 %) eikä se käytä yhtiössä tosiasiallista määräysvaltaa. Klikkaa vaihetta, yhtiökorttia tai taulukon riviä.
      </p>
    </div>

    <div class="flow-steps">
      <div class="flow-step clickable-card" onclick="openFlowModal(1)">
        <span class="flow-badge" data-i18n="f1_step">Vaihe 1 · Klikkaa</span>
        <h4 data-i18n="f1_title">Hajautettu pienomistus (&lt;10 %)</h4>
        <p data-i18n="f1_desc">Kunta tai hyvinvointialue merkitsee pienen osakeosuuden (esim. 0,04–2,5 %) yhteisestä ICT-, laboratorio- tai taloushallintoyhtiöstä.</p>
      </div>
      <div class="flow-step clickable-card" onclick="openFlowModal(2)">
        <span class="flow-badge" data-i18n="f2_step">Vaihe 2 · Klikkaa</span>
        <h4 data-i18n="f2_title">Sidosyksikkösuorahankinta (15 §)</h4>
        <p data-i18n="f2_desc">Sidosyksikköpoikkeukseen vedoten palvelut tilataan suoraan yhtiöltä ilman omaa avointa tarjouskilpailua (KHO 8.10.2025 T2250 &amp; HE 2/2026 vp).</p>
      </div>
      <div class="flow-step danger clickable-card" onclick="openFlowModal(3)">
        <span class="flow-badge" data-i18n="f3_step">Vaihe 3 · Rakenne</span>
        <h4 data-i18n="f3_title">Hallintoporras ja puitesopimukset</h4>
        <p data-i18n="f3_desc">Sidosyksikkö kokoaa hankinnat ja hankkii osan järjestelmistä kaupallisilta sopimustoimittajilta; moniportainen rakenne lisää hallinto- ja koordinointikustannuksia.</p>
      </div>
      <div class="flow-step danger clickable-card" onclick="openFlowModal(4)">
        <span class="flow-badge" data-i18n="f4_step">Vaihe 4 · Säästöpotentiaali</span>
        <h4 data-i18n="f4_title">230,99 milj. €/v tehostamispotentiaali</h4>
        <p data-i18n="f4_desc">KKV:n ja VATT:n tutkimuksiin pohjautuvalla 11–14 % kilpailu- ja koordinointihyödyllä avoin kilpailutus ja osiin jakaminen vapauttaisi n. 231 M€/v.</p>
      </div>
    </div>

    <h3 style="font-size:19px; margin: 20px 0 12px;" data-i18n="inhouse_heading">Klikkaa sidosyksikköä nähdäksesi tilinpäätöstiedot (2024–2025) ja hallinto-oikeudellisen selvityspyynnön:</h3>
    <div class="cards-grid" id="inhouse-cards"></div>

    <div class="table-wrap">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
        <div>
          <h3 style="font-size:18.5px;" data-i18n="inhouse_tbl_title">Kaikki 15 sidosyksikköä ja palvelukeskusta taulukossa (Klikkaa saraketta lajitellaksesi tai riviä avataksesi)</h3>
          <p style="font-size:13.5px;color:var(--muted);" id="inhouse-count-sub"></p>
        </div>
        <button type="button" class="btn-secondary" onclick="exportInhouseCsv()" data-i18n="inhouse_csv_btn">⬇ Vie sidosyksikkötaulukko (.csv)</button>
      </div>
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th class="sortable" onclick="sortInhouse('inhouse_vendor')"><span data-i18n="th_ih_name">Sidosyksikkö &amp; Y-tunnus</span> <span id="sort-ih-inhouse_vendor"></span></th>
              <th class="sortable" onclick="sortInhouse('buyer_name')"><span data-i18n="th_ih_buy">Omistaja- / tilaajaryhmä</span> <span id="sort-ih-buyer_name"></span></th>
              <th class="sortable" onclick="sortInhouse('buyer_equity_share_pct')"><span data-i18n="th_ih_eq">Viiteomistus-%</span> <span id="sort-ih-buyer_equity_share_pct"></span></th>
              <th class="sortable" onclick="sortInhouse('annual_spend_m_eur')"><span data-i18n="th_ih_sp">Liikevaihto (M€/v)</span> <span id="sort-ih-annual_spend_m_eur">▼</span></th>
              <th class="sortable" onclick="sortInhouse('inhouse_markup_pct')"><span data-i18n="th_ih_mk">Koordinointi (%)</span> <span id="sort-ih-inhouse_markup_pct"></span></th>
              <th class="sortable" onclick="sortInhouse('recoverable_saving_m_eur')"><span data-i18n="th_ih_sv">Säästöpotentiaali (M€/v)</span> <span id="sort-ih-recoverable_saving_m_eur"></span></th>
            </tr>
          </thead>
          <tbody id="inhouse-tbody"></tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="section-block" id="sec-arbitrage">
    <div class="section-head">
      <h2 data-i18n="s2_title">2. Alueellinen yksikkökustannusvertailu (THL / HALI / KKV): P25-vertailutaso (594,40 M€/v)</h2>
      <p data-i18n="s2_sub">
        Klikkaa mitä tahansa alueellista vertailukorttia nähdäksesi, kuinka suuri säästöpotentiaali syntyy, jos yli 25. persentiilin (P25) yksikkökustannustason alueet saavuttavat edullisimman neljänneksen kustannustason.
      </p>
    </div>
    <div class="cards-grid" id="arbitrage-cards"></div>
  </section>

  <section class="section-block" id="sec-hilma">
    <div class="section-head">
      <h2 data-i18n="s3_title">3. Markkinaoikeuden (MAO) ja KHO:n vahvistetut julkisten hankintojen ratkaisut (10 Finlex/KKV-tapausta)</h2>
      <p data-i18n="s3_sub">
        Klikkaa dokumentoitua markkinaoikeuden (MAO) tai korkeimman hallinto-oikeuden (KHO) ratkaisua (2023–2025) nähdäksesi ratkaisun oikeudellisen sisällön sekä mallipohjan avoimen kilpailutuksen ja osiin jakamisen (Hankintalaki 75 §) edistämiseksi.
      </p>
    </div>
    <div class="cards-grid" id="hilma-cards"></div>
  </section>

  <section class="section-block" id="sec-foia">
    <div class="section-head">
      <h2 data-i18n="s4_title">4. Julkisuuslain (621/1999 13 §) ostolaskutietopyyntö (Kaikki 21 hyvinvointialuetta + HUS + 21 kaupunkia = 43 viranomaista)</h2>
      <p data-i18n="s4_sub">
        Julkisuuslain (621/1999) mukaan jokaisella on oikeus saada viranomaisen julkiset ostolaskutiedot koneluettavassa muodossa 14 vuorokauden kuluessa. Klikkaa mitä tahansa 43 viranomaisesta avataksesi valmiin tietopyynnön.
      </p>
    </div>
    <div class="cards-grid" id="buyer-cards"></div>

    <div class="table-wrap">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
        <div>
          <h3 style="font-size:18.5px;" data-i18n="buyer_tbl_title">Kaikki 43 julkista ostajaa (21 hyvinvointialuetta + HUS + 21 suurinta kaupunkia)</h3>
          <p style="font-size:13.5px;color:var(--muted);" id="buyer-count-sub"></p>
        </div>
        <button type="button" class="btn-secondary" onclick="exportBuyersCsv()" data-i18n="buyer_csv_btn">⬇ Vie kaikki 43 kirjaamoa (.csv)</button>
      </div>
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th class="sortable" onclick="sortBuyers('entity_name')"><span data-i18n="th_b_name">Hankintayksikkö &amp; Y-tunnus</span> <span id="sort-b-entity_name"></span></th>
              <th class="sortable" onclick="sortBuyers('entity_type')"><span data-i18n="th_b_type">Tyyppi</span> <span id="sort-b-entity_type"></span></th>
              <th class="sortable" onclick="sortBuyers('annual_purchases_m_eur')"><span data-i18n="th_b_sp">Ulkoiset ostot (M€/v)</span> <span id="sort-b-annual_purchases_m_eur">▼</span></th>
              <th class="sortable" onclick="sortBuyers('publishes_open_invoices')"><span data-i18n="th_b_op">Avoin ostolaskudata</span> <span id="sort-b-publishes_open_invoices"></span></th>
              <th><span data-i18n="th_b_sh">Sidosyksiköt &amp; Kirjaamo</span></th>
            </tr>
          </thead>
          <tbody id="buyer-tbody"></tbody>
        </table>
      </div>
    </div>
  </section>
</main>

<div class="modal-backdrop" id="detail-modal" onclick="if(event.target===this)closeModal()">
  <div class="modal-card">
    <button class="modal-close" onclick="closeModal()" aria-label="Sulje">✕</button>
    <div id="modal-content"></div>
  </div>
</div>

<footer>
  <div>
    <strong>Suomen Talousinstituutti · Avoin Tutkimusjulkaisu (2026)</strong><br/>
    Lähdeaineisto: Tilastokeskus S.13, PRH YTJ, Tilinpäätökset 2024–2025, THL, HALI ry, KKV sekä Finlex (MAO &amp; KHO 8.10.2025 taltio 2250).
  </div>
  <div>
    <a href="Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx" download>Lataa 5-välilehtinen Excel (.xlsx)</a> ·
    <a href="https://github.com/libertaari-suomalainen/kartelli-tutka">Avoin lähdekoodi (GitHub)</a> ·
    <a href="https://libertaari-suomalainen.github.io/tukipalkkio-purku/">Tutkimus I: Yritys- ja järjestötukien läpivalaisu (STEA &amp; Business Finland)</a>
  </div>
</footer>
"""
    html += f"""
<script>
const APP = {json_blob};
let LANG = 'fi';
let INHOUSE_SORT = {{ col: 'annual_spend_m_eur', asc: false }};
let BUYER_SORT = {{ col: 'annual_purchases_m_eur', asc: false }};
let LAST_INHOUSE = [];
let LAST_BUYERS = [];
let ACTIVE_BASE_LEGAL_TEXT = '';
let ACTIVE_RECIPIENT_EMAIL = '';
let ACTIVE_SUBJECT = '';

const fmtM = (n) => Number(n).toLocaleString('fi-FI', {{minimumFractionDigits: 2, maximumFractionDigits: 2}}) + ' milj. €';
const fmtCardM = (n) => {{
  const m = Number(n);
  if (!m || Math.abs(m) < 0.005) return '0 €';
  const digits = Math.abs(m) >= 100 ? 0 : 1;
  return m.toLocaleString('fi-FI', {{minimumFractionDigits: digits, maximumFractionDigits: digits}}) + ' M€';
}};
const fmtEUR = (n) => Math.round(Number(n)).toLocaleString('fi-FI') + ' €';
const escHtml = (s) => String(s || '').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));

const CPV_NAMES = {{
  "85121000-LocumMD": {{
    fi: "Vuokralääkärit & päivystys (CPV 85121000)",
    en: "Locum Physicians & ER Staffing (CPV 85121000)",
    unit_fi: "tunti",
    unit_en: "hour"
  }},
  "72260000-ITWorkstation": {{
    fi: "IT-työasemat & lähituki (CPV 72260000)",
    en: "IT Workstations & Support (CPV 72260000)",
    unit_fi: "työntekijä/v",
    unit_en: "FTE/year"
  }},
  "48814000-EHR": {{
    fi: "Potilastietojärjestelmät APTJ (CPV 48814000)",
    en: "EHR Patient Information Systems (CPV 48814000)",
    unit_fi: "lääkäri/hoitaja/v",
    unit_en: "clinician/year"
  }},
  "85311100-ElderlyCare": {{
    fi: "Ympärivuorokautinen hoiva (CPV 85311100)",
    en: "24/7 Elderly Assisted Living (CPV 85311100)",
    unit_fi: "hoitopäivä",
    unit_en: "resident-day"
  }},
  "60130000-SoteTransport": {{
    fi: "Sote- ja koulukuljetukset (CPV 60130000)",
    en: "Statutory Sote & School Transport (CPV 60130000)",
    unit_fi: "matka",
    unit_en: "trip"
  }}
}};

const I18N = {{
  fi: {{
    brand_title: "Suomen Talousinstituutti · Julkisten Hankintojen Tutkimus",
    brand_sub: "Tutkimusraportti 2026 · 15 sidosyksikköä, kaikki 21 hyvinvointialuetta + HUS + 21 kaupunkia",
    nav_sister: "← Tutkimus I: Yritys- & järjestötuet",
    nav_xlsx: "⬇ Lataa Excel-aineisto (.xlsx)",
    hero_kicker: "JULKISET HANKINNAT · TUTKIMUSRAPORTTI 2026 · 38,7 MRD. €/V",
    hero_title: "Julkisten hankintojen (38,7 mrd. €/v) rakenteellinen tehokkuus- ja sidosyksikköanalyysi",
    hero_lead: "Valtio, kaikki 21 hyvinvointialuetta, HUS ja 308 kuntaa ostavat ulkopuolisilta toimittajilta IT-järjestelmiä, hoivapalveluita, laboratoriotutkimuksia ja urakoita <strong>38,7 miljardilla eurolla vuodessa</strong> (Tilastokeskus S.13). Virallisiin tilinpäätöksiin (2024–2025), THL:n ja HALI ry:n yksikkökustannusvertailuihin sekä markkinaoikeuden (MAO) ja korkeimman hallinto-oikeuden (KHO) ratkaisuihin perustuva analyysimme osoittaa <strong>844 miljoonan euron suoraan mallinnetun vuotuisen tehostamispotentiaalin</strong> (ja koko 38,7 mrd. € hankintakantaan suhteutettuna <strong>1,1–2,2 mrd. €/v</strong>). <em>Huom: Yksityiset sopimustoimittajat toimivat laillisesti; tarkastelu kohdistuu julkisen sektorin omiin hankintarakenteisiin (Hankintalaki 15 § ja 75 §).</em>",
    summary_box_title: "Miten luet tätä julkaisua? (Kaikki 15 sidosyksikköä, 31 yksikkökustannusvertailua, 10 MAO/KHO-ratkaisua ja 43 viranomaista ovat klikattavia)",
    summary_box_body: "<strong>Klikkaa mitä tahansa lukukorttia, sidosyksikköä tai palvelukeskusta (Istekki, Apotti, Sarastia/Numera, 2M-IT, Monetra, Tiera, Valtori, Fimlab, Tuomi, Meita, Kaarea, Polkka, ISLAB, Sansia, Hetapalvelut), alueellista yksikkökustannusvertailua, Finlex/KKV MAO-oikeustapausta tai mitä tahansa Suomen 21 hyvinvointialueesta ja 21 suurimmasta kaupungista</strong>. Voit ladata jokaisesta kohteesta valmiin hallinto-oikeudellisen tietopyynnön tai selvityspyynnön (.txt tai PDF).",
    kpi1_lbl: "Julkiset ulkoiset ostot",
    kpi1_sub: "Valtion, 21 hyvinvointialueen, HUS:n ja kuntien vuotuiset ostot (Tilastokeskus S.13)",
    click_1: "Klikkaa: Minne 38,7 mrd. € menee? →",
    kpi2_lbl: "15 Sidosyksikköä & TVT-keskus",
    kpi2_sub: "Tilinpäätösten (2024–2025) mukainen liikevaihto — kilpailupotentiaali 230,99 M€/v (KKV/VATT-malli)",
    click_2: "Klikkaa: Hankintalain 15 § & KHO 8.10.2025 →",
    kpi3_lbl: "Alueellinen P25-kustannusvertailu",
    kpi3_sub: "Säästöpotentiaali, kun kalleimmat alueet saavuttavat edullisimman neljänneksen (P25) yksikkökustannuksen",
    click_3: "Klikkaa: THL / HALI yksikkökustannuserot →",
    kpi4_lbl: "Yhden tarjouksen kilpailutukset",
    kpi4_sub: "KKV:n mukaan n. 15–16 % tarjouskilpailuista saa vain 1 tarjouksen (~1,5 mrd. €/v) — osiin jakaminen (75 §) lisää kilpailua",
    click_4: "Klikkaa: 10 MAO/KHO-ratkaisua (Finlex) →",
    lbl_search: "Hae sidosyksikköä (15 kpl), hyvinvointialuetta tai kaupunkia (43 kpl), MAO-tapausta tai palvelua",
    chip_lbl: "Pikavalinnat:",
    chip_all: "Näytä kaikki",
    s1_title: "1. Sidosyksikköjärjestelmä ja Hankintalain 15 § (15 yksikköä = 1,96 mrd. €/v tilinpäätösliikevaihto)",
    s1_sub: "Korkein hallinto-oikeus (KHO 8.10.2025 taltio 2250) ja markkinaoikeus (MAO:154/2024 & MAO:500/2024) vahvistivat, ettei julkinen hankintayksikkö voi tehdä suorahankintoja sidosyksikköpoikkeuksella (Hankintalaki 15 §), jos sen omistusosuus on muodollinen (esim. 0,04–0,09 %) eikä se käytä yhtiössä tosiasiallista määräysvaltaa. Klikkaa vaihetta, yhtiökorttia tai taulukon riviä.",
    f1_step: "Vaihe 1 · Klikkaa",
    f1_title: "Hajautettu pienomistus (<10 %)",
    f1_desc: "Kunta tai hyvinvointialue merkitsee pienen osakeosuuden (esim. 0,04–2,5 %) yhteisestä ICT-, laboratorio- tai taloushallintoyhtiöstä.",
    f2_step: "Vaihe 2 · Klikkaa",
    f2_title: "Sidosyksikkösuorahankinta (15 §)",
    f2_desc: "Sidosyksikköpoikkeukseen vedoten palvelut tilataan suoraan yhtiöltä ilman omaa avointa tarjouskilpailua (KHO 8.10.2025 T2250 & HE 2/2026 vp).",
    f3_step: "Vaihe 3 · Rakenne",
    f3_title: "Hallintoporras ja puitesopimukset",
    f3_desc: "Sidosyksikkö kokoaa hankinnat ja hankkii osan järjestelmistä kaupallisilta sopimustoimittajilta; moniportainen rakenne lisää hallinto- ja koordinointikustannuksia.",
    f4_step: "Vaihe 4 · Säästöpotentiaali",
    f4_title: "230,99 milj. €/v tehostamispotentiaali",
    f4_desc: "KKV:n ja VATT:n tutkimuksiin pohjautuvalla 11–14 % kilpailu- ja koordinointihyödyllä avoin kilpailutus ja osiin jakaminen vapauttaisi n. 231 M€/v.",
    inhouse_heading: "Klikkaa sidosyksikköä nähdäksesi tilinpäätöstiedot (2024–2025) ja hallinto-oikeudellisen selvityspyynnön:",
    inhouse_tbl_title: "Kaikki 15 sidosyksikköä ja palvelukeskusta taulukossa (Klikkaa saraketta lajitellaksesi tai riviä avataksesi)",
    inhouse_csv_btn: "⬇ Vie sidosyksikkötaulukko (.csv)",
    th_ih_name: "Sidosyksikkö & Y-tunnus",
    th_ih_buy: "Omistaja- / tilaajaryhmä",
    th_ih_eq: "Viiteomistus-%",
    th_ih_sp: "Liikevaihto (M€/v)",
    th_ih_mk: "Koordinointi (%)",
    th_ih_sv: "Säästöpotentiaali (M€/v)",
    s2_title: "2. Alueellinen yksikkökustannusvertailu (THL / HALI / KKV): P25-vertailutaso (594,40 M€/v)",
    s2_sub: "Klikkaa mitä tahansa alueellista vertailukorttia nähdäksesi, kuinka suuri säästöpotentiaali syntyy, jos yli 25. persentiilin (P25) yksikkökustannustason alueet saavuttavat edullisimman neljänneksen kustannustason.",
    s3_title: "3. Markkinaoikeuden (MAO) ja KHO:n vahvistetut julkisten hankintojen ratkaisut (10 Finlex/KKV-tapausta)",
    s3_sub: "Klikkaa dokumentoitua markkinaoikeuden (MAO) tai korkeimman hallinto-oikeuden (KHO) ratkaisua (2023–2025) nähdäksesi ratkaisun oikeudellisen sisällön sekä mallipohjan avoimen kilpailutuksen ja osiin jakamisen (Hankintalaki 75 §) edistämiseksi.",
    s4_title: "4. Julkisuuslain (621/1999 13 §) ostolaskutietopyyntö (Kaikki 21 hyvinvointialuetta + HUS + 21 kaupunkia = 43 viranomaista)",
    s4_sub: "Julkisuuslain (621/1999) mukaan jokaisella on oikeus saada viranomaisen julkiset ostolaskutiedot koneluettavassa muodossa 14 vuorokauden kuluessa. Klikkaa mitä tahansa 43 viranomaisesta avataksesi valmiin tietopyynnön.",
    buyer_tbl_title: "Kaikki 43 julkista ostajaa (21 hyvinvointialuetta + HUS + 21 suurinta kaupunkia)",
    buyer_csv_btn: "⬇ Vie kaikki 43 kirjaamoa (.csv)",
    th_b_name: "Hankintayksikkö & Y-tunnus",
    th_b_type: "Tyyppi",
    th_b_sp: "Ulkoiset ostot (M€/v)",
    th_b_op: "Avoin ostolaskudata",
    th_b_sh: "Sidosyksiköt & Kirjaamo"
  }},
  en: {{
    brand_title: "Finnish Economic Institute (STI) · Public Procurement Analysis",
    brand_sub: "2026 Empirical Report · 15 In-House Units, All 21 Wellbeing Counties + HUS + 21 Cities",
    nav_sister: "← Study I: Corporate & NGO Grants",
    nav_xlsx: "⬇ Download Excel Dataset (.xlsx)",
    hero_kicker: "PUBLIC PROCUREMENT · RESEARCH REPORT 2026 · €38.7B/YR",
    hero_title: "Structural Efficiency & In-House Governance Analysis of Finnish Public Procurement (€38.7B/yr)",
    hero_lead: "Finland's state, all 21 Wellbeing Counties, HUS, and 308 municipalities spend <strong>€38.7 billion per year</strong> purchasing IT systems, healthcare services, lab diagnostics, and contracts (Statistics Finland S.13). Grounded in audited 2024–2025 financial statements, THL/HALI unit-cost benchmarks, and Finlex Market Court (MAO) & Supreme Administrative Court (KHO) rulings, our analysis models <strong>€844M/yr in direct structural efficiency potential</strong> (and <strong>€1.1B–€2.2B/yr</strong> across the full €38.7B procurement base). <em>Note: Private framework vendors act lawfully; the policy analysis focuses on public procurement governance (Procurement Act § 15 & § 75).</em>",
    summary_box_title: "How to Read This Interactive Report (All 15 In-House Entities, 31 Cost Benchmarks, 10 MAO/KHO Rulings & 43 Buyers Are Clickable)",
    summary_box_body: "<strong>Click any metric card, in-house unit (Istekki, Apotti, Sarastia/Numera, 2M-IT, Monetra, Tiera, Valtori, Fimlab, Tuomi, Meita, Kaarea, Polkka, ISLAB, Sansia, Hetapalvelut), regional unit-cost benchmark, Finlex MAO case, or any of Finland's 21 Wellbeing Counties and 21 largest cities</strong> to inspect primary-source figures and download administrative requests.",
    kpi1_lbl: "Total Public External Purchases",
    kpi1_sub: "Annual external purchases by the state, 21 Wellbeing Counties, HUS, and 308 municipalities",
    click_1: "Click: Where does the €38.7B go? →",
    kpi2_lbl: "15 In-House & State IT Units",
    kpi2_sub: "Audited 2024–2025 turnover (€1.96B/yr) — €230.99M/yr competitive efficiency benchmark",
    click_2: "Click: Procurement Act § 15 & KHO 8.10.2025 →",
    kpi3_lbl: "Regional P25 Cost Benchmark",
    kpi3_sub: "Annual efficiency potential when high-cost counties converge to top-quartile (P25) unit costs",
    click_3: "Click: THL / HALI unit-cost dispersion →",
    kpi4_lbl: "Single-Bid Public Tenders",
    kpi4_sub: "KKV reports ~15–16% of tenders receive only 1 bid (~€1.5B/yr) — dividing contracts into lots (§ 75) boosts competition",
    click_4: "Click: 10 Verified MAO/KHO Rulings →",
    lbl_search: "Search in-house unit (15), Wellbeing County or city (43), MAO ruling, or category",
    chip_lbl: "Quick filters:",
    chip_all: "Show all",
    s1_title: "1. In-House Entities & Procurement Act § 15 (15 Units = €1.96B/yr Audited Turnover)",
    s1_sub: "Finland's Supreme Administrative Court (KHO 8.10.2025 T2250) and Market Court (MAO:154/2024 & MAO:500/2024) confirmed that a public authority cannot make direct in-house awards (§ 15) when it holds only a nominal share (e.g. 0.04%–0.09%) without genuine governance control.",
    f1_step: "Step 1 · Click",
    f1_title: "Dispersed Minority Equity (<10%)",
    f1_desc: "A municipality or Wellbeing County holds a small minority share (0.04%–2.5%) in a joint ICT, laboratory, or financial services company.",
    f2_step: "Step 2 · Click",
    f2_title: "In-House Direct Award (§ 15)",
    f2_desc: "Relying on the in-house exemption, services are ordered directly without an open tender (reviewed in KHO 8.10.2025 T2250 & HE 2/2026 vp).",
    f3_step: "Step 3 · Structure",
    f3_title: "Administrative Layer & Frameworks",
    f3_desc: "The in-house unit aggregates demand and procures components from commercial vendors; multi-tier structures add coordination overhead.",
    f4_step: "Step 4 · Efficiency Potential",
    f4_title: "€230.99M/yr Efficiency Benchmark",
    f4_desc: "Applying a conservative 11–14% KKV/VATT competitive tendering benchmark across the €1.96B volume yields ~€231M/yr in savings.",
    inhouse_heading: "Click any in-house unit to inspect 2024–2025 financial statement figures & administrative review templates:",
    inhouse_tbl_title: "All 15 In-House Units & Service Centers in Table View (Click Header to Sort or Row to Open)",
    inhouse_csv_btn: "⬇ Export In-House Table (.csv)",
    th_ih_name: "In-House Entity & ID",
    th_ih_buy: "Owner / Buyer Group",
    th_ih_eq: "Ref. Equity %",
    th_ih_sp: "Turnover (M€/yr)",
    th_ih_mk: "Coordination (%)",
    th_ih_sv: "Efficiency Potential (M€/yr)",
    s2_title: "2. Regional Unit-Cost Benchmark (THL / HALI / KKV): P25 Quartile Comparison (€594.40M/yr)",
    s2_sub: "Click any regional benchmark card to see the modeled cost reduction if regions above the 25th percentile (P25) converge to the P25 benchmark.",
    s3_title: "3. Market Court (MAO) & Supreme Administrative Court (KHO) Rulings (10 Verified Finlex/KKV Cases)",
    s3_sub: "Click any verified MAO or KHO ruling (2023–2025) to inspect the court's legal findings and download an administrative template promoting open competition and division into lots (§ 75).",
    s4_title: "4. Request Public Purchase Invoices Under the Openness of Government Activities Act (All 21 Wellbeing Counties + HUS + 21 Cities = 43 Authorities)",
    s4_sub: "Under Finland's Openness Act (621/1999 § 13 & § 16.3), citizens have the right to receive machine-readable public purchase invoice data within 14 days.",
    buyer_tbl_title: "All 43 Major Public Buyers (All 21 Wellbeing Counties + HUS + 21 Largest Cities)",
    buyer_csv_btn: "⬇ Export All 43 Buyers (.csv)",
    th_b_name: "Public Authority & ID",
    th_b_type: "Type",
    th_b_sp: "External Spend (M€/yr)",
    th_b_op: "Open Invoice Ledger",
    th_b_sh: "In-House Units & Registry"
  }}
}};

function setHashQuietly(hashStr) {{
  if (history.replaceState) {{
    history.replaceState(null, '', '#' + hashStr);
  }} else {{
    window.location.hash = hashStr;
  }}
}}

function copyDirectLink(btn) {{
  navigator.clipboard.writeText(window.location.href);
  const orig = btn.textContent;
  btn.textContent = LANG === 'fi' ? '✓ Suora linkki kopioitu!' : '✓ Direct Link Copied!';
  setTimeout(() => {{ btn.textContent = orig; }}, 1800);
}}

function downloadTextFile(filename, textContent) {{
  const blob = new Blob([textContent], {{ type: 'text/plain;charset=utf-8' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}}

function openModalHtml(title, subtitle, sectionsHtml, hashId) {{
  if (hashId) setHashQuietly(hashId);
  const fi = LANG === 'fi';
  document.getElementById('modal-content').innerHTML = `
    <h2>${{title}}</h2>
    <div class="modal-sub">${{subtitle}}</div>
    <div class="modal-toolbar">
      <button type="button" class="btn-secondary" onclick="copyDirectLink(this)">${{fi ? '🔗 Kopioi suora linkki tähän kohteeseen' : '🔗 Copy Direct Link to This Item'}}</button>
      <button type="button" class="btn-secondary" onclick="window.print()">${{fi ? '🖨 Tulosta / Tallenna PDF' : '🖨 Print / Save as PDF'}}</button>
    </div>
    ${{sectionsHtml}}
  `;
  document.getElementById('detail-modal').classList.add('open');
}}

function closeModal() {{
  document.getElementById('detail-modal').classList.remove('open');
  if (history.replaceState) {{
    history.replaceState(null, '', window.location.pathname + window.location.search);
  }}
}}
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeModal(); }});

function copyLegalBox(btn) {{
  const box = document.getElementById('active-legal-textarea');
  if (!box) return;
  navigator.clipboard.writeText(box.value);
  const old = btn.innerText;
  btn.innerText = LANG === 'fi' ? '✓ Kopioitu leikepöydälle!' : '✓ Copied to clipboard!';
  setTimeout(() => {{ btn.innerText = old; }}, 2000);
}}

function updateCustomizedLegalText() {{
  const box = document.getElementById('active-legal-textarea');
  if (!box) return;
  const nameEl = document.getElementById('cust-signer-name');
  const orgEl = document.getElementById('cust-signer-org');
  const sName = nameEl ? nameEl.value.trim() : '';
  const sOrg = orgEl ? orgEl.value.trim() : '';
  let txt = ACTIVE_BASE_LEGAL_TEXT;
  if (sName || sOrg) {{
    txt += `\\n\\nALLEKIRJOITUS JA ILMOITTAJAN YHTEYSTIEDOT:\\n${{sName || '[Nimi]'}}${{sOrg ? ' / ' + sOrg : ''}}`;
  }}
  box.value = txt;
  const mailLink = document.getElementById('active-mailto-link');
  if (mailLink && ACTIVE_RECIPIENT_EMAIL) {{
    mailLink.href = `mailto:${{ACTIVE_RECIPIENT_EMAIL}}?subject=${{encodeURIComponent(ACTIVE_SUBJECT)}}&body=${{encodeURIComponent(txt)}}`;
  }}
}}

function renderCustomizerInputs() {{
  const fi = LANG === 'fi';
  return `<div class="customizer-grid">
    <input id="cust-signer-name" type="text" placeholder="${{fi ? 'Oma nimi / allekirjoittaja (valinnainen)' : 'Your Name / Signer (optional)'}}" oninput="updateCustomizedLegalText()" />
    <input id="cust-signer-org" type="text" placeholder="${{fi ? 'Yritys, Y-tunnus tai sähköposti (valinnainen)' : 'Company, Business ID or Email (optional)'}}" oninput="updateCustomizedLegalText()" />
  </div>`;
}}

function openKpiModal(key) {{
  const fi = LANG === 'fi';
  if (key === 'total_spend') {{
    openModalHtml(
      fi ? "Minne julkisen sektorin 38,70 miljardin euron ulkoiset ostot menevät?" : "Where Does Finland's €38.70 Billion in Public Procurement Go?",
      fi ? "Tilastokeskus (S.13: P.2 + D.632) · Valtio, 21 hyvinvointialuetta, HUS ja 308 kuntaa" : "Statistics Finland · State, 21 Wellbeing Counties, HUS, and 308 Municipalities",
      `<div class="modal-section">
        <h4>${{fi ? "Selkokielinen kokonaiskuva" : "Plain-English Overview"}}</h4>
        <p>${{fi
          ? "Suomen julkisyhteisöt käyttävät joka vuosi 38,7 miljardia euroa tavaroiden, IT-järjestelmien, hoivapalveluiden, laboratoriotutkimusten, kuljetusten ja rakennusurakoiden ostamiseen. Tässä tutkimuksessa mallinnetut kolme osa-aluetta osoittavat 844,32 milj. €/v suoran tehostamispotentiaalin (230,99 M€ 15 sidosyksikön ja palvelukeskuksen kilpailuttamisesta + 594,40 M€ P25-yksikkökustannusvertailusta + 18,93 M€ 10 dokumentoidusta MAO/KHO-tapauksesta), ja koko kansalliseen hankintakantaan suhteutettuna 1,1–2,2 mrd. €/v."
          : "Finland's public sector spends €38.7 billion every year purchasing goods, IT systems, healthcare services, and construction. The three empirical modules in this report identify €844.32M/yr in direct efficiency potential (€230.99M across 15 in-house units + €594.40M P25 unit-cost convergence + €18.93M across 10 MAO/KHO rulings), scaling to €1.1B–€2.2B/yr nationwide."}}</p>
      </div>`,
      'kpi-total'
    );
  }} else if (key === 'inhouse_leak') {{
    openModalHtml(
      fi ? "Sidosyksikköjärjestelmä ja Hankintalain 15 § (15 yksikköä = 1,96 mrd. €/v)" : "In-House Governance & Procurement Act § 15 (15 Units = €1.96B/yr)",
      fi ? "KHO 8.10.2025 taltio 2250, MAO:154/2024, MAO:500/2024 & HE 2/2026 vp" : "Supreme Administrative Court KHO 8.10.2025, MAO:154/2024 & Procurement Act § 15",
      `<div class="modal-section">
        <h4>${{fi ? "Mitä KHO 8.10.2025 (T2250) ja MAO:154/2024 linjasivat?" : "What Did KHO 8.10.2025 (T2250) and MAO:154/2024 Rule?"}}</h4>
        <p>${{fi
          ? "Hankintalain 15 §:n mukaan julkinen hankintayksikkö voi tehdä suorahankinnan sidosyksiköltään vain, jos se käyttää yhtiöön tosiasiallista määräysvaltaa samalla tavoin kuin omiin toimipaikkoihinsa. KHO ja MAO vahvistivat, ettei muodollinen pienomistus (esim. 0,04–0,09 %) ilman todellista päätösvaltaa täytä lain edellytyksiä. Tarkastellun 15 yksikön yhteenlaskettu tilinpäätösliikevaihto (2024–2025) on 1 963,40 M€/v ja konservatiivinen KKV/VATT-vertailumallin mukainen tehostamispotentiaali 230,99 M€/v."
          : "Under Procurement Act § 15, a public buyer can make direct awards to an in-house unit only when exercising genuine control over it. KHO and MAO confirmed that nominal minority shareholdings (0.04%–0.09%) without real governance power do not qualify. Total audited turnover across the 15 units is €1,963.40M/yr, with a conservative €230.99M/yr competitive efficiency potential."}}</p>
      </div>`,
      'kpi-inhouse'
    );
  }} else if (key === 'price_spread') {{
    openModalHtml(
      fi ? "Alueelliset yksikkökustannuserot (THL / HALI ry / KKV)" : "Regional Unit-Cost Dispersion (THL / HALI / KKV Benchmarks)",
      fi ? "Viiden keskeisen sote- ja ICT-kategorian P25-vertailu" : "P25 Benchmark Comparison Across 5 Major Healthcare & ICT Categories",
      `<div class="modal-section">
        <h4>${{fi ? "594,40 miljoonan euron säästöpotentiaali edullisimman neljänneksen (P25) kustannustasolla" : "€594.40M Annual Efficiency Potential at the Top-Quartile (P25) Benchmark"}}</h4>
        <p>${{fi
          ? "THL:n ja HALI ry:n julkaisemien yksikkökustannustietojen mukaan saman palvelun (kuten ikäihmisten ympärivuorokautisen palveluasumisen hoitopäivän tai potilastietojärjestelmän) yksikkökustannus vaihtelee merkittävästi alueittain ja oman tuotannon sekä ostopalvelun välillä. Kun yli 25. persentiilin (P25) kustannustason alueet saavuttavat P25-vertailutason, laskennallinen säästöpotentiaali tarkastelluissa 31 vertailupisteessä on 594,40 M€/v."
          : "Published unit-cost statistics from THL and HALI show significant regional dispersion in identical healthcare and ICT services. Converging regions above the 25th percentile (P25) to the P25 benchmark yields €594.40M/yr across the 31 regional comparisons."}}</p>
      </div>`,
      'kpi-spread'
    );
  }} else if (key === 'single_bid') {{
    openModalHtml(
      fi ? "Yhden tarjouksen kilpailutukset (KKV: n. 15–16 %) ja MAO-oikeuskäytäntö" : "Single-Bid Tenders (KKV: ~15–16%) & Market Court Case Law",
      fi ? "10 vahvistettua Finlex / KKV MAO- ja KHO-ratkaisua (2023–2025)" : "10 Verified Finlex / KKV Market Court & Supreme Administrative Court Rulings",
      `<div class="modal-section">
        <h4>${{fi ? "Miten kilpailua voidaan lisätä hankintalain 75 §:n mukaisella osiin jakamisella?" : "How Dividing Contracts Into Lots (§ 75) Increases Competition"}}</h4>
        <p>${{fi
          ? "Kilpailu- ja kuluttajaviraston (KKV) tutkimusten mukaan noin 15–16 prosenttia Suomen julkisista hankinnoista saa vain yhden tarjouksen (yhteensä n. 1,5 mrd. €/v), ja merkittävä osa saa vain 1–2 tarjousta. Kun hankinnat jaetaan hankintalain 75 §:n mukaisesti osakokonaisuuksiin ja soveltuvuusvaatimukset mitoitetaan suhteellisuusperiaatteen (85 §) mukaisesti, useampi pk-yritys pystyy osallistumaan tarjouskilpailuun."
          : "According to the Finnish Competition and Consumer Authority (KKV), roughly 15–16% of Finnish public tenders receive only a single bid (~€1.5B/yr). Dividing large contracts into lots (§ 75) and setting proportionate qualification criteria (§ 85) enables broader SME participation and stronger price competition."}}</p>
      </div>`,
      'kpi-singlebid'
    );
  }}
}}

function openFlowModal(step) {{
  const fi = LANG === 'fi';
  const steps = {{
    1: {{
      t: fi ? "Vaihe 1: Hajautettu pienomistus (<10 %) yhteisessä sidosyksikössä" : "Step 1: Dispersed Minority Shareholding (<10%) in a Joint In-House Company",
      s: fi ? "Muodollinen osakeomistus ilman yksittäisen tilaajan määräysvaltaa" : "Nominal Shareholding Without Individual Governance Control",
      b: fi ? "Kunta tai hyvinvointialue merkitsee pienen osakeosuuden (esim. 0,04 % – 2,5 % osakekannasta) kymmenien tai satojen julkisyhteisöjen yhteisestä yhtiöstä. KHO:n ennakkopäätöksen (8.10.2025 taltio 2250) mukaan pelkkä muodollinen pienomistus ilman todellista päätösvaltaa yhtiön strategisiin tavoitteisiin ei täytä hankintalain 15 §:n edellytyksiä."
            : "A municipality or Wellbeing County holds a small fraction (0.04%–2.5%) of shares in a joint company owned by dozens or hundreds of public authorities. Under KHO 8.10.2025 (T2250), nominal minority ownership without real strategic control does not satisfy Procurement Act § 15."
    }},
    2: {{
      t: fi ? "Vaihe 2: Sidosyksikkösuorahankinta ilman avointa tarjouskilpailua" : "Step 2: Direct In-House Award Without Open Tendering",
      s: fi ? "Hankintalain 15 § ja 10 % vähimmäisomistusraja (HE 2/2026 vp)" : "Procurement Act § 15 and the 10% Minimum Ownership Reform (HE 2/2026 vp)",
      b: fi ? "Sidosyksikköpoikkeukseen vedoten hankintayksikkö tilaa IT-, taloushallinto- tai tukipalvelut suoraan yhtiöltä julkaisematta hankintailmoitusta Hilmassa. Hankintalain uudistus (HE 2/2026 vp) asettaa sidosyksikköomistukselle selkeän 10 prosentin vähimmäisomistusrajan."
            : "Relying on the in-house exemption, the contracting authority orders services directly without publishing an open Hilma tender notice. Finland's procurement law reform (HE 2/2026 vp) establishes a statutory 10% minimum equity threshold."
    }},
    3: {{
      t: fi ? "Vaihe 3: Moniportainen hallintorakenne ja puitesopimusketjut" : "Step 3: Multi-Tier Governance & Framework Subcontracting",
      s: fi ? "Koordinointikustannus ja rajapintojen avoimuus" : "Coordination Overhead and Open Standards",
      b: fi ? "Sidosyksikkö tuottaa osan palveluista itse ja hankkii osan ohjelmistoista, laitteista ja asiantuntijatyöstä kaupallisilta puitesopimustoimittajilta. Kaupalliset toimittajat toimivat täysin laillisesti; rakenteellinen kysymys koskee sitä, milloin suora yhteishankinta (Hansel / oma kilpailutus) on moniportaista sidosyksikkörakennetta kustannustehokkaampi."
            : "The in-house unit produces part of the services internally and procures software, hardware, and specialist work from commercial framework vendors. Commercial vendors act lawfully; the structural question is when direct open tendering is more cost-efficient than a multi-tier in-house structure."
    }},
    4: {{
      t: fi ? "Vaihe 4: Tehostamispotentiaali — 230,99 milj. €/v (15 yksikköä)" : "Step 4: Efficiency Potential — €230.99M/yr Across 15 Units",
      s: fi ? "KKV:n ja VATT:n tutkimuksiin perustuva 11–14 % kilpailupotentiaali" : "11–14% Competitive Benchmark Grounded in KKV & VATT Research",
      b: fi ? "Kun 15 tarkastellun sidosyksikön ja palvelukeskuksen 1 963,40 miljoonan euron vuotuiseen tilinpäätösliikevaihtoon sovelletaan konservatiivista 11–14 % kilpailu- ja koordinointisäästöä, laskennallinen tehostamispotentiaali on 230,99 miljoonaa euroa vuodessa."
            : "Applying a conservative 11–14% competitive and coordination efficiency benchmark across the €1,963.40M/yr audited turnover of the 15 units yields €230.99M/yr in modeled savings."
    }}
  }};
  const item = steps[step];
  openModalHtml(item.t, item.s, `<div class="modal-section"><h4>${{fi ? "Mitä tässä vaiheessa tapahtuu?" : "What Happens in This Step?"}}</h4><p>${{item.b}}</p></div>`, `flow-${{step}}`);
}}

function openInhouseModal(idx) {{
  const f = APP.ssot.inhouse_flows[idx];
  if (!f) return;
  const kkv = APP.kkv_filings[f.inhouse_y_tunnus];
  const oik = APP.oikaisu_filings[f.inhouse_y_tunnus];
  const fi = LANG === 'fi';
  ACTIVE_BASE_LEGAL_TEXT = kkv.body;
  ACTIVE_RECIPIENT_EMAIL = kkv.recipient_email;
  ACTIVE_SUBJECT = kkv.subject;
  const mailtoKkv = `mailto:${{kkv.recipient_email}}?subject=${{encodeURIComponent(kkv.subject)}}&body=${{encodeURIComponent(kkv.body)}}`;
  const mailtoOik = `mailto:${{oik.recipient_email}}?subject=${{encodeURIComponent(oik.subject)}}&body=${{encodeURIComponent(oik.body)}}`;

  openModalHtml(
    `${{f.inhouse_vendor}} (Y-tunnus: ${{f.inhouse_y_tunnus}})`,
    `${{f.buyer_name}} · ${{fi ? "Omistusosuus" : "Buyer Ownership"}}: ${{f.buyer_equity_share_pct}} %`,
    `<div class="modal-section">
      <h4>${{fi ? "Selkokielinen kuvaus järjestelystä" : "Plain-English Explanation of This Arrangement"}}</h4>
      <p>${{fi
        ? `<strong>${{f.buyer_name}}</strong> ostaa yksiköltä <strong>${{f.inhouse_vendor}}</strong> palveluita <strong>${{fmtM(f.annual_spend_m_eur)}}</strong> arvosta vuodessa ilman avointa kilpailutusta (${{f.legal_status}}). Välikäsi perii arviolta <strong>${{f.inhouse_markup_pct}} %</strong> sisäisen katteen ja ketjuttaa työtä suoraan yksityisille suuryrityksille (<strong>${{f.subcontractor_vendor}}</strong>). Avoin kilpailutus säästäisi arviolta <strong>${{fmtM(f.recoverable_saving_m_eur)}}</strong> vuodessa.`
        : `<strong>${{f.buyer_name}}</strong> awards <strong>${{fmtM(f.annual_spend_m_eur)}}/year</strong> without open tenders to <strong>${{f.inhouse_vendor}}</strong> (${{f.buyer_equity_share_pct}}% equity). The intermediary charges an estimated <strong>${{f.inhouse_markup_pct}}%</strong> markup while subcontracting to <strong>${{f.subcontractor_vendor}}</strong>. Open competition would save <strong>${{fmtM(f.recoverable_saving_m_eur)}}/year</strong>.`}}</p>
    </div>
    <div class="modal-section">
      <h4>${{fi ? "Räätälöi ja lataa valmis 0,00 € toimenpidepyyntö (KKV tai oikaisuvaatimus)" : "Customize & Download Ready-to-Send €0.00 Official Complaint (KKV or Rectification)"}}</h4>
      <p>${{fi
        ? "Markkinaoikeuden valitusoikeudenkäynti maksaa 2 440–7 300 €, mutta alla oleva valvontailmoitus KKV:lle (kirjaamo@kkv.fi) tai hankintaoikaisuvaatimus ostajan kirjaamoon on 100 % maksuton (0,00 €). Voit lisätä alle omat tietosi:"
        : "Filing a Market Court appeal costs €2,440–€7,300, but submitting this statutory investigation request to KKV (kirjaamo@kkv.fi) or the buyer's registry costs €0.00. Optionally add your details below:"}}</p>
      ${{renderCustomizerInputs()}}
      <textarea id="active-legal-textarea" class="legal-box">${{kkv.body}}</textarea>
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button class="btn-primary" onclick="copyLegalBox(this)">${{fi ? "📋 Kopioi asiakirja" : "📋 Copy Filing Text"}}</button>
        <button class="btn-secondary" onclick="downloadTextFile('KKV_Toimenpidepyynto_${{f.inhouse_y_tunnus}}.txt', document.getElementById('active-legal-textarea').value)">${{fi ? "⬇ Lataa .txt-asiakirja" : "⬇ Download .txt"}}</button>
        <a id="active-mailto-link" class="btn-secondary" href="${{mailtoKkv}}">${{fi ? "✉️ Avaa sähköpostissa (KKV kirjaamo@kkv.fi)" : "✉️ Open in Email (KKV)"}}</a>
        <a class="btn-secondary" href="${{mailtoOik}}">${{fi ? "✉️ Oikaisuvaatimus ostajalle (" + f.buyer_kirjaamo_email + ")" : "✉️ Send Rectification to Buyer"}}</a>
      </div>
    </div>`,
    `inhouse-${{f.inhouse_y_tunnus}}`
  );
}}

function openArbitrageModal(idx) {{
  const r = APP.ssot.arbitrage_rows[idx];
  if (!r) return;
  const fi = LANG === 'fi';
  const catMeta = CPV_NAMES[r.cpv_category] || {{ fi: r.cpv_category, en: r.cpv_category, unit_fi: r.unit_name, unit_en: r.unit_name }};
  openModalHtml(
    `${{r.entity_name}}`,
    `${{fi ? catMeta.fi : catMeta.en}} · ${{r.kirjaamo_email}}`,
    `<div class="modal-section">
      <h4>${{fi ? "Mistä alueellinen ylihinta syntyy?" : "Why Is This Region Overpaying?"}}</h4>
      <p>${{fi
        ? `<strong>${{r.entity_name}}</strong> maksaa tästä palvelusta <strong>${{Number(r.unit_price_eur).toLocaleString('fi-FI')}} € / ${{catMeta.unit_fi}}</strong> (volyymi ${{Number(r.annual_units).toLocaleString('fi-FI')}} kpl/v = ${{fmtEUR(r.annual_baseline_eur)}}/v), kun Suomen edullisimman neljänneksen (P25-vertailutaso) yksikköhinta samalle palvelulle on <strong>${{Number(r.p25_benchmark_eur).toLocaleString('fi-FI')}} € / ${{catMeta.unit_fi}}</strong> (+${{r.overpay_vs_p25_pct}} % ylihintaa). Jos alue kilpailuttaisi sopimuksen parhaan neljänneksen hintatasolle, veronmaksajat säästäisivät <strong>${{fmtEUR(r.recoverable_saving_eur)}}</strong> joka vuosi.`
        : `<strong>${{r.entity_name}}</strong> pays <strong>€${{Number(r.unit_price_eur).toLocaleString('fi-FI')}} per ${{catMeta.unit_en}}</strong> (annual volume ${{Number(r.annual_units).toLocaleString('fi-FI')}} = ${{fmtEUR(r.annual_baseline_eur)}}/yr), whereas Finland's top-quartile (P25) benchmark price for the exact same service is <strong>€${{Number(r.p25_benchmark_eur).toLocaleString('fi-FI')}}</strong> (+${{r.overpay_vs_p25_pct}}% markup). Matching the P25 benchmark saves <strong>${{fmtEUR(r.recoverable_saving_eur)}}/year</strong>.`}}</p>
    </div>`,
    `arb-${{idx}}`
  );
}}

function openHilmaModal(idx) {{
  const t = APP.ssot.flagged_hilma_tenders[idx];
  if (!t) return;
  const fil = APP.hilma_filings[t.tender_id];
  const fi = LANG === 'fi';
  ACTIVE_BASE_LEGAL_TEXT = fil.body;
  ACTIVE_RECIPIENT_EMAIL = fil.recipient_email;
  ACTIVE_SUBJECT = fil.subject;
  const mailto = `mailto:${{fil.recipient_email}}?subject=${{encodeURIComponent(fil.subject)}}&body=${{encodeURIComponent(fil.body)}}`;

  openModalHtml(
    `${{t.buyer_name}} (${{t.tender_id}})`,
    `${{t.cpv_code}} · ${{fi ? "Saadut tarjoukset" : "Bids Received"}}: ${{t.bids_received}} kpl · ${{fi ? "Valittu toimittaja" : "Incumbent"}}: ${{t.incumbent_vendor}}`,
    `<div class="modal-section">
      <h4>${{fi ? "Miten kilpailutus rajattiin yhdelle tarjoajalle?" : "How Competitors Were Locked Out"}}</h4>
      <p>${{fi
        ? `Tässä <strong>${{fmtEUR(t.contract_value_eur)}}</strong> arvoisessa hankinnassa saatiin vain <strong>${{t.bids_received}} tarjous(ta)</strong>, vaikka Suomessa ja EU:ssa toimii <strong>${{t.qualified_eu_sme_pool_size}} pätevää pk-toimittajaa</strong>. Syy: <em>”${{t.lockout_reason}}”</em>. Kun muut yritykset suljettiin ulos, sopimus meni toimittajalle <strong>${{t.incumbent_vendor}}</strong> ilman todellista hintakilpailua (vuosisäästöpotentiaali avoimessa kilpailussa <strong>${{fmtEUR(t.expected_annual_saving_eur)}}</strong>).`
        : `This <strong>${{fmtEUR(t.contract_value_eur)}}</strong> procurement received only <strong>${{t.bids_received}} bid(s)</strong> despite <strong>${{t.qualified_eu_sme_pool_size}} qualified SMEs</strong> in the market, due to: <em>"${{t.lockout_reason}}"</em>. Opening the tender saves an estimated <strong>${{fmtEUR(t.expected_annual_saving_eur)}}/year</strong>.`}}</p>
    </div>
    <div class="modal-section">
      <h4>${{fi ? "Räätälöi ja lataa 0,00 € vaatimus syrjivän tarjousehdon poistamiseksi (Hankintalaki 67 § & 75 §)" : "Customize & Download €0.00 Demand to Remove Tailored Spec (Procurement Act § 67 & § 75)"}}</h4>
      ${{renderCustomizerInputs()}}
      <textarea id="active-legal-textarea" class="legal-box">${{fil.body}}</textarea>
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button class="btn-primary" onclick="copyLegalBox(this)">${{fi ? "📋 Kopioi vaatimus" : "📋 Copy Challenge Text"}}</button>
        <button class="btn-secondary" onclick="downloadTextFile('Hankintaoikaisu_${{idx + 1}}.txt', document.getElementById('active-legal-textarea').value)">${{fi ? "⬇ Lataa .txt-asiakirja" : "⬇ Download .txt"}}</button>
        <a id="active-mailto-link" class="btn-secondary" href="${{mailto}}">${{fi ? "✉️ Lähetä hankintayksikölle (" + fil.recipient_email + ")" : "✉️ Send via Email"}}</a>
      </div>
    </div>`,
    `tender-${{idx}}`
  );
}}

function openBuyerFoiaModal(idx) {{
  const b = APP.ssot.public_buyer_directory[idx];
  if (!b) return;
  const fil = APP.foia_filings[b.y_tunnus];
  const fi = LANG === 'fi';
  ACTIVE_BASE_LEGAL_TEXT = fil.body;
  ACTIVE_RECIPIENT_EMAIL = fil.recipient_email;
  ACTIVE_SUBJECT = fil.subject;
  const mailto = `mailto:${{fil.recipient_email}}?subject=${{encodeURIComponent(fil.subject)}}&body=${{encodeURIComponent(fil.body)}}`;

  openModalHtml(
    `${{b.entity_name}} (Y-tunnus: ${{b.y_tunnus}})`,
    `${{fi ? "Julkisuuslain (621/1999) 13 § ja 16.3 § mukainen tietopyyntö" : "Statutory Freedom of Information Request (Act 621/1999)"}} · ${{b.kirjaamo_email}}`,
    `<div class="modal-section">
      <h4>${{fi ? "Mitä tämä asiakirja velvoittaa viranomaisen tekemään?" : "What Does This Request Require the Authority to Do?"}}</h4>
      <p>${{fi
        ? `Tämä valmis tietopyyntö velvoittaa viranomaisen (<strong>${{b.entity_name}}</strong>, vuosiostot <strong>${{fmtM(b.annual_purchases_m_eur)}}</strong>, keskeiset sidosyksiköt: <em>${{b.primary_inhouse_shells}}</em>) luovuttamaan 14 vuorokauden kuluessa koneluettavan ostolaskuaineiston (CSV/XLSX) sekä sidosyksikköjen osakassopimukset ja suorahankintapäätökset maksutta.`
        : `This statutory request requires <strong>${{b.entity_name}}</strong> (annual purchases <strong>${{fmtM(b.annual_purchases_m_eur)}}</strong>, primary in-house shells: <em>${{b.primary_inhouse_shells}}</em>) to release machine-readable purchase invoice ledgers (CSV/XLSX) and in-house shareholder agreements within 14 days at zero cost.`}}</p>
      ${{renderCustomizerInputs()}}
      <textarea id="active-legal-textarea" class="legal-box">${{fil.body}}</textarea>
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button class="btn-primary" onclick="copyLegalBox(this)">${{fi ? "📋 Kopioi tietopyyntö" : "📋 Copy FOIA Request"}}</button>
        <button class="btn-secondary" onclick="downloadTextFile('Tietopyynto_${{b.y_tunnus}}.txt', document.getElementById('active-legal-textarea').value)">${{fi ? "⬇ Lataa .txt-asiakirja" : "⬇ Download .txt"}}</button>
        <a id="active-mailto-link" class="btn-secondary" href="${{mailto}}">${{fi ? "✉️ Avaa sähköpostissa (" + b.kirjaamo_email + ")" : "✉️ Open in Email"}}</a>
      </div>
    </div>`,
    `buyer-${{b.y_tunnus}}`
  );
}}

function sortInhouse(col) {{
  if (INHOUSE_SORT.col === col) {{
    INHOUSE_SORT.asc = !INHOUSE_SORT.asc;
  }} else {{
    INHOUSE_SORT.col = col;
    INHOUSE_SORT.asc = (col === 'inhouse_vendor' || col === 'buyer_name');
  }}
  renderAll();
}}

function sortBuyers(col) {{
  if (BUYER_SORT.col === col) {{
    BUYER_SORT.asc = !BUYER_SORT.asc;
  }} else {{
    BUYER_SORT.col = col;
    BUYER_SORT.asc = (col === 'entity_name' || col === 'entity_type');
  }}
  renderAll();
}}

function exportInhouseCsv() {{
  const headers = ['Sija', 'Sidosyksikko', 'Y_tunnus', 'Tilaajat', 'Omistus_Pct', 'Suoraostot_M_EUR_v', 'Valikasikate_Pct', 'Alihankintapreemio_Pct', 'Vuosisaasto_M_EUR_v', 'Alihankkijat', 'Kirjaamo'];
  const lines = [headers.join(';')];
  LAST_INHOUSE.forEach((f, idx) => {{
    lines.push([
      idx + 1,
      `"${{String(f.inhouse_vendor).replace(/"/g, '""')}}"`,
      `"${{f.inhouse_y_tunnus}}"`,
      `"${{String(f.buyer_name).replace(/"/g, '""')}}"`,
      f.buyer_equity_share_pct,
      f.annual_spend_m_eur,
      f.inhouse_markup_pct,
      f.subcontractor_uncompeted_premium_pct,
      f.recoverable_saving_m_eur,
      `"${{String(f.subcontractor_vendor).replace(/"/g, '""')}}"`,
      `"${{f.buyer_kirjaamo_email}}"`
    ].join(';'));
  }});
  const blob = new Blob(['\\uFEFF' + lines.join('\\r\\n')], {{ type: 'text/csv;charset=utf-8;' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'STI_Sidosyksikot_15_kpl_2026.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}}

function exportBuyersCsv() {{
  const headers = ['Sija', 'Hankintayksikko', 'Tyyppi', 'Y_tunnus', 'Kirjaamo', 'Ulkoiset_ostot_M_EUR_v', 'Avoin_ostolaskudata', 'Sidosyksikot'];
  const lines = [headers.join(';')];
  LAST_BUYERS.forEach((b, idx) => {{
    lines.push([
      idx + 1,
      `"${{String(b.entity_name).replace(/"/g, '""')}}"`,
      `"${{b.entity_type}}"`,
      `"${{b.y_tunnus}}"`,
      `"${{b.kirjaamo_email}}"`,
      b.annual_purchases_m_eur,
      b.publishes_open_invoices ? 'KYLLA' : 'EI',
      `"${{String(b.primary_inhouse_shells).replace(/"/g, '""')}}"`
    ].join(';'));
  }});
  const blob = new Blob(['\\uFEFF' + lines.join('\\r\\n')], {{ type: 'text/csv;charset=utf-8;' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'STI_Kaikki_43_Julkista_Ostajaa_2026.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}}

function setSearch(val) {{
  const box = document.getElementById('search-box');
  box.value = val;
  document.querySelectorAll('.chip').forEach(btn => {{
    const txt = btn.textContent.trim().toLowerCase();
    btn.classList.toggle('active', (val === '' && (txt.includes('kaikki') || txt.includes('all'))) || (val !== '' && txt.includes(val.toLowerCase())));
  }});
  renderAll();
}}

function setLang(l) {{
  LANG = l;
  document.getElementById('btn-fi').classList.toggle('active', l === 'fi');
  document.getElementById('btn-en').classList.toggle('active', l === 'en');
  document.querySelectorAll('[data-i18n]').forEach(el => {{
    const k = el.getAttribute('data-i18n');
    if (I18N[l][k]) el.innerHTML = I18N[l][k];
  }});
  renderAll();
}}

function renderAll() {{
  const rawQ = (document.getElementById('search-box').value || '').trim();
  const safeQ = escHtml(rawQ);
  const q = rawQ.toLowerCase();
  const fi = LANG === 'fi';

  // 1. In-house cards & sortable table
  const filteredInhouse = APP.ssot.inhouse_flows.map((f, origIdx) => ({{ ...f, origIdx }})).filter(f => {{
    const txt = `${{f.inhouse_vendor}} ${{f.inhouse_y_tunnus}} ${{f.buyer_name}} ${{f.subcontractor_vendor}} ${{f.legal_status}}`.toLowerCase();
    return !q || txt.includes(q);
  }});

  let inHtml = '';
  filteredInhouse.forEach(f => {{
    const isToken = f.is_illegal_under_10pct;
    const eqStr = Number(f.buyer_equity_share_pct).toLocaleString('fi-FI');
    const accent = isToken ? 'red-accent' : 'amber-accent';
    const badge = isToken
      ? `<span class="badge badge-red">${{fi ? 'Pienosakkaat ' + eqStr + ' % (<10 %)' : 'Minority Share ' + eqStr + '%'}}</span>`
      : `<span class="badge badge-amber">${{fi ? 'Enemmistö / Lakisääteinen' : 'Majority / Statutory'}}</span>`;
    const inComment = isToken
      ? (fi
          ? `${{f.legal_status}}`
          : `Audited turnover ${{fmtCardM(f.annual_spend_m_eur)}}/yr · Minority shareholder ref. ${{eqStr}}%. Framework categories: ${{f.subcontractor_vendor}}.`)
      : (fi
          ? `${{f.legal_status}}`
          : `Audited turnover ${{fmtCardM(f.annual_spend_m_eur)}}/yr (${{eqStr}}% ref. share). Framework categories: ${{f.subcontractor_vendor}}.`);
    inHtml += `<div class="story-card ${{accent}} clickable-card" onclick="openInhouseModal(${{f.origIdx}})">
      <div class="story-top">
        <div class="card-kicker-row">
          ${{badge}}
          <span class="card-id-pill">Y: ${{f.inhouse_y_tunnus}}</span>
        </div>
        <h3>${{f.inhouse_vendor}}</h3>
        <div class="story-subtitle">${{fi ? 'Omistajat / tilaajat:' : 'Owners / Buyers:'}} ${{f.buyer_name}}</div>
        <p class="story-commentary">${{inComment}}</p>
      </div>
      <div>
        <div class="metrics-strip">
          <div><span>${{fi ? 'Liikevaihto / v' : 'Turnover / yr'}}</span><strong>${{fmtCardM(f.annual_spend_m_eur)}}</strong></div>
          <div><span>${{fi ? 'Koordinointi' : 'Coordination'}}</span><strong style="color:var(--amber)">${{f.inhouse_markup_pct}} %</strong></div>
          <div><span>${{fi ? 'Säästöpotentiaali' : 'Efficiency Pot.'}}</span><strong style="color:var(--red)">-${{fmtCardM(f.recoverable_saving_m_eur)}}</strong></div>
        </div>
        <div class="click-hint">${{fi ? 'Klikkaa: Tilinpäätöstiedot & 0 € KKV-selvityspyyntö →' : 'Click: Financial data & €0 KKV review request →'}}</div>
      </div>
    </div>`;
  }});
  if (!inHtml) {{
    inHtml = `<div class="empty-box"><span>${{fi ? `Ei sidosyksikköosumia haulle ”${{safeQ}}”. Katso osiot 2–4 alla.` : `No in-house matches for "${{safeQ}}". Check Sections 2–4 below.`}}</span><button type="button" class="btn-secondary" onclick="setSearch('')">${{fi ? 'Näytä kaikki' : 'Show all'}}</button></div>`;
  }}
  document.getElementById('inhouse-cards').innerHTML = inHtml;

  const sortedInhouse = [...filteredInhouse].sort((a, b) => {{
    const va = a[INHOUSE_SORT.col];
    const vb = b[INHOUSE_SORT.col];
    let cmp = (typeof va === 'number' && typeof vb === 'number') ? (va - vb) : String(va || '').localeCompare(String(vb || ''), 'fi');
    return INHOUSE_SORT.asc ? cmp : -cmp;
  }});
  LAST_INHOUSE = sortedInhouse;
  ['inhouse_vendor', 'buyer_name', 'buyer_equity_share_pct', 'annual_spend_m_eur', 'inhouse_markup_pct', 'recoverable_saving_m_eur'].forEach(col => {{
    const el = document.getElementById('sort-ih-' + col);
    if (el) el.textContent = INHOUSE_SORT.col === col ? (INHOUSE_SORT.asc ? '▲' : '▼') : '';
  }});
  const sumIhSpend = sortedInhouse.length === APP.ssot.inhouse_flows.length ? APP.ssot.inhouse_summary.total_inhouse_spend_m_eur : sortedInhouse.reduce((a, b) => a + b.annual_spend_m_eur, 0);
  const sumIhSave = sortedInhouse.length === APP.ssot.inhouse_flows.length ? APP.ssot.inhouse_summary.recoverable_annual_saving_m_eur : sortedInhouse.reduce((a, b) => a + b.recoverable_saving_m_eur, 0);
  document.getElementById('inhouse-count-sub').textContent = fi
    ? `Näytetään ${{sortedInhouse.length}} / 15 sidosyksikköä · Suoraostot yht. ${{fmtM(sumIhSpend)}} · Vuosisäästö yht. ${{fmtM(sumIhSave)}}`
    : `Showing ${{sortedInhouse.length}} / 15 in-house intermediaries · Direct spend ${{fmtM(sumIhSpend)}} · Annual saving ${{fmtM(sumIhSave)}}`;
  document.getElementById('inhouse-tbody').innerHTML = sortedInhouse.map((f, i) => `
    <tr class="clickable-row" onclick="openInhouseModal(${{f.origIdx}})">
      <td>${{i + 1}}</td>
      <td><strong>${{escHtml(f.inhouse_vendor)}}</strong><br/><span style="font-size:11.5px;color:var(--muted);">Y: ${{f.inhouse_y_tunnus}}</span></td>
      <td>${{escHtml(f.buyer_name)}}</td>
      <td><span class="badge ${{f.is_illegal_under_10pct ? 'badge-red' : 'badge-amber'}}">${{Number(f.buyer_equity_share_pct).toLocaleString('fi-FI')}} %</span></td>
      <td><strong>${{fmtM(f.annual_spend_m_eur)}}</strong></td>
      <td>${{f.inhouse_markup_pct}} %</td>
      <td style="color:var(--red);font-weight:700;">-${{fmtM(f.recoverable_saving_m_eur)}}</td>
    </tr>
  `).join('');

  // 2. Arbitrage cards (show rows where overpay_vs_p25_pct > 0)
  let arbMatches = 0;
  let arbHtml = '';
  APP.ssot.arbitrage_rows.forEach((r, idx) => {{
    if (r.overpay_vs_p25_pct <= 0) return;
    const catMeta = CPV_NAMES[r.cpv_category] || {{ fi: r.cpv_category, en: r.cpv_category, unit_fi: r.unit_name, unit_en: r.unit_name }};
    const txt = `${{r.entity_name}} ${{r.cpv_category}} ${{catMeta.fi}} ${{catMeta.en}}`.toLowerCase();
    if (q && !txt.includes(q)) return;
    arbMatches++;
    const unitLbl = fi ? catMeta.unit_fi : catMeta.unit_en;
    arbHtml += `<div class="story-card amber-accent clickable-card" onclick="openArbitrageModal(${{idx}})">
      <div class="story-top">
        <div class="card-kicker-row">
          <span class="badge badge-red">+${{r.overpay_vs_p25_pct}} % ${{fi ? 'ylihinta' : 'markup'}}</span>
          <span class="card-id-pill">${{r.cpv_category.split('-')[0]}}</span>
        </div>
        <h3>${{r.entity_name}}</h3>
        <div class="story-subtitle">${{fi ? catMeta.fi : catMeta.en}}</div>
        <p class="story-commentary">${{fi
          ? `Maksaa ${{Number(r.unit_price_eur).toLocaleString('fi-FI')}} € / ${{unitLbl}}, kun Suomen edullisimman neljänneksen (P25) vertailuhinta on ${{Number(r.p25_benchmark_eur).toLocaleString('fi-FI')}} €.`
          : `Pays €${{Number(r.unit_price_eur).toLocaleString('fi-FI')}} per ${{unitLbl}} vs. top-quartile (P25) benchmark of €${{Number(r.p25_benchmark_eur).toLocaleString('fi-FI')}}.`}}</p>
      </div>
      <div>
        <div class="metrics-strip">
          <div><span>${{fi ? 'Alueen hinta' : 'Unit Price'}}</span><strong style="color:var(--red)">${{Number(r.unit_price_eur).toLocaleString('fi-FI')}} €</strong></div>
          <div><span>${{fi ? 'P25-vertailu' : 'P25 Benchmark'}}</span><strong style="color:var(--accent-dark)">${{Number(r.p25_benchmark_eur).toLocaleString('fi-FI')}} €</strong></div>
          <div><span>${{fi ? 'Säästö / v' : 'Saving / yr'}}</span><strong style="color:var(--red)">-${{fmtCardM(r.recoverable_saving_eur / 1e6)}}</strong></div>
        </div>
        <div class="click-hint">${{fi ? 'Klikkaa: Yksikköhintojen erittely →' : 'Click: Inspect unit-price breakdown →'}}</div>
      </div>
    </div>`;
  }});
  if (!arbHtml) {{
    arbHtml = `<div class="empty-box"><span>${{fi ? `Ei hintavertailuosumia haulle ”${{safeQ}}”.` : `No price benchmark matches for "${{safeQ}}".`}}</span><button type="button" class="btn-secondary" onclick="setSearch('')">${{fi ? 'Näytä kaikki' : 'Show all'}}</button></div>`;
  }}
  document.getElementById('arbitrage-cards').innerHTML = arbHtml;

  // 3. Hilma single-bid cards
  let hilmaMatches = 0;
  let hilmaHtml = '';
  APP.ssot.flagged_hilma_tenders.forEach((t, idx) => {{
    const txt = `${{t.buyer_name}} ${{t.tender_id}} ${{t.cpv_code}} ${{t.incumbent_vendor}} ${{t.lockout_reason}}`.toLowerCase();
    if (q && !txt.includes(q)) return;
    hilmaMatches++;
    const bidBadge = t.is_direct_award
      ? `<span class="badge badge-red">${{fi ? '0 tarjousta (Suorahankinta)' : '0 Bids (Direct Award)'}}</span>`
      : `<span class="badge badge-red">${{t.bids_received}} ${{fi ? 'tarjous(ta)' : 'bid(s)'}}</span>`;
    hilmaHtml += `<div class="story-card red-accent clickable-card" onclick="openHilmaModal(${{idx}})">
      <div class="story-top">
        <div class="card-kicker-row">
          ${{bidBadge}}
          <span class="card-id-pill">${{t.tender_id}}</span>
        </div>
        <h3>${{t.buyer_name}}</h3>
        <div class="story-subtitle">${{t.incumbent_vendor}}</div>
        <p class="story-commentary">${{t.lockout_reason}}</p>
      </div>
      <div>
        <div class="metrics-strip">
          <div><span>${{fi ? 'Sopimusarvo' : 'Contract Value'}}</span><strong>${{fmtCardM(t.contract_value_eur / 1e6)}}</strong></div>
          <div><span>${{fi ? 'Estetyt PK:t' : 'Locked SMEs'}}</span><strong>${{t.qualified_eu_sme_pool_size}} kpl</strong></div>
          <div><span>${{fi ? 'Säästö / v' : 'Est. Saving'}}</span><strong style="color:var(--red)">-${{fmtCardM(t.expected_annual_saving_eur / 1e6)}}</strong></div>
        </div>
        <div class="click-hint">${{fi ? 'Klikkaa: 0 € vaatimus tarjousehdon poistamiseksi →' : 'Click: Open €0 tender spec challenge →'}}</div>
      </div>
    </div>`;
  }});
  if (!hilmaHtml) {{
    hilmaHtml = `<div class="empty-box"><span>${{fi ? `Ei MAO/Hilma-kilpailutusosumia haulle ”${{safeQ}}”.` : `No MAO/Hilma tender matches for "${{safeQ}}".`}}</span><button type="button" class="btn-secondary" onclick="setSearch('')">${{fi ? 'Näytä kaikki' : 'Show all'}}</button></div>`;
  }}
  document.getElementById('hilma-cards').innerHTML = hilmaHtml;

  // 4. Buyer FOIA directory cards & sortable table (All 43 Public Buyers)
  const filteredBuyers = APP.ssot.public_buyer_directory.map((b, origIdx) => ({{ ...b, origIdx }})).filter(b => {{
    const txt = `${{b.entity_name}} ${{b.y_tunnus}} ${{b.entity_type}} ${{b.kirjaamo_email}} ${{b.primary_inhouse_shells}}`.toLowerCase();
    return !q || txt.includes(q);
  }});

  let buyerHtml = '';
  filteredBuyers.forEach(b => {{
    buyerHtml += `<div class="story-card green-accent clickable-card" onclick="openBuyerFoiaModal(${{b.origIdx}})">
      <div class="story-top">
        <div class="card-kicker-row">
          <span class="badge badge-green">0,00 € FOIA · Julkisuuslaki</span>
          <span class="card-id-pill">Y: ${{b.y_tunnus}}</span>
        </div>
        <h3>${{b.entity_name}}</h3>
        <div class="story-subtitle">${{fi ? 'Sidosyksiköt:' : 'In-House Shells:'}} ${{b.primary_inhouse_shells}}</div>
        <p class="story-commentary">${{fi
          ? `Vuosiostot ${{fmtCardM(b.annual_purchases_m_eur)}} · Vaadi ostolaskut (CSV/XLSX) ja suorahankintasopimukset julkisuuslain 13 §:n nojalla.`
          : `Annual spend ${{fmtCardM(b.annual_purchases_m_eur)}} · Demand machine-readable purchase invoices (CSV/XLSX) within 14 days.`}}</p>
      </div>
      <div>
        <div class="metrics-strip">
          <div><span>${{fi ? 'Ulkoiset ostot' : 'Annual Spend'}}</span><strong>${{fmtCardM(b.annual_purchases_m_eur)}}</strong></div>
          <div><span>${{fi ? 'Avoin ostodata' : 'Open Ledger'}}</span><strong style="color:${{b.publishes_open_invoices ? 'var(--accent-dark)' : 'var(--amber)'}}">${{b.publishes_open_invoices ? (fi ? 'Julkaistu' : 'Published') : (fi ? 'Vain pyynnöstä' : 'By Request')}}</strong></div>
          <div><span>${{fi ? 'Vastausaika' : 'Statutory SLA'}}</span><strong>14 vrk</strong></div>
        </div>
        <div class="click-hint">${{fi ? 'Klikkaa: Valmis tietopyyntö (' + b.kirjaamo_email + ') →' : 'Click: Ready-to-send FOIA request →'}}</div>
      </div>
    </div>`;
  }});
  if (!buyerHtml) {{
    buyerHtml = `<div class="empty-box"><span>${{fi ? `Ei kirjaamo-osumia haulle ”${{safeQ}}”.` : `No public buyer matches for "${{safeQ}}".`}}</span><button type="button" class="btn-secondary" onclick="setSearch('')">${{fi ? 'Näytä kaikki' : 'Show all'}}</button></div>`;
  }}
  document.getElementById('buyer-cards').innerHTML = buyerHtml;

  const sortedBuyers = [...filteredBuyers].sort((a, b) => {{
    const va = a[BUYER_SORT.col];
    const vb = b[BUYER_SORT.col];
    let cmp = 0;
    if (typeof va === 'number' && typeof vb === 'number') cmp = va - vb;
    else if (typeof va === 'boolean' && typeof vb === 'boolean') cmp = (va === vb) ? 0 : (va ? 1 : -1);
    else cmp = String(va || '').localeCompare(String(vb || ''), 'fi');
    return BUYER_SORT.asc ? cmp : -cmp;
  }});
  LAST_BUYERS = sortedBuyers;
  ['entity_name', 'entity_type', 'annual_purchases_m_eur', 'publishes_open_invoices'].forEach(col => {{
    const el = document.getElementById('sort-b-' + col);
    if (el) el.textContent = BUYER_SORT.col === col ? (BUYER_SORT.asc ? '▲' : '▼') : '';
  }});
  const sumBuyerSpend = sortedBuyers.reduce((a, b) => a + b.annual_purchases_m_eur, 0);
  document.getElementById('buyer-count-sub').textContent = fi
    ? `Näytetään ${{sortedBuyers.length}} / 43 viranomaista · Ulkoiset vuosiostot yht. ${{fmtM(sumBuyerSpend)}}`
    : `Showing ${{sortedBuyers.length}} / 43 public authorities · Total external spend ${{fmtM(sumBuyerSpend)}}`;
  document.getElementById('buyer-tbody').innerHTML = sortedBuyers.map((b, i) => `
    <tr class="clickable-row" onclick="openBuyerFoiaModal(${{b.origIdx}})">
      <td>${{i + 1}}</td>
      <td><strong>${{escHtml(b.entity_name)}}</strong><br/><span style="font-size:11.5px;color:var(--muted);">Y: ${{b.y_tunnus}}</span></td>
      <td><span class="badge ${{b.entity_type === 'Kunta' ? 'badge-green' : 'badge-amber'}}">${{b.entity_type}}</span></td>
      <td><strong>${{fmtM(b.annual_purchases_m_eur)}}</strong></td>
      <td><span class="badge ${{b.publishes_open_invoices ? 'badge-green' : 'badge-red'}}">${{b.publishes_open_invoices ? (fi ? 'Julkaistu' : 'Published') : (fi ? 'Vain pyynnöstä' : 'By Request')}}</span></td>
      <td style="font-size:12.5px;">${{escHtml(b.primary_inhouse_shells)}}<br/><span style="color:var(--accent-dark);font-weight:600;">${{b.kirjaamo_email}}</span></td>
    </tr>
  `).join('');

  // Update Search Status Banner
  const statusEl = document.getElementById('search-status');
  if (q) {{
    statusEl.style.display = 'block';
    statusEl.innerHTML = fi
      ? `Hakutulokset haulle <strong>”${{safeQ}}”</strong>: <strong>${{filteredInhouse.length}}</strong> sidosyksikköä (Osio 1), <strong>${{arbMatches}}</strong> hintavertailua (Osio 2), <strong>${{hilmaMatches}}</strong> MAO/Hilma-tapausta (Osio 3) ja <strong>${{filteredBuyers.length}}</strong> kirjaamoa (Osio 4). <a href="javascript:void(0)" onclick="setSearch('')" style="color:var(--accent-dark);margin-left:10px;">✕ Tyhjennä haku</a>`
      : `Search results for <strong>"${{safeQ}}"</strong>: <strong>${{filteredInhouse.length}}</strong> in-house flows (Sec 1), <strong>${{arbMatches}}</strong> price benchmarks (Sec 2), <strong>${{hilmaMatches}}</strong> MAO/Hilma cases (Sec 3), and <strong>${{filteredBuyers.length}}</strong> buyer registries (Sec 4). <a href="javascript:void(0)" onclick="setSearch('')" style="color:var(--accent-dark);margin-left:10px;">✕ Clear search</a>`;
  }} else {{
    statusEl.style.display = 'none';
  }}
}}

function handleHashRoute() {{
  const h = (window.location.hash || '').replace(/^#/, '');
  if (!h) return;
  if (h.startsWith('inhouse-')) {{
    const yid = h.slice(8);
    const idx = APP.ssot.inhouse_flows.findIndex(f => f.inhouse_y_tunnus === yid);
    if (idx !== -1) openInhouseModal(idx);
  }} else if (h.startsWith('buyer-')) {{
    const yid = h.slice(6);
    const idx = APP.ssot.public_buyer_directory.findIndex(b => b.y_tunnus === yid);
    if (idx !== -1) openBuyerFoiaModal(idx);
  }} else if (h.startsWith('tender-')) {{
    const tidx = parseInt(h.slice(7), 10);
    if (!isNaN(tidx)) openHilmaModal(tidx);
  }} else if (h.startsWith('arb-')) {{
    const aidx = parseInt(h.slice(4), 10);
    if (!isNaN(aidx)) openArbitrageModal(aidx);
  }} else if (h.startsWith('q=')) {{
    setSearch(decodeURIComponent(h.slice(2)));
  }}
}}

document.getElementById('search-box').addEventListener('input', renderAll);
window.addEventListener('hashchange', handleHashRoute);
renderAll();
handleHashRoute();
</script>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path
