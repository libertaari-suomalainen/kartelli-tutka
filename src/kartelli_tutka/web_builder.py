"""
Kartelli-Tutka — Suomen Talousinstituutti (STI) Editorial Research Report & Interactive Case Explorer.
Compiles the canonical SSOT payload and pre-generated legal filings into a self-contained,
mobile-first editorial web application (`dist/index.html`) where every KPI, flow step,
in-house company, regional price comparison, and tender card is clickable.
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
  .hero-lead {{ font-size: clamp(16px, 2vw, 18px); color: var(--body); max-width: 880px; margin-bottom: 22px; }}
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
  .section-head p {{ font-size: 15.5px; color: var(--muted); max-width: 840px; }}
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
    max-width: 760px;
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
  .modal-sub {{ font-size: 14px; color: var(--muted); margin-bottom: 20px; }}
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
  @media (max-width: 960px) {{
    .topbar {{ position: relative; }}
    .topbar-inner {{ flex-wrap: wrap; }}
    .nav-actions {{ width: 100%; justify-content: flex-start; flex-wrap: wrap; }}
    .flow-steps {{ grid-template-columns: minmax(0, 1fr); }}
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
    .kpi-grid, .cards-grid, .flow-steps {{ grid-template-columns: minmax(0, 1fr); }}
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
        <span data-i18n="brand_sub">Tutkimusraportti 2026 · Sidosyksiköt, alueelliset ylihinnat &amp; 0 € viranomaisilmoitukset</span>
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
    <h1 class="hero-title" data-i18n="hero_title">38,7 miljardin euron ostokartelli: Miksi kuntien ja hyvinvointialueiden rahat eivät riitä hoitajiin?</h1>
    <p class="hero-lead" data-i18n="hero_lead">
      Valtio, 21 hyvinvointialuetta ja 308 kuntaa ostavat ulkopuolisilta yrityksiltä IT-järjestelmiä, hoivapalveluita ja urakoita <strong>38,7 miljardilla eurolla vuodessa</strong>. Tutkimuksemme osoittaa, että tästä potista <strong>1,26–3,5 miljardia euroa vuodessa</strong> (tämän aineiston suoraan mallinnetut säästöt <strong>1,26 mrd. €/v</strong>, koko 38,7 mrd. € hankintakantaan skaalattuna <strong>2,86–3,5 mrd. €/v</strong>) hupenee laittomiin ”in-house”-välikäsiin, 2–3-kertaisiin alueellisiin ylihintoihin ja 1–2 tarjouksen näennäiskilpailutuksiin.
    </p>
    <div class="callout-stone">
      <h3 data-i18n="summary_box_title">Miten luet tätä julkaisua? (Kaikki kortit ovat klikattavia)</h3>
      <p data-i18n="summary_box_body">
        <strong>Klikkaa mitä tahansa lukukorttia, IT-/talousyhtiötä (Istekki, Apotti, Sarastia, 2M-IT, Monetra, Tiera, Valtori), alueellista hintavertailua tai Hilma-kilpailutusta</strong>. Saat esiin selkokielisen selityksen sekä valmiin, maksuttoman (0 €) viranomaisilmoituksen Kilpailu- ja kuluttajavirastolle (KKV) tai hyvinvointialueen kirjaamoon.
      </p>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card clickable-card" onclick="openKpiModal('total_spend')">
        <div>
          <div class="kpi-label" data-i18n="kpi1_lbl">Julkiset ulkoiset ostot</div>
          <div class="kpi-val">38,70 mrd. €/v</div>
          <div class="kpi-sub" data-i18n="kpi1_sub">Valtion, hyvinvointialueiden ja kuntien vuotuiset ostot yrityksiltä</div>
        </div>
        <div class="click-hint" data-i18n="click_1">Klikkaa: Minne 38,7 mrd. € menee? →</div>
      </div>

      <div class="kpi-card clickable-card" onclick="openKpiModal('inhouse_leak')">
        <div>
          <div class="kpi-label" data-i18n="kpi2_lbl">Sidosyksikkö- eli ”in-house”-ketjutus</div>
          <div class="kpi-val red">1,42 mrd. €/v</div>
          <div class="kpi-sub" data-i18n="kpi2_sub">7 välikäsiyhtiötä (Istekki, Apotti, Sarastia, 2M-IT, Monetra, Tiera, Valtori) ilman kilpailutusta</div>
        </div>
        <div class="click-hint" data-i18n="click_2">Klikkaa: Mikä on 0,04 % ”kuoriosake”? →</div>
      </div>

      <div class="kpi-card clickable-card" onclick="openKpiModal('price_spread')">
        <div>
          <div class="kpi-label" data-i18n="kpi3_lbl">Alueiden välinen 2–3x ylihinta</div>
          <div class="kpi-val green">711,23 milj. €/v</div>
          <div class="kpi-sub" data-i18n="kpi3_sub">Vuosisäästö, kun kalleimmat alueet laskevat yksikköhinnat parhaan neljänneksen tasolle</div>
        </div>
        <div class="click-hint" data-i18n="click_3">Klikkaa: Miksi sama palvelu maksaa 3x? →</div>
      </div>

      <div class="kpi-card clickable-card" onclick="openKpiModal('single_bid')">
        <div>
          <div class="kpi-label" data-i18n="kpi4_lbl">1–2 tarjouksen kilpailutukset</div>
          <div class="kpi-val red">45 % hankinnoista</div>
          <div class="kpi-sub" data-i18n="kpi4_sub">Räätälöidyt tarjousehdot sulkevat pk-yritykset ulos (n. 25 % vain 1 tarjous) ja nostavat hintoja 15–30 %</div>
        </div>
        <div class="click-hint" data-i18n="click_4">Klikkaa: Miten ehdot räätälöidään? →</div>
      </div>
    </div>
  </section>

  <!-- GLOBAL SEARCH & QUICK FILTERS -->
  <section class="search-hub" id="haku">
    <div>
      <label for="search-box" data-i18n="lbl_search">Hae sidosyksikköä, hyvinvointialuetta, kuntaa, toimittajaa tai palvelua</label>
      <input id="search-box" type="search" class="input-box" placeholder="Kokeile esim. Istekki, Apotti, Sarastia, 2M-IT, Tiera, HUS, Pirha, Varha, Lapha, Tieto, CGI, Mehiläinen..." />
    </div>
    <div class="quick-chips">
      <span class="chip-label" data-i18n="chip_lbl">Pikavalinnat:</span>
      <button type="button" class="chip active" onclick="setSearch('')" data-i18n="chip_all">Näytä kaikki</button>
      <button type="button" class="chip" onclick="setSearch('Istekki')">Istekki Oy</button>
      <button type="button" class="chip" onclick="setSearch('Apotti')">Oy Apotti Ab</button>
      <button type="button" class="chip" onclick="setSearch('Sarastia')">Sarastia / Numera</button>
      <button type="button" class="chip" onclick="setSearch('2M-IT')">2M-IT Oy</button>
      <button type="button" class="chip" onclick="setSearch('Tiera')">Kuntien Tiera</button>
      <button type="button" class="chip" onclick="setSearch('Pirha')">Pirha (Pirkanmaa)</button>
      <button type="button" class="chip" onclick="setSearch('HUS')">HUS &amp; Vake</button>
      <button type="button" class="chip" onclick="setSearch('Varha')">Varha (Varsinais-Suomi)</button>
      <button type="button" class="chip" onclick="setSearch('Lapha')">Lapha (Lappi)</button>
      <button type="button" class="chip" onclick="setSearch('LocumMD')">Vuokralääkärit</button>
    </div>
    <div class="search-status" id="search-status"></div>
  </section>

  <section class="section-block" id="sec-inhouse">
    <div class="section-head">
      <h2 data-i18n="s1_title">1. Miten ”kuoriosakkeella” kierretään kilpailutuslaki? (7 sidosyksikköjättiä = 1,42 mrd. €/v)</h2>
      <p data-i18n="s1_sub">
        Korkein hallinto-oikeus (KHO 8.10.2025 taltio 2250) ja markkinaoikeus (MAO:154/2024) linjasivat, ettei hyvinvointialue saa ostaa palveluita ilman kilpailutusta yhtiöltä, josta se omistaa vain nimellisen murto-osan eikä käytä todellista määräysvaltaa. Klikkaa vaihetta tai yhtiökorttia.
      </p>
    </div>

    <div class="flow-steps">
      <div class="flow-step clickable-card" onclick="openFlowModal(1)">
        <span class="flow-badge" data-i18n="f1_step">Vaihe 1 · Klikkaa</span>
        <h4 data-i18n="f1_title">0,04 % nimellinen ”kuoriosake”</h4>
        <p data-i18n="f1_desc">Kunta tai hyvinvointialue ostaa muutaman sadan euron nimellisen osakkeen yhteisestä IT- tai talousyhtiöstä (esim. Sarastia, Istekki tai Tiera).</p>
      </div>
      <div class="flow-step clickable-card" onclick="openFlowModal(2)">
        <span class="flow-badge" data-i18n="f2_step">Vaihe 2 · Klikkaa</span>
        <h4 data-i18n="f2_title">Miljoonien suorahankinta ilman kilpaa</h4>
        <p data-i18n="f2_desc">Osakkeen varjolla virkamiehet tilaavat yhtiöltä kymmenillä miljoonilla euroilla IT- ja talouspalveluita järjestämättä avointa tarjouskilpailua.</p>
      </div>
      <div class="flow-step danger clickable-card" onclick="openFlowModal(3)">
        <span class="flow-badge" data-i18n="f3_step">Vaihe 3 · Vuotokohta</span>
        <h4 data-i18n="f3_title">Välikäsi ottaa 21–30 % katteen</h4>
        <p data-i18n="f3_desc">Välikäsiyhtiö ei tee kaikkea itse, vaan ketjuttaa sopimukset pörssiyhtiöille (Tietoevry, CGI, Atea, Accountor) ja ottaa välistä 21–30 % hallintokatteen.</p>
      </div>
      <div class="flow-step danger clickable-card" onclick="openFlowModal(4)">
        <span class="flow-badge" data-i18n="f4_step">Vaihe 4 · Lopputulos</span>
        <h4 data-i18n="f4_title">532 milj. €/v ylihintaa veronmaksajille</h4>
        <p data-i18n="f4_desc">Paikalliset pk-yritykset eivät pääse tarjoamaan lainkaan, ja hyvinvointialue joutuu säästämään hoitajista maksaakseen IT-välikäsien laskut.</p>
      </div>
    </div>

    <h3 style="font-size:19px; margin: 20px 0 12px;" data-i18n="inhouse_heading">Klikkaa sidosyksikköyhtiötä nähdäksesi rahan reitin ja valmiin 0 € KKV-ilmoituksen:</h3>
    <div class="cards-grid" id="inhouse-cards"></div>
  </section>

  <section class="section-block" id="sec-arbitrage">
    <div class="section-head">
      <h2 data-i18n="s2_title">2. Alueellinen hintavertailu: Miksi sama palvelu maksaa naapurialueella 2–3 kertaa enemmän?</h2>
      <p data-i18n="s2_sub">
        Klikkaa mitä tahansa hintavertailukorttia nähdäksesi, kuinka paljon kyseinen hyvinvointialue maksaa ylihintaa verrattuna Suomen edullisimpaan neljännekseen (P25-vertailuhinta).
      </p>
    </div>
    <div class="cards-grid" id="arbitrage-cards"></div>
  </section>

  <section class="section-block" id="sec-hilma">
    <div class="section-head">
      <h2 data-i18n="s3_title">3. Räätälöidyt tarjouskilpailut: 1–2 tarjouksen näennäiskilpailutukset (Hilma-tyyppitapaukset)</h2>
      <p data-i18n="s3_sub">
        Klikkaa edustavaa kilpailutustapausta nähdäksesi, millä keinotekoisella ehdolla muut tarjoajat suljettiin ulos ja miten pk-yrittäjä voi vaatia syrjivän ehdon poistamista maksutta (Hankintalaki 67 §, 75 § &amp; 133 §).
      </p>
    </div>
    <div class="cards-grid" id="hilma-cards"></div>
  </section>

  <section class="section-block" id="sec-foia">
    <div class="section-head">
      <h2 data-i18n="s4_title">4. Vaadi oman hyvinvointialueesi tai kuntasi ostolaskut julkisiksi (0 € tietopyyntö)</h2>
      <p data-i18n="s4_sub">
        Julkisuuslain (621/1999) mukaan jokaisella kansalaisella on oikeus saada hyvinvointialueen ja kunnan ostolaskut koneluettavassa muodossa 14 vuorokauden kuluessa. Klikkaa aluetta avataksesi valmiin tietopyynnön.
      </p>
    </div>
    <div class="cards-grid" id="buyer-cards"></div>
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
    Lähdeaineisto: Tutkihankintoja.fi, Hilma, KKV sidosyksikköselvitykset, MAO:154/2024 &amp; PRH YTJ.
  </div>
  <div>
    <a href="Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx" download>Lataa Excel-aineisto (.xlsx)</a> ·
    <a href="https://github.com/libertaari-suomalainen/kartelli-tutka">Avoin lähdekoodi (GitHub)</a> ·
    <a href="https://libertaari-suomalainen.github.io/tukipalkkio-purku/">Tutkimus I: Yritys- ja järjestötukien läpivalaisu (11,5 mrd. €)</a>
  </div>
</footer>
"""
    html += f"""
<script>
const APP = {json_blob};
let LANG = 'fi';

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
    brand_sub: "Tutkimusraportti 2026 · Sidosyksiköt, alueelliset ylihinnat & 0 € viranomaisilmoitukset",
    nav_sister: "← Tutkimus I: Yritys- & järjestötuet (11,5 mrd. €)",
    nav_xlsx: "⬇ Lataa Excel-aineisto (.xlsx)",
    hero_kicker: "JULKISET HANKINNAT · TUTKIMUSRAPORTTI 2026 · 38,7 MRD. €/V",
    hero_title: "38,7 miljardin euron ostokartelli: Miksi kuntien ja hyvinvointialueiden rahat eivät riitä hoitajiin?",
    hero_lead: "Valtio, 21 hyvinvointialuetta ja 308 kuntaa ostavat ulkopuolisilta yrityksiltä IT-järjestelmiä, hoivapalveluita ja urakoita <strong>38,7 miljardilla eurolla vuodessa</strong>. Tutkimuksemme osoittaa, että tästä potista <strong>1,26–3,5 miljardia euroa vuodessa</strong> (tämän aineiston suoraan mallinnetut säästöt <strong>1,26 mrd. €/v</strong>, koko 38,7 mrd. € hankintakantaan skaalattuna <strong>2,86–3,5 mrd. €/v</strong>) hupenee laittomiin ”in-house”-välikäsiin, 2–3-kertaisiin alueellisiin ylihintoihin ja 1–2 tarjouksen näennäiskilpailutuksiin.",
    summary_box_title: "Miten luet tätä julkaisua? (Kaikki kortit ovat klikattavia)",
    summary_box_body: "<strong>Klikkaa mitä tahansa lukukorttia, IT-/talousyhtiötä (Istekki, Apotti, Sarastia, 2M-IT, Monetra, Tiera, Valtori), alueellista hintavertailua tai Hilma-kilpailutusta</strong>. Saat esiin selkokielisen selityksen sekä valmiin, maksuttoman (0 €) viranomaisilmoituksen Kilpailu- ja kuluttajavirastolle (KKV) tai hyvinvointialueen kirjaamoon.",
    kpi1_lbl: "Julkiset ulkoiset ostot",
    kpi1_sub: "Valtion, hyvinvointialueiden ja kuntien vuotuiset ostot yrityksiltä",
    click_1: "Klikkaa: Minne 38,7 mrd. € menee? →",
    kpi2_lbl: "Sidosyksikkö- eli ”in-house”-ketjutus",
    kpi2_sub: "7 välikäsiyhtiötä (Istekki, Apotti, Sarastia, 2M-IT, Monetra, Tiera, Valtori) ilman kilpailutusta",
    click_2: "Klikkaa: Mikä on 0,04 % ”kuoriosake”? →",
    kpi3_lbl: "Alueiden välinen 2–3x ylihinta",
    kpi3_sub: "Vuosisäästö, kun kalleimmat alueet laskevat yksikköhinnat parhaan neljänneksen tasolle",
    click_3: "Klikkaa: Miksi sama palvelu maksaa 3x? →",
    kpi4_lbl: "1–2 tarjouksen kilpailutukset",
    kpi4_sub: "Räätälöidyt tarjousehdot sulkevat pk-yritykset ulos (n. 25 % vain 1 tarjous) ja nostavat hintoja 15–30 %",
    click_4: "Klikkaa: Miten ehdot räätälöidään? →",
    lbl_search: "Hae sidosyksikköä, hyvinvointialuetta, kuntaa, toimittajaa tai palvelua",
    chip_lbl: "Pikavalinnat:",
    chip_all: "Näytä kaikki",
    s1_title: "1. Miten ”kuoriosakkeella” kierretään kilpailutuslaki? (7 sidosyksikköjättiä = 1,42 mrd. €/v)",
    s1_sub: "Korkein hallinto-oikeus (KHO 8.10.2025 taltio 2250) ja markkinaoikeus (MAO:154/2024) linjasivat, ettei hyvinvointialue saa ostaa palveluita ilman kilpailutusta yhtiöltä, josta se omistaa vain nimellisen murto-osan eikä käytä todellista määräysvaltaa. Klikkaa vaihetta tai yhtiökorttia.",
    f1_step: "Vaihe 1 · Klikkaa",
    f1_title: "0,04 % nimellinen ”kuoriosake”",
    f1_desc: "Kunta tai hyvinvointialue ostaa muutaman sadan euron nimellisen osakkeen yhteisestä IT- tai talousyhtiöstä (esim. Sarastia, Istekki tai Tiera).",
    f2_step: "Vaihe 2 · Klikkaa",
    f2_title: "Miljoonien suorahankinta ilman kilpaa",
    f2_desc: "Osakkeen varjolla virkamiehet tilaavat yhtiöltä kymmenillä miljoonilla euroilla IT- ja talouspalveluita järjestämättä avointa tarjouskilpailua.",
    f3_step: "Vaihe 3 · Vuotokohta",
    f3_title: "Välikäsi ottaa 21–30 % katteen",
    f3_desc: "Välikäsiyhtiö ei tee kaikkea itse, vaan ketjuttaa sopimukset pörssiyhtiöille (Tietoevry, CGI, Atea, Accountor) ja ottaa välistä 21–30 % hallintokatteen.",
    f4_step: "Vaihe 4 · Lopputulos",
    f4_title: "532 milj. €/v ylihintaa veronmaksajille",
    f4_desc: "Paikalliset pk-yritykset eivät pääse tarjoamaan lainkaan, ja hyvinvointialue joutuu säästämään hoitajista maksaakseen IT-välikäsien laskut.",
    inhouse_heading: "Klikkaa sidosyksikköyhtiötä nähdäksesi rahan reitin ja valmiin 0 € KKV-ilmoituksen:",
    s2_title: "2. Alueellinen hintavertailu: Miksi sama palvelu maksaa naapurialueella 2–3 kertaa enemmän?",
    s2_sub: "Klikkaa mitä tahansa hintavertailukorttia nähdäksesi, kuinka paljon kyseinen hyvinvointialue maksaa ylihintaa verrattuna Suomen edullisimpaan neljännekseen (P25-vertailuhinta).",
    s3_title: "3. Räätälöidyt tarjouskilpailut: 1–2 tarjouksen näennäiskilpailutukset (Hilma-tyyppitapaukset)",
    s3_sub: "Klikkaa edustavaa kilpailutustapausta nähdäksesi, millä keinotekoisella ehdolla muut tarjoajat suljettiin ulos ja miten pk-yrittäjä voi vaatia syrjivän ehdon poistamista maksutta (Hankintalaki 67 §, 75 § & 133 §).",
    s4_title: "4. Vaadi oman hyvinvointialueesi tai kuntasi ostolaskut julkisiksi (0 € tietopyyntö)",
    s4_sub: "Julkisuuslain (621/1999) mukaan jokaisella kansalaisella on oikeus saada hyvinvointialueen ja kunnan ostolaskut koneluettavassa muodossa 14 vuorokauden kuluessa. Klikkaa aluetta avataksesi valmiin tietopyynnön."
  }},
  en: {{
    brand_title: "Finnish Economic Institute (STI) · Public Procurement Audit",
    brand_sub: "2026 Empirical Report · In-House Monopolies, Regional Markups & €0 Legal Filings",
    nav_sister: "← Study I: Corporate & NGO Subsidies (€11.5B)",
    nav_xlsx: "⬇ Download Excel Dataset (.xlsx)",
    hero_kicker: "PUBLIC PROCUREMENT · RESEARCH REPORT 2026 · €38.7B/YR",
    hero_title: "The €38.7 Billion Procurement Cartel: Why Public Money Never Reaches Frontline Care",
    hero_lead: "Finland's state, 21 Wellbeing Counties, and 308 municipalities spend <strong>€38.7 billion per year</strong> buying IT systems, healthcare services, and contracts from outside vendors. Our research shows that <strong>€1.26B–€3.5B per year</strong> (directly modeled savings in this dataset <strong>€1.26B/yr</strong>, scaled across the full €38.7B procurement base <strong>€2.86B–€3.5B/yr</strong>) is lost to illegal 'in-house' middlemen, 2–3x regional price markups, and 1–2 bid tenders.",
    summary_box_title: "How to Read This Interactive Report (Every Card Is Clickable)",
    summary_box_body: "<strong>Click any metric card, IT/admin company (Istekki, Apotti, Sarastia, 2M-IT, Monetra, Tiera, Valtori), regional price comparison, or tender below</strong> to open a plain-English explanation—plus a ready-to-send, zero-fee (€0) official filing to the Competition Authority (KKV) or your Wellbeing County.",
    kpi1_lbl: "Total Public External Purchases",
    kpi1_sub: "Annual purchases by the state, 21 Wellbeing Counties, and 308 municipalities",
    click_1: "Click: Where does the €38.7B go? →",
    kpi2_lbl: "In-House 'Sidosyksikkö' Middlemen",
    kpi2_sub: "7 middlemen (Istekki, Apotti, Sarastia, 2M-IT, Monetra, Tiera, Valtori) bypassing open tenders",
    click_2: "Click: What is the 0.04% 'token share' loophole? →",
    kpi3_lbl: "2–3x Regional Overpricing",
    kpi3_sub: "Annual savings when overpriced counties match top-quartile (P25) unit prices",
    click_3: "Click: Why does the same service cost 3x more? →",
    kpi4_lbl: "1–2 Bid 'Rigged' Tenders",
    kpi4_sub: "Tailored requirements lock out SMEs (~25% receive only 1 bid) and inflate prices by 15–30%",
    click_4: "Click: How are tender specs rigged? →",
    lbl_search: "Search in-house company, Wellbeing County, municipality, vendor, or category",
    chip_lbl: "Quick filters:",
    chip_all: "Show all",
    s1_title: "1. How a 0.04% 'Token Share' Bypasses Procurement Law (7 In-House Giants = €1.42B/yr)",
    s1_sub: "Finland's Supreme Administrative Court (KHO 8.10.2025 taltio 2250) and Market Court (MAO:154/2024) ruled that a public authority cannot buy services without competitive bidding from an in-house company in which it holds only a nominal token share and exercises no real control.",
    f1_step: "Step 1 · Click",
    f1_title: "0.04% Nominal 'Token Share'",
    f1_desc: "A municipality or Wellbeing County buys a tiny nominal share in a joint IT or payroll company (e.g., Sarastia, Istekki, or Tiera).",
    f2_step: "Step 2 · Click",
    f2_title: "Multi-Million Direct Award",
    f2_desc: "Using that single share as an excuse, officials award tens of millions in contracts with zero open competitive bidding.",
    f3_step: "Step 3 · The Leak",
    f3_title: "Middleman Takes a 21–30% Markup",
    f3_desc: "The middleman subcontracts the actual work to large conglomerates (Tietoevry, CGI, Atea, Accountor) while skimming a 21–30% fee.",
    f4_step: "Step 4 · Outcome",
    f4_title: "€532M/yr Overcharge to Taxpayers",
    f4_desc: "Local SMEs are locked out of the market, and counties cut frontline nurses to pay inflated IT and administrative bills.",
    inhouse_heading: "Click any in-house intermediary to inspect the money trail & ready-to-send €0 KKV complaint:",
    s2_title: "2. Regional Price Audit: Why Does the Exact Same Service Cost 2–3x More Next Door?",
    s2_sub: "Click any regional price card to see how much that Wellbeing County overpays compared to Finland's best-performing quartile (P25 benchmark).",
    s3_title: "3. Tailored Tenders: 1–2 Bid 'Fake Competitions' (Hilma Archetypes)",
    s3_sub: "Click any representative tender case to see which artificial requirement locked out competitors and how any entrepreneur can demand its removal for €0.",
    s4_title: "4. Demand Your Wellbeing County's Purchase Invoices Under the Freedom of Information Act (€0)",
    s4_sub: "Under Finland's Openness of Government Activities Act (621/1999), every citizen has the right to receive machine-readable purchase invoice data within 14 days. Click any authority to open a ready-to-send request."
  }}
}};

function openModalHtml(title, subtitle, sectionsHtml) {{
  document.getElementById('modal-content').innerHTML = `
    <h2>${{title}}</h2>
    <div class="modal-sub">${{subtitle}}</div>
    ${{sectionsHtml}}
  `;
  document.getElementById('detail-modal').classList.add('open');
}}

function closeModal() {{
  document.getElementById('detail-modal').classList.remove('open');
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

function openKpiModal(key) {{
  const fi = LANG === 'fi';
  if (key === 'total_spend') {{
    openModalHtml(
      fi ? "Minne julkisen sektorin 38,70 miljardin euron ulkoiset ostot menevät?" : "Where Does Finland's €38.70 Billion in Public Procurement Go?",
      fi ? "Tilastokeskus (S.13: P.2 + D.632) · Valtio, 21 hyvinvointialuetta ja 308 kuntaa" : "Statistics Finland · State, 21 Wellbeing Counties, and 308 Municipalities",
      `<div class="modal-section">
        <h4>${{fi ? "Selkokielinen kokonaiskuva" : "Plain-English Overview"}}</h4>
        <p>${{fi
          ? "Suomen julkisyhteisöt käyttävät joka vuosi 38,7 miljardia euroa tavaroiden, IT-järjestelmien, hoivapalveluiden, kuljetusten ja rakennusurakoiden ostamiseen yksityisiltä ja julkisomisteisilta yrityksiltä. Tämä on Suomen suurin yksittäinen verovarojen erä. Tässä tutkimuksessa suoraan mallinnetut kolme leikkuria tuottavat 1,26 mrd. €/v välittömän säästön (532,38 M€ sidosyksiköistä + 711,23 M€ P25-hintavertailusta + 13,22 M€ Hilma-esimerkkikohteista), ja koko kansalliseen hankintakantaan skaalattuna 2,86–3,5 mrd. €/v."
          : "Finland's public sector spends €38.7 billion every year buying goods, IT systems, healthcare services, and construction from external vendors. The three directly modeled modules in this report identify €1.26B/yr in immediate savings (€532.38M in-house markups + €711.23M P25 unit-price compression + €13.22M Hilma sample), scaling to €2.86B–€3.5B/yr nationwide."}}</p>
      </div>`
    );
  }} else if (key === 'inhouse_leak') {{
    openModalHtml(
      fi ? "Mikä on sidosyksikkö- eli ”in-house”-kuoriosakekikkailu? (1,42 mrd. €/v)" : "What Is the In-House 'Token Share' Loophole? (€1.42B/yr)",
      fi ? "KHO 8.10.2025 taltio 2250, MAO:154/2024 & Hankintalaki 15 §" : "Supreme Administrative Court KHO 8.10.2025, MAO:154/2024 & Procurement Act § 15",
      `<div class="modal-section">
        <h4>${{fi ? "Näin kilpailutuslaki kierretään" : "How the Law Is Bypassed"}}</h4>
        <p>${{fi
          ? "Hankintalain mukaan julkinen viranomainen saa ostaa palveluita ilman kilpailutusta vain omalta yksiköltään, jota se tosiasiallisesti hallitsee. Kunnat ja hyvinvointialueet ovat kuitenkin kiertäneet lakia ostamalla 0,04–1,2 prosentin nimellisen ”kuoriosakkeen” jättimäisistä yhteisyrityksistä (Istekki, Sarastia/Numera, 2M-IT, Monetra, Tiera) tai lukittautumalla kilpailuttamattomiin alihankintaketjuihin (Apotti, Valtori) yhteensä 1,42 miljardilla eurolla vuodessa."
          : "Under procurement law, a public buyer can skip competitive bidding only when buying from an entity it genuinely controls. Finnish counties and municipalities bypassed the law by buying a tiny 0.04%–1.2% 'token share' in giant joint companies or locking into uncompeted subcontracting chains totaling €1.42B/year."}}</p>
      </div>`
    );
  }} else if (key === 'price_spread') {{
    openModalHtml(
      fi ? "Miksi sama palvelu maksaa yhdellä alueella 2–3 kertaa enemmän kuin naapurissa?" : "Why Does the Same Service Cost 2–3x More in Neighboring Regions?",
      fi ? "Viiden suurimman sote- ja IT-hankintakategorian yksikköhintavertailu" : "Unit-Price Audit Across 5 Major Healthcare & IT Categories",
      `<div class="modal-section">
        <h4>${{fi ? "711,23 miljoonan euron vuosisäästö pelkällä hintakaton asettamisella" : "€711.23M Annual Saving by Capping Unit Prices at the Best Quartile (P25)"}}</h4>
        <p>${{fi
          ? "Koska hyvinvointialueet eivät julkaise eivätkä vertaa maksamiaan yksikköhintoja, sama potilastietojärjestelmän lisenssi, vuokralääkäritunti tai ikäihmisten ympärivuorokautinen hoivavuorokausi maksaa kalleimmilla alueilla jopa 2–3 kertaa enemmän kuin Suomen edullisimmassa neljänneksessä (P25-taso)."
          : "Because Wellbeing Counties do not benchmark unit prices, the exact same EHR software seat, locum doctor hour, or elderly care day costs up to 3x more in the most expensive regions than in the best-performing quartile (P25)."}}</p>
      </div>`
    );
  }} else if (key === 'single_bid') {{
    openModalHtml(
      fi ? "1–2 tarjouksen näennäiskilpailutukset (45 % hankinnoista)" : "1–2 Bid 'Rigged' Tenders (45% of Public Procurements)",
      fi ? "Hilma-kilpailutusaineisto & Hankintalain 67 § ja 75 §" : "Hilma Tender Registry & Procurement Act § 67 & § 75",
      `<div class="modal-section">
        <h4>${{fi ? "Miten tarjouspyyntö räätälöidään vanhalle toimittajalle?" : "How Tender Specifications Are Tailored to the Incumbent"}}</h4>
        <p>${{fi
          ? "Noin 45 prosentissa Suomen julkisista hankinnoista saadaan vain 1–2 tarjousta (ja noin neljänneksessä vain 1 tarjous). Tyypillinen keino on kirjata tarjouspyyntöön suhteeton liikevaihtovaatimus, suljettu rajapinta tai jättää hankinta jakamatta osiin (Hankintalaki 75 §). Tällöin pk-yritykset putoavat pois ja nykyinen toimittaja voi hinnoitella palvelun ilman kilpailupainetta."
          : "Roughly 45% of Finnish public tenders receive only 1–2 bids (and ~25% receive just 1 bid) because tender specifications require disproportionate turnover, proprietary interfaces, or fail to divide contracts into lots (§ 75)—allowing the incumbent vendor to name its price."}}</p>
      </div>`
    );
  }}
}}

function openFlowModal(step) {{
  const fi = LANG === 'fi';
  const steps = {{
    1: {{
      t: fi ? "Vaihe 1: Kunta tai hyvinvointialue ostaa 0,04 % ”kuoriosakkeen”" : "Step 1: Authority Buys a 0.04% Nominal 'Token Share'",
      s: fi ? "Nimellinen omistus ilman todellista päätösvaltaa" : "Nominal Ownership With Zero Real Governance Control",
      b: fi ? "Hyvinvointialue ostaa esimerkiksi yhden osakkeen (0,04 % – 1,2 % osakekannasta) satojen kuntien ja alueiden yhteisestä yhtiöstä. Yhtiökokouksessa yksittäisellä hyvinvointialueella ei ole minkäänlaista todellista määräysvaltaa yhtiön hinnoitteluun tai johtoon."
            : "A Wellbeing County buys a tiny fraction (0.04%–1.2%) of shares in a joint company owned by hundreds of municipalities, giving it zero real control over pricing or management."
    }},
    2: {{
      t: fi ? "Vaihe 2: Virkamies tilaa kymmenillä miljoonilla ilman kilpailutusta" : "Step 2: Officials Award Tens of Millions Without Competitive Bidding",
      s: fi ? "Hankintalain 15 §:n väärinkäyttö (MAO:154/2024 & KHO 8.10.2025)" : "Abuse of Procurement Act § 15 (Ruled Illegal in MAO:154/2024 & KHO 8.10.2025)",
      b: fi ? "Koska yhtiötä kutsutaan ”sidosyksiköksi” (in-house), hankintajohtaja ei julkaise lainkaan tarjouspyyntöä Hilmassa. Sopimus annetaan suoraan välikäsiyhtiölle, vaikka markkinoilla olisi kymmeniä edullisempia suomalaisia yrityksiä."
            : "Claiming the vendor is an 'in-house' unit, procurement officials skip public tenders entirely and hand multi-million contracts directly to the intermediary."
    }},
    3: {{
      t: fi ? "Vaihe 3: Välikäsiyhtiö ottaa 21–30 % katteen ja ketjuttaa työn pörssiyhtiöille" : "Step 3: Middleman Skims 21–30% and Subcontracts to Big Tech",
      s: fi ? "Tuplabyrokratia veronmaksajan piikkiin" : "Double Bureaucracy Paid by the Taxpayer",
      b: fi ? "Välikäsiyhtiö (kuten Istekki, Tiera tai Sarastia) ei suinkaan tuota kaikkia ohjelmistoja ja laitteita itse, vaan ostaa ne edelleen suurilta pörssiyhtiöiltä (Tietoevry, CGI, Atea, Accountor) ja lisää laskuun oman 21–30 % hallinto- ja johtopalkkiokatteensa."
            : "The in-house intermediary subcontracts the actual software and hardware delivery to large conglomerates (Tietoevry, CGI, Atea) and adds its own 21–30% administrative margin on top."
    }},
    4: {{
      t: fi ? "Vaihe 4: Lopputulos — 532 milj. €/v ylihintaa ja hoitajien irtisanomiset" : "Step 4: Outcome — €532M/yr Overcharge & Frontline Care Cuts",
      s: fi ? "Hallinto ja IT-välikädet syövät hoitobudjetin (532,38 milj. €/v)" : "Middleman Markups Drain the Frontline Care Budget (€532.38M/yr)",
      b: fi ? "Kun hyvinvointialueet ja valtion virastot maksavat seitsemälle IT- ja taloushallintovälikädelle yhteensä 532,38 miljoonaa euroa vuodessa ylihintaa ja ketjutuskustannuksia, lakisääteinen alijäämä katetaan sulkemalla terveysasemia ja vähentämällä hoitohenkilökuntaa."
            : "When Wellbeing Counties and state agencies overpay €532.38M/yr across the 7 IT and administrative middlemen, they balance their budgets by closing local clinics and cutting nursing staff."
    }}
  }};
  const item = steps[step];
  openModalHtml(item.t, item.s, `<div class="modal-section"><h4>${{fi ? "Mitä tässä vaiheessa tapahtuu?" : "What Happens in This Step?"}}</h4><p>${{item.b}}</p></div>`);
}}

function openInhouseModal(idx) {{
  const f = APP.ssot.inhouse_flows[idx];
  const kkv = APP.kkv_filings[f.inhouse_y_tunnus];
  const oik = APP.oikaisu_filings[f.inhouse_y_tunnus];
  const fi = LANG === 'fi';
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
      <h4>${{fi ? "Valmis 0,00 € toimenpidepyyntö Kilpailu- ja kuluttajavirastolle (KKV) tai oikaisuvaatimus" : "Ready-to-Send €0.00 Official Complaint (KKV or Rectification Demand)"}}</h4>
      <p>${{fi
        ? "Markkinaoikeuden valitusoikeudenkäynti maksaa 2 440–7 300 €, mutta alla oleva valvontailmoitus KKV:lle (kirjaamo@kkv.fi) tai hankintaoikaisuvaatimus ostajan kirjaamoon on jokaiselle kansalaiselle ja yrittäjälle 100 % maksuton (0,00 €):"
        : "Filing a Market Court appeal costs €2,440–€7,300, but submitting this statutory investigation request to the Competition Authority (kirjaamo@kkv.fi) or the buyer's registry costs €0.00:"}}</p>
      <textarea id="active-legal-textarea" class="legal-box" readonly>${{kkv.body}}</textarea>
      <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <button class="btn-primary" onclick="copyLegalBox(this)">${{fi ? "Kopioi asiakirja leikepöydälle" : "Copy Filing Text"}}</button>
        <a class="btn-secondary" href="${{mailtoKkv}}">${{fi ? "Avaa sähköpostissa (KKV kirjaamo@kkv.fi)" : "Open in Email (KKV)"}}</a>
        <a class="btn-secondary" href="${{mailtoOik}}">${{fi ? "Lähetä oikaisuvaatimus ostajalle (" + f.buyer_kirjaamo_email + ")" : "Send Rectification to Buyer"}}</a>
      </div>
    </div>`
  );
}}

function openArbitrageModal(idx) {{
  const r = APP.ssot.arbitrage_rows[idx];
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
    </div>`
  );
}}

function openHilmaModal(idx) {{
  const t = APP.ssot.flagged_hilma_tenders[idx];
  const fil = APP.hilma_filings[t.tender_id];
  const fi = LANG === 'fi';
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
      <h4>${{fi ? "Valmis 0,00 € vaatimus syrjivän tarjousehdon poistamiseksi (Hankintalaki 67 § & 75 §)" : "Ready-to-Send €0.00 Demand to Remove Tailored Spec (Procurement Act § 67 & § 75)"}}</h4>
      <textarea id="active-legal-textarea" class="legal-box" readonly>${{fil.body}}</textarea>
      <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <button class="btn-primary" onclick="copyLegalBox(this)">${{fi ? "Kopioi vaatimus leikepöydälle" : "Copy Challenge Text"}}</button>
        <a class="btn-secondary" href="${{mailto}}">${{fi ? "Lähetä hankintayksikölle (" + fil.recipient_email + ")" : "Send via Email"}}</a>
      </div>
    </div>`
  );
}}

function openBuyerFoiaModal(idx) {{
  const b = APP.ssot.public_buyer_directory[idx];
  const fil = APP.foia_filings[b.y_tunnus];
  const fi = LANG === 'fi';
  const mailto = `mailto:${{fil.recipient_email}}?subject=${{encodeURIComponent(fil.subject)}}&body=${{encodeURIComponent(fil.body)}}`;

  openModalHtml(
    `${{b.entity_name}} (Y-tunnus: ${{b.y_tunnus}})`,
    `${{fi ? "Julkisuuslain (621/1999) 13 § ja 16.3 § mukainen tietopyyntö" : "Statutory Freedom of Information Request (Act 621/1999)"}} · ${{b.kirjaamo_email}}`,
    `<div class="modal-section">
      <h4>${{fi ? "Mitä tämä asiakirja velvoittaa viranomaisen tekemään?" : "What Does This Request Require the Authority to Do?"}}</h4>
      <p>${{fi
        ? `Tämä valmis tietopyyntö velvoittaa viranomaisen (<strong>${{b.entity_name}}</strong>, vuosiostot <strong>${{fmtM(b.annual_purchases_m_eur)}}</strong>, keskeiset sidosyksiköt: <em>${{b.primary_inhouse_shells}}</em>) luovuttamaan 14 vuorokauden kuluessa koneluettavan ostolaskuaineiston (CSV/XLSX) sekä sidosyksikköjen osakassopimukset ja suorahankintapäätökset maksutta.`
        : `This statutory request requires <strong>${{b.entity_name}}</strong> (annual purchases <strong>${{fmtM(b.annual_purchases_m_eur)}}</strong>, primary in-house shells: <em>${{b.primary_inhouse_shells}}</em>) to release machine-readable purchase invoice ledgers (CSV/XLSX) and in-house shareholder agreements within 14 days at zero cost.`}}</p>
      <textarea id="active-legal-textarea" class="legal-box" readonly>${{fil.body}}</textarea>
      <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <button class="btn-primary" onclick="copyLegalBox(this)">${{fi ? "Kopioi tietopyyntö leikepöydälle" : "Copy FOIA Request"}}</button>
        <a class="btn-secondary" href="${{mailto}}">${{fi ? "Avaa sähköpostissa (" + b.kirjaamo_email + ")" : "Open in Email"}}</a>
      </div>
    </div>`
  );
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

  // 1. In-house cards
  let inMatches = 0;
  let inHtml = '';
  APP.ssot.inhouse_flows.forEach((f, idx) => {{
    const txt = `${{f.inhouse_vendor}} ${{f.inhouse_y_tunnus}} ${{f.buyer_name}} ${{f.subcontractor_vendor}} ${{f.legal_status}}`.toLowerCase();
    if (q && !txt.includes(q)) return;
    inMatches++;
    const isToken = f.is_illegal_under_10pct;
    const eqStr = Number(f.buyer_equity_share_pct).toLocaleString('fi-FI');
    const accent = isToken ? 'red-accent' : 'amber-accent';
    const badge = isToken
      ? `<span class="badge badge-red">${{fi ? 'Kuoriosake ' + eqStr + ' %' : 'Token Share ' + eqStr + '%'}}</span>`
      : `<span class="badge badge-amber">${{fi ? 'Suorahankintamonopoli' : 'In-House Monopoly'}}</span>`;
    const inComment = isToken
      ? (fi
          ? `Vähemmistöosakkaan osuus vain ${{eqStr}} %, suoraosto ilman kilpailutusta ${{fmtCardM(f.annual_spend_m_eur)}}/v. Ketjuttaa työtä: ${{f.subcontractor_vendor}}.`
          : `Minority buyer owns just ${{eqStr}}% yet awards ${{fmtCardM(f.annual_spend_m_eur)}}/yr without tenders. Subcontracted to: ${{f.subcontractor_vendor}}.`)
      : (fi
          ? `${{f.legal_status}}. Suoraosto ilman kilpailutusta ${{fmtCardM(f.annual_spend_m_eur)}}/v. Ketjuttaa työtä: ${{f.subcontractor_vendor}}.`
          : `Uncompeted in-house monopoly (${{eqStr}}% equity), ${{fmtCardM(f.annual_spend_m_eur)}}/yr direct spend. Subcontracted to: ${{f.subcontractor_vendor}}.`);
    inHtml += `<div class="story-card ${{accent}} clickable-card" onclick="openInhouseModal(${{idx}})">
      <div class="story-top">
        <div class="card-kicker-row">
          ${{badge}}
          <span class="card-id-pill">Y: ${{f.inhouse_y_tunnus}}</span>
        </div>
        <h3>${{f.inhouse_vendor}}</h3>
        <div class="story-subtitle">${{fi ? 'Tilaajat:' : 'Buyers:'}} ${{f.buyer_name}}</div>
        <p class="story-commentary">${{inComment}}</p>
      </div>
      <div>
        <div class="metrics-strip">
          <div><span>${{fi ? 'Suora osto / v' : 'Direct Spend'}}</span><strong>${{fmtCardM(f.annual_spend_m_eur)}}</strong></div>
          <div><span>${{fi ? 'Välikäden kate' : 'Markup'}}</span><strong style="color:var(--amber)">${{f.inhouse_markup_pct}} %</strong></div>
          <div><span>${{fi ? 'Vuosisäästö' : 'Annual Saving'}}</span><strong style="color:var(--red)">-${{fmtCardM(f.recoverable_saving_m_eur)}}</strong></div>
        </div>
        <div class="click-hint">${{fi ? 'Klikkaa: Rahan reitti & 0 € KKV-ilmoitus →' : 'Click: Money trail & €0 KKV complaint →'}}</div>
      </div>
    </div>`;
  }});
  if (!inHtml) {{
    inHtml = `<div class="empty-box"><span>${{fi ? `Ei sidosyksikköosumia haulle ”${{safeQ}}”. Katso osiot 2–4 alla.` : `No in-house matches for "${{safeQ}}". Check Sections 2–4 below.`}}</span><button type="button" class="btn-secondary" onclick="setSearch('')">${{fi ? 'Näytä kaikki' : 'Show all'}}</button></div>`;
  }}
  document.getElementById('inhouse-cards').innerHTML = inHtml;

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
    hilmaHtml = `<div class="empty-box"><span>${{fi ? `Ei Hilma-kilpailutusosumia haulle ”${{safeQ}}”.` : `No Hilma tender matches for "${{safeQ}}".`}}</span><button type="button" class="btn-secondary" onclick="setSearch('')">${{fi ? 'Näytä kaikki' : 'Show all'}}</button></div>`;
  }}
  document.getElementById('hilma-cards').innerHTML = hilmaHtml;

  // 4. Buyer FOIA directory cards
  let buyerMatches = 0;
  let buyerHtml = '';
  APP.ssot.public_buyer_directory.forEach((b, idx) => {{
    const txt = `${{b.entity_name}} ${{b.y_tunnus}} ${{b.kirjaamo_email}} ${{b.primary_inhouse_shells}}`.toLowerCase();
    if (q && !txt.includes(q)) return;
    buyerMatches++;
    buyerHtml += `<div class="story-card green-accent clickable-card" onclick="openBuyerFoiaModal(${{idx}})">
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

  // Update Search Status Banner
  const statusEl = document.getElementById('search-status');
  if (q) {{
    statusEl.style.display = 'block';
    statusEl.innerHTML = fi
      ? `Hakutulokset haulle <strong>”${{safeQ}}”</strong>: <strong>${{inMatches}}</strong> sidosyksikköä (Osio 1), <strong>${{arbMatches}}</strong> hintavertailua (Osio 2), <strong>${{hilmaMatches}}</strong> Hilma-kilpailutusta (Osio 3) ja <strong>${{buyerMatches}}</strong> kirjaamoa (Osio 4). <a href="javascript:void(0)" onclick="setSearch('')" style="color:var(--accent-dark);margin-left:10px;">✕ Tyhjennä haku</a>`
      : `Search results for <strong>"${{safeQ}}"</strong>: <strong>${{inMatches}}</strong> in-house flows (Sec 1), <strong>${{arbMatches}}</strong> price benchmarks (Sec 2), <strong>${{hilmaMatches}}</strong> Hilma tenders (Sec 3), and <strong>${{buyerMatches}}</strong> buyer registries (Sec 4). <a href="javascript:void(0)" onclick="setSearch('')" style="color:var(--accent-dark);margin-left:10px;">✕ Clear search</a>`;
  }} else {{
    statusEl.style.display = 'none';
  }}
}}

document.getElementById('search-box').addEventListener('input', renderAll);
renderAll();
</script>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path
