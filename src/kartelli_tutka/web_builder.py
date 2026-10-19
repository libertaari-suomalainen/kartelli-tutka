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
    padding: 12px 20px;
  }}
  .topbar-inner {{
    max-width: 1140px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
  }}
  .brand {{
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    color: var(--text);
  }}
  .brand-mark {{
    width: 36px;
    height: 36px;
    border-radius: 6px;
    background: var(--accent);
    color: #fff;
    font-family: 'DM Sans', sans-serif;
    font-weight: 800;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}
  .brand-text strong {{
    display: block;
    font-family: 'DM Sans', sans-serif;
    font-size: 15.5px;
    font-weight: 700;
    line-height: 1.2;
  }}
  .brand-text span {{ display: block; font-size: 12px; color: var(--muted); }}
  .nav-actions {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
  .lang-btn {{
    background: var(--stone);
    border: 1px solid var(--border-strong);
    color: var(--text);
    padding: 8px 13px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    min-height: 40px;
  }}
  .lang-btn.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
  .btn-primary {{
    background: var(--accent);
    color: #fff;
    text-decoration: none;
    padding: 9px 15px;
    border-radius: 6px;
    font-size: 13.5px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    min-height: 40px;
    border: none;
    cursor: pointer;
  }}
  .btn-primary:hover {{ background: var(--accent-dark); }}
  .btn-secondary {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border-strong);
    text-decoration: none;
    padding: 9px 14px;
    border-radius: 6px;
    font-size: 13.5px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    min-height: 40px;
    cursor: pointer;
  }}
  .btn-secondary:hover {{ background: var(--stone); }}
  .container {{ max-width: 1140px; margin: 0 auto; padding: 32px 20px 80px; }}
  .hero-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 40px;
    box-shadow: var(--shadow);
    margin-bottom: 32px;
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
  .hero-title {{ font-size: clamp(26px, 4vw, 40px); line-height: 1.16; font-weight: 800; margin-bottom: 16px; }}
  .hero-lead {{ font-size: clamp(16px, 2vw, 18.5px); color: var(--body); max-width: 860px; margin-bottom: 24px; }}
  .callout-stone {{
    background: var(--stone);
    border-left: 4px solid var(--accent);
    padding: 18px 22px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 28px;
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
  .section-head p {{ font-size: 15.5px; color: var(--muted); max-width: 820px; }}
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
  .cards-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 18px; }}
  .story-card {{
    background: var(--bg);
    border: 1px solid var(--border-strong);
    border-radius: 8px;
    padding: 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .story-card.red-accent {{ border-left: 4px solid var(--red); }}
  .story-card.amber-accent {{ border-left: 4px solid var(--amber); }}
  .story-card.green-accent {{ border-left: 4px solid var(--accent); }}
  .story-top {{ margin-bottom: 14px; }}
  .story-header {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 8px; }}
  .story-card h3 {{ font-size: 18px; line-height: 1.3; }}
  .story-meta {{ font-size: 13px; color: var(--muted); margin-bottom: 10px; }}
  .story-commentary {{ font-size: 14.5px; color: var(--body); margin-bottom: 14px; }}
  .metrics-strip {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 12px;
  }}
  .metrics-strip div span {{ display: block; font-size: 11px; color: var(--muted); }}
  .metrics-strip div strong {{ font-family: 'DM Sans', sans-serif; font-size: 14.5px; color: var(--text); }}
  .badge {{ display: inline-block; padding: 4px 10px; border-radius: 99px; font-size: 11.5px; font-weight: 700; white-space: nowrap; }}
  .badge-red {{ background: var(--red-soft); color: var(--red); border: 1px solid var(--red-border); }}
  .badge-amber {{ background: var(--amber-soft); color: var(--amber); border: 1px solid var(--amber-border); }}
  .badge-green {{ background: var(--accent-soft); color: var(--accent-dark); border: 1px solid #A7F3D0; }}
  .filter-bar {{
    background: var(--stone);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
  }}
  .filter-col {{ flex: 1; min-width: 240px; }}
  .filter-col label {{ display: block; font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }}
  .input-box, .select-box {{
    width: 100%;
    min-height: 44px;
    padding: 10px 14px;
    border-radius: 6px;
    border: 1px solid var(--border-strong);
    background: var(--surface);
    color: var(--text);
    font-size: 15px;
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
  .modal-card h2 {{ font-size: 24px; margin-bottom: 8px; padding-right: 44px; }}
  .modal-sub {{ font-size: 14px; color: var(--muted); margin-bottom: 20px; }}
  .modal-section {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px 20px;
    margin-bottom: 16px;
  }}
  .modal-section h4 {{ font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent-dark); margin-bottom: 8px; }}
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
    max-width: 1140px;
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
  @media (max-width: 900px) {{
    .flow-steps {{ grid-template-columns: 1fr; }}
    .hero-card, .section-block {{ padding: 22px 18px; }}
  }}
  @media (max-width: 640px) {{
    .container {{ padding: 18px 12px 56px; }}
    .modal-backdrop {{ padding: 10px; align-items: flex-end; }}
    .modal-card {{ padding: 22px 18px; max-height: 92vh; border-radius: 12px 12px 0 0; }}
    .metrics-strip {{ grid-template-columns: 1fr; }}
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
        <span data-i18n="brand_sub">Tutkimusraportti · Klikkaa mitä tahansa korttia avataksesi selkokielisen analyysin</span>
      </div>
    </a>
    <div class="nav-actions">
      <button class="lang-btn active" id="btn-fi" onclick="setLang('fi')">Suomi</button>
      <button class="lang-btn" id="btn-en" onclick="setLang('en')">English</button>
      <a class="btn-secondary" href="https://libertaari-suomalainen.github.io/tukipalkkio-purku/" data-i18n="nav_sister">← Tutkimus I: Yritys- & järjestötuet (11,5 mrd. €)</a>
      <a class="btn-primary" href="Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx" download data-i18n="nav_xlsx">Lataa Excel-malli (.xlsx)</a>
    </div>
  </div>
</header>

<main class="container">
  <section class="hero-card">
    <div class="kicker" data-i18n="hero_kicker">JULKISET HANKINNAT · TUTKIMUSRAPORTTI 2026</div>
    <h1 class="hero-title" data-i18n="hero_title">38,7 miljardin euron ostokartelli: Miksi kuntien ja hyvinvointialueiden rahat eivät riitä hoitajiin?</h1>
    <p class="hero-lead" data-i18n="hero_lead">
      Valtio, 21 hyvinvointialuetta ja 308 kuntaa ostavat ulkopuolisilta yrityksiltä IT-järjestelmiä, hoivapalveluita ja urakoita <strong>38,7 miljardilla eurolla vuodessa</strong>. Tutkimuksemme osoittaa, että tästä potista <strong>1,5–3,5 miljardia euroa vuodessa</strong> hupenee laittomiin ”in-house”-välikäsiin, 2–3-kertaisiin alueellisiin ylihintoihin ja yhden tarjouksen näennäiskilpailutuksiin.
    </p>
    <div class="callout-stone">
      <h3 data-i18n="summary_box_title">Miten luet tätä julkaisua? (Kaikki kortit ovat klikattavia)</h3>
      <p data-i18n="summary_box_body">
        <strong>Klikkaa mitä tahansa lukukorttia, kaavion vaihetta, IT-/talousyhtiötä, hintavertailua tai kilpailutusta</strong>. Saat esiin selkokielisen selityksen siitä, miten järjestely toimii — sekä halutessasi valmiin, maksuttoman (0 €) viranomaisilmoituksen Kilpailu- ja kuluttajavirastolle (KKV) tai omalle hyvinvointialueellesi.
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
          <div class="kpi-label" data-i18n="kpi4_lbl">Yhden tarjouksen kilpailutukset</div>
          <div class="kpi-val red">45 % hankinnoista</div>
          <div class="kpi-sub" data-i18n="kpi4_sub">Räätälöidyt tarjousehdot sulkevat pk-yritykset ulos ja nostavat hintoja 15–30 %</div>
        </div>
        <div class="click-hint" data-i18n="click_4">Klikkaa: Miten ehdot räätälöidään? →</div>
      </div>
    </div>
  </section>

  <section class="section-block" id="sec-inhouse">
    <div class="section-head">
      <h2 data-i18n="s1_title">1. Miten ”kuoriosakkeella” kierretään kilpailutuslaki? (Klikkaa vaihetta tai yhtiötä)</h2>
      <p data-i18n="s1_sub">
        Korkein hallinto-oikeus ja markkinaoikeus (päätös MAO:154/2024) linjasivat, ettei hyvinvointialue saa ostaa palveluita ilman kilpailutusta yhtiöltä, josta se omistaa vain nimellisen murto-osan eikä käytä todellista määräysvaltaa.
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
        <h4 data-i18n="f4_title">504 milj. €/v ylihintaa veronmaksajille</h4>
        <p data-i18n="f4_desc">Paikalliset pk-yritykset eivät pääse tarjoamaan lainkaan, ja hyvinvointialue joutuu säästämään hoitajista maksaakseen IT-välikäsien laskut.</p>
      </div>
    </div>

    <div class="filter-bar" style="margin-top:20px;">
      <div class="filter-col">
        <label for="search-box" data-i18n="lbl_search">Hae yhtiötä, hyvinvointialuetta tai palvelua</label>
        <input id="search-box" type="text" class="input-box" placeholder="Hae esim. Istekki, Apotti, Sarastia, Pirkanmaa, HUS, Lapha..." />
      </div>
    </div>

    <h3 style="font-size:19px; margin-bottom:12px;" data-i18n="inhouse_heading">Klikkaa sidosyksikköyhtiötä nähdäksesi rahan reitin ja valmiin 0 € KKV-ilmoituksen:</h3>
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
      <h2 data-i18n="s3_title">3. Räätälöidyt tarjouskilpailut: Yhden tarjouksen näennäiskilpailutukset</h2>
      <p data-i18n="s3_sub">
        Klikkaa kilpailutuskorttia nähdäksesi, millä keinotekoisella ehdolla muut tarjoajat suljettiin ulos ja miten pk-yrittäjä voi vaatia syrjivän ehdon poistamista maksutta.
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
    Lähdeaineisto: Tutkihankintoja.fi, Hilma, KKV sidosyksikköselvitykset, MAO:154/2024 & PRH YTJ.
  </div>
  <div>
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
const fmtEUR = (n) => Math.round(Number(n)).toLocaleString('fi-FI') + ' €';

const I18N = {{
  fi: {{
    brand_title: "Suomen Talousinstituutti · Julkisten Hankintojen Tutkimus",
    brand_sub: "Tutkimusraportti · Klikkaa mitä tahansa korttia avataksesi selkokielisen analyysin",
    nav_sister: "← Tutkimus I: Yritys- & järjestötuet (11,5 mrd. €)",
    nav_xlsx: "Lataa Excel-malli (.xlsx)",
    hero_kicker: "JULKISET HANKINNAT · TUTKIMUSRAPORTTI 2026",
    hero_title: "38,7 miljardin euron ostokartelli: Miksi kuntien ja hyvinvointialueiden rahat eivät riitä hoitajiin?",
    hero_lead: "Valtio, 21 hyvinvointialuetta ja 308 kuntaa ostavat ulkopuolisilta yrityksiltä IT-järjestelmiä, hoivapalveluita ja urakoita <strong>38,7 miljardilla eurolla vuodessa</strong>. Tutkimuksemme osoittaa, että tästä potista <strong>1,5–3,5 miljardia euroa vuodessa</strong> hupenee laittomiin ”in-house”-välikäsiin, 2–3-kertaisiin alueellisiin ylihintoihin ja yhden tarjouksen näennäiskilpailutuksiin.",
    summary_box_title: "Miten luet tätä julkaisua? (Kaikki kortit ovat klikattavia)",
    summary_box_body: "<strong>Klikkaa mitä tahansa lukukorttia, kaavion vaihetta, IT-/talousyhtiötä, hintavertailua tai kilpailutusta</strong>. Saat esiin selkokielisen selityksen siitä, miten järjestely toimii — sekä halutessasi valmiin, maksuttoman (0 €) viranomaisilmoituksen Kilpailu- ja kuluttajavirastolle (KKV) tai omalle hyvinvointialueellesi.",
    kpi1_lbl: "Julkiset ulkoiset ostot",
    kpi1_sub: "Valtion, hyvinvointialueiden ja kuntien vuotuiset ostot yrityksiltä",
    click_1: "Klikkaa: Minne 38,7 mrd. € menee? →",
    kpi2_lbl: "Sidosyksikkö- eli ”in-house”-ketjutus",
    kpi2_sub: "7 välikäsiyhtiötä (Istekki, Apotti, Sarastia, 2M-IT, Monetra, Tiera, Valtori) ilman kilpailutusta",
    click_2: "Klikkaa: Mikä on 0,04 % ”kuoriosake”? →",
    kpi3_lbl: "Alueiden välinen 2–3x ylihinta",
    kpi3_sub: "Vuosisäästö, kun kalleimmat alueet laskevat yksikköhinnat parhaan neljänneksen tasolle",
    click_3: "Klikkaa: Miksi sama palvelu maksaa 3x? →",
    kpi4_lbl: "Yhden tarjouksen kilpailutukset",
    kpi4_sub: "Räätälöidyt tarjousehdot sulkevat pk-yritykset ulos ja nostavat hintoja 15–30 %",
    click_4: "Klikkaa: Miten ehdot räätälöidään? →",
    s1_title: "1. Miten ”kuoriosakkeella” kierretään kilpailutuslaki? (Klikkaa vaihetta tai yhtiötä)",
    s1_sub: "Korkein hallinto-oikeus ja markkinaoikeus (päätös MAO:154/2024) linjasivat, ettei hyvinvointialue saa ostaa palveluita ilman kilpailutusta yhtiöltä, josta se omistaa vain nimellisen murto-osan eikä käytä todellista määräysvaltaa.",
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
    f4_title: "504 milj. €/v ylihintaa veronmaksajille",
    f4_desc: "Paikalliset pk-yritykset eivät pääse tarjoamaan lainkaan, ja hyvinvointialue joutuu säästämään hoitajista maksaakseen IT-välikäsien laskut.",
    lbl_search: "Hae yhtiötä, hyvinvointialuetta tai palvelua",
    inhouse_heading: "Klikkaa sidosyksikköyhtiötä nähdäksesi rahan reitin ja valmiin 0 € KKV-ilmoituksen:",
    s2_title: "2. Alueellinen hintavertailu: Miksi sama palvelu maksaa naapurialueella 2–3 kertaa enemmän?",
    s2_sub: "Klikkaa mitä tahansa hintavertailukorttia nähdäksesi, kuinka paljon kyseinen hyvinvointialue maksaa ylihintaa verrattuna Suomen edullisimpaan neljännekseen (P25-vertailuhinta).",
    s3_title: "3. Räätälöidyt tarjouskilpailut: Yhden tarjouksen näennäiskilpailutukset",
    s3_sub: "Klikkaa kilpailutuskorttia nähdäksesi, millä keinotekoisella ehdolla muut tarjoajat suljettiin ulos ja miten pk-yrittäjä voi vaatia syrjivän ehdon poistamista maksutta.",
    s4_title: "4. Vaadi oman hyvinvointialueesi tai kuntasi ostolaskut julkisiksi (0 € tietopyyntö)",
    s4_sub: "Julkisuuslain (621/1999) mukaan jokaisella kansalaisella on oikeus saada hyvinvointialueen ja kunnan ostolaskut koneluettavassa muodossa 14 vuorokauden kuluessa. Klikkaa aluetta avataksesi valmiin tietopyynnön."
  }},
  en: {{
    brand_title: "Finnish Economic Institute (STI) · Public Procurement Audit",
    brand_sub: "Interactive Policy Report · Click any card for a plain-English explanation & 0 € legal action",
    nav_sister: "← Study I: Corporate & NGO Subsidies (€11.5B)",
    nav_xlsx: "Download Excel Model (.xlsx)",
    hero_kicker: "PUBLIC PROCUREMENT · RESEARCH REPORT 2026",
    hero_title: "The €38.7 Billion Procurement Cartel: Why Public Money Never Reaches Frontline Care",
    hero_lead: "Finland's state, 21 Wellbeing Counties, and 308 municipalities spend <strong>€38.7 billion per year</strong> buying IT systems, healthcare services, and contracts from outside vendors. Our research shows that <strong>€1.5B–€3.5B per year</strong> is lost to illegal 'in-house' middlemen, 2–3x regional price markups, and tailored single-bid tenders.",
    summary_box_title: "How to Read This Interactive Report (Every Card Is Clickable)",
    summary_box_body: "<strong>Click any metric card, flowchart step, IT/admin company, regional price comparison, or tender below</strong> to open a plain-English explanation of how the scheme works—plus a ready-to-send, zero-fee (€0) official filing to the Competition Authority (KKV) or your Wellbeing County.",
    kpi1_lbl: "Total Public External Purchases",
    kpi1_sub: "Annual purchases by the state, 21 Wellbeing Counties, and 308 municipalities",
    click_1: "Click: Where does the €38.7B go? →",
    kpi2_lbl: "In-House 'Sidosyksikkö' Middlemen",
    kpi2_sub: "7 middlemen (Istekki, Apotti, Sarastia, 2M-IT, Monetra, Tiera, Valtori) bypassing open tenders",
    click_2: "Click: What is the 0.04% 'token share' loophole? →",
    kpi3_lbl: "2–3x Regional Overpricing",
    kpi3_sub: "Annual savings when overpriced counties match top-quartile (P25) unit prices",
    click_3: "Click: Why does the same service cost 3x more? →",
    kpi4_lbl: "Single-Bid 'Rigged' Tenders",
    kpi4_sub: "Tailored requirements lock out SMEs and inflate prices by 15–30%",
    click_4: "Click: How are tender specs rigged? →",
    s1_title: "1. How a 0.04% 'Token Share' Bypasses Procurement Law (Click Any Step or Company)",
    s1_sub: "Finland's Market Court (MAO:154/2024) ruled that a public authority cannot buy services without competitive bidding from an in-house company in which it holds only a nominal token share and exercises no real control.",
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
    f4_title: "€504M/yr Overcharge to Taxpayers",
    f4_desc: "Local SMEs are locked out of the market, and counties cut frontline nurses to pay inflated IT and administrative bills.",
    lbl_search: "Search company, Wellbeing County, or service category",
    inhouse_heading: "Click any in-house intermediary to inspect the money trail & ready-to-send €0 KKV complaint:",
    s2_title: "2. Regional Price Audit: Why Does the Exact Same Service Cost 2–3x More Next Door?",
    s2_sub: "Click any regional price card to see how much that Wellbeing County overpays compared to Finland's best-performing quartile (P25 benchmark).",
    s3_title: "3. Tailored Tenders: Single-Bid 'Fake Competitions'",
    s3_sub: "Click any tender card to see which artificial requirement locked out competitors and how any entrepreneur can demand its removal for €0.",
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
          ? "Suomen julkisyhteisöt käyttävät joka vuosi 38,7 miljardia euroa tavaroiden, IT-järjestelmien, hoivapalveluiden, kuljetusten ja rakennusurakoiden ostamiseen yksityisiltä ja julkisomisteisilta yrityksiltä. Tämä on Suomen suurin yksittäinen verovarojen erä.Jo 5–9 prosentin tehostaminen kilpailua avaamalla säästää 2–3,5 miljardia euroa vuodessa."
          : "Finland's public sector spends €38.7 billion every year buying goods, IT systems, healthcare services, and construction from external vendors. Opening this market to genuine competition saves €2B–€3.5B per year without cutting a single frontline worker."}}</p>
      </div>`
    );
  }} else if (key === 'inhouse_leak') {{
    openModalHtml(
      fi ? "Mikä on sidosyksikkö- eli ”in-house”-kuoriosakekikkailu? (1,42 mrd. €/v)" : "What Is the In-House 'Token Share' Loophole? (€1.42B/yr)",
      fi ? "Markkinaoikeuden ennakkopäätös MAO:154/2024 & Hankintalaki 15 §" : "Market Court Precedent MAO:154/2024 & Procurement Act § 15",
      `<div class="modal-section">
        <h4>${{fi ? "Näin kilpailutuslaki kierretään" : "How the Law Is Bypassed"}}</h4>
        <p>${{fi
          ? "Hankintalain mukaan julkinen viranomainen saa ostaa palveluita ilman kilpailutusta vain omalta yksiköltään, jota se tosiasiallisesti hallitsee. Kunnat ja hyvinvointialueet ovat kuitenkin kiertäneet lakia ostamalla 0,04–1,2 prosentin nimellisen ”kuoriosakkeen” jättimäisistä yhteisyrityksistä (Istekki, Sarastia/Numera, 2M-IT, Monetra, Tiera, Apotti) ja tilaamalla niiltä 1,42 miljardilla eurolla palveluita ilman tarjouskilpailua."
          : "Under procurement law, a public buyer can skip competitive bidding only when buying from an entity it genuinely controls. Finnish counties and municipalities bypassed the law by buying a tiny 0.04%–1.2% 'token share' in giant joint companies and awarding them €1.42B/year without tenders."}}</p>
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
      fi ? "Yhden tarjouksen näennäiskilpailutukset (45 % hankinnoista)" : "Single-Bid 'Rigged' Tenders (45% of Public Procurements)",
      fi ? "Hilma-kilpailutusaineisto & Hankintalain 67 §" : "Hilma Tender Registry & Procurement Act § 67",
      `<div class="modal-section">
        <h4>${{fi ? "Miten tarjouspyyntö räätälöidään vanhalle toimittajalle?" : "How Tender Specifications Are Tailored to the Incumbent"}}</h4>
        <p>${{fi
          ? "Lähes puolessa Suomen julkisista hankinnoista saadaan vain 1–2 tarjousta. Tyypillinen keino on kirjata tarjouspyyntöön vaatimus, että tarjoajalla täytyy olla jo valmiiksi täsmälleen samanlainen sopimus viiden suomalaisen hyvinvointialueen kanssa tai tietty suljettu rajapinta. Tällöin vain nykyinen toimittaja voi jättää tarjouksen ja hinnoitella palvelun ilman kilpailupainetta."
          : "Nearly half of Finnish public tenders receive only 1–2 bids because tender specifications require hyper-specific incumbent references or proprietary interfaces—allowing the incumbent vendor to name its price."}}</p>
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
      s: fi ? "Hankintalain 15 §:n väärinkäyttö (todettu laittomaksi MAO:154/2024)" : "Abuse of Procurement Act § 15 (Ruled Illegal in MAO:154/2024)",
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
      t: fi ? "Vaihe 4: Lopputulos — 504 milj. €/v ylihintaa ja hoitajien irtisanomiset" : "Step 4: Outcome — €504M/yr Overcharge & Frontline Care Cuts",
      s: fi ? "Hallinto ja IT-välikädet syövät hoitobudjetin" : "Middleman Markups Drain the Frontline Care Budget",
      b: fi ? "Kun hyvinvointialue maksaa IT- ja taloushallintovälikäsille kymmeniä miljoonia ylihintaa, lakisääteinen alijäämä katetaan sulkemalla terveysasemia ja vähentämällä hoitohenkilökuntaa."
            : "When Wellbeing Counties overpay tens of millions to IT and administrative middlemen, they balance their budgets by closing local clinics and cutting nursing staff."
    }}
  }};
  const item = steps[step];
  openModalHtml(item.t, item.s, `<div class="modal-section"><h4>${{fi ? "Mitä tässä vaiheessa tapahtuu?" : "What Happens in This Step?"}}</h4><p>${{item.b}}</p></div>`);
}}

function openInhouseModal(idx) {{
  const f = APP.ssot.inhouse_leakage.flows[idx];
  const kkv = APP.kkv_filings[f.inhouse_y_tunnus];
  const oik = APP.oikaisu_filings[f.inhouse_y_tunnus];
  const fi = LANG === 'fi';
  const mailtoKkv = `mailto:${{kkv.recipient_email}}?subject=${{encodeURIComponent(kkv.subject)}}&body=${{encodeURIComponent(kkv.body)}}`;
  const mailtoOik = `mailto:${{oik.recipient_email}}?subject=${{encodeURIComponent(oik.subject)}}&body=${{encodeURIComponent(oik.body)}}`;

  openModalHtml(
    `${{f.inhouse_name}} (Y-tunnus: ${{f.inhouse_y_tunnus}})`,
    `${{f.buyer_name}} · ${{fi ? "Omistusosuus" : "Buyer Ownership"}}: ${{f.buyer_ownership_pct}} %`,
    `<div class="modal-section">
      <h4>${{fi ? "Selkokielinen kuvaus järjestelystä" : "Plain-English Explanation of This Arrangement"}}</h4>
      <p>${{fi
        ? `<strong>${{f.buyer_name}}</strong> ostaa <strong>${{f.inhouse_name}}</strong> -yhtiöltä palveluita <strong>${{fmtM(f.annual_direct_spend_m_eur)}}</strong> arvosta vuodessa ilman avointa kilpailutusta, vaikka ostajan omistusosuus yhtiöstä on vain <strong>${{f.buyer_ownership_pct}} %</strong>. Välikäsi perii arviolta <strong>${{f.intermediary_margin_pct}} %</strong> sisäisen katteen ja ketjuttaa työtä suoraan yksityisille suuryrityksille (<strong>${{f.private_subcontractors}}</strong>). Avoin kilpailutus säästäisi arviolta <strong>${{fmtM(f.estimated_annual_saving_m_eur)}}</strong> vuodessa.`
        : `<strong>${{f.buyer_name}}</strong> awards <strong>${{fmtM(f.annual_direct_spend_m_eur)}}/year</strong> without open tenders to <strong>${{f.inhouse_name}}</strong> despite holding only a <strong>${{f.buyer_ownership_pct}}%</strong> ownership share. The intermediary charges an estimated <strong>${{f.intermediary_margin_pct}}%</strong> markup while subcontracting to <strong>${{f.private_subcontractors}}</strong>. Open competition would save <strong>${{fmtM(f.estimated_annual_saving_m_eur)}}/year</strong>.`}}</p>
    </div>
    <div class="modal-section">
      <h4>${{fi ? "Valmis 0,00 € toimenpidepyyntö Kilpailu- ja kuluttajavirastolle (KKV) tai oikaisuvaatimus" : "Ready-to-Send €0.00 Official Complaint (KKV or Rectification Demand)"}}</h4>
      <p>${{fi
        ? "Markkinaoikeuden valitus maksaa yli 2 000 €, mutta alla oleva valvontailmoitus KKV:lle (kirjaamo@kkv.fi) tai hankintaoikaisuvaatimus ostajan kirjaamoon on jokaiselle kansalaiselle ja yrittäjälle 100 % maksuton (0,00 €):"
        : "Filing a Market Court appeal costs €2,120+, but submitting this statutory investigation request to the Competition Authority (kirjaamo@kkv.fi) or the buyer's registry costs €0.00:"}}</p>
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
  const r = APP.ssot.price_arbitrage.rows[idx];
  const fi = LANG === 'fi';
  openModalHtml(
    `${{r.entity_name}} — ${{r.cpv_category.split(' ')[1] || r.cpv_category}}`,
    `${{fi ? "Alueellinen yksikköhintavertailu" : "Regional Unit-Price Comparison"}} · ${{r.cpv_category}}`,
    `<div class="modal-section">
      <h4>${{fi ? "Mistä ylihinta syntyy?" : "Why Is This Region Overpaying?"}}</h4>
      <p>${{fi
        ? `<strong>${{r.entity_name}}</strong> maksaa tästä palvelusta <strong>${{Number(r.unit_price_eur).toLocaleString('fi-FI')}} € / ${{r.unit_name}}</strong>, kun Suomen edullisimman neljänneksen (P25-vertailutaso) yksikköhinta samalle palvelulle on <strong>${{Number(r.p25_benchmark_unit_price_eur).toLocaleString('fi-FI')}} € / ${{r.unit_name}}</strong> (+${{r.overprice_pct}} % ylihintaa). Jos alue kilpailuttaisi sopimuksen parhaan neljänneksen hintatasolle, veronmaksajat säästäisivät <strong>${{fmtEUR(r.annual_saving_eur)}}</strong> joka vuosi.`
        : `<strong>${{r.entity_name}}</strong> pays <strong>€${{Number(r.unit_price_eur).toLocaleString('fi-FI')}} per ${{r.unit_name}}</strong>, whereas Finland's top-quartile (P25) benchmark price for the exact same service is <strong>€${{Number(r.p25_benchmark_unit_price_eur).toLocaleString('fi-FI')}}</strong> (+${{r.overprice_pct}}% markup). Matching the P25 benchmark saves <strong>${{fmtEUR(r.annual_saving_eur)}}/year</strong>.`}}</p>
    </div>`
  );
}}

function openHilmaModal(idx) {{
  const t = APP.ssot.single_bid_cartels[idx];
  const fil = APP.hilma_filings[t.tender_id];
  const fi = LANG === 'fi';
  const mailto = `mailto:${{fil.recipient_email}}?subject=${{encodeURIComponent(fil.subject)}}&body=${{encodeURIComponent(fil.body)}}`;

  openModalHtml(
    `${{t.buyer_name}} (${{t.tender_id}})`,
    `${{t.cpv_code}} · ${{fi ? "Saadut tarjoukset" : "Bids Received"}}: ${{t.bids_received}} kpl`,
    `<div class="modal-section">
      <h4>${{fi ? "Miten kilpailutus rajattiin yhdelle tarjoajalle?" : "How Competitors Were Locked Out"}}</h4>
      <p>${{fi
        ? `Tässä <strong>${{fmtEUR(t.estimated_value_eur)}}</strong> arvoisessa hankinnassa saatiin vain <strong>${{t.bids_received}} tarjous(ta)</strong> (tarjousaika ${{t.days_open}} pv). Tarjouspyyntöön oli kirjattu rajoittava ehto: <em>”${{t.tailored_requirement_note}}”</em>. Kun muut yritykset eivät voineet jättää tarjousta, hinta jäi arviolta 25 % kilpailtua markkinahintaa korkeammaksi (vuosisäästöpotentiaali <strong>${{fmtEUR(t.expected_annual_saving_eur)}}</strong>).`
        : `This <strong>${{fmtEUR(t.estimated_value_eur)}}</strong> procurement received only <strong>${{t.bids_received}} bid(s)</strong> (${{t.days_open}} days open) due to a tailored requirement: <em>"${{t.tailored_requirement_note}}"</em>. Opening the tender to SMEs saves an estimated <strong>${{fmtEUR(t.expected_annual_saving_eur)}}/year</strong>.`}}</p>
    </div>
    <div class="modal-section">
      <h4>${{fi ? "Valmis 0,00 € vaatimus syrjivän tarjousehdon poistamiseksi (Hankintalaki 67 §)" : "Ready-to-Send €0.00 Demand to Remove Tailored Spec (Procurement Act § 67)"}}</h4>
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
        ? `Tämä valmis tietopyyntö velvoittaa <strong>${{b.entity_name}}</strong> -viranomaisen luovuttamaan 14 vuorokauden kuluessa koneluettavan ostolaskuaineiston (CSV/XLSX) sekä sidosyksikköjen osakassopimukset ja suorahankintapäätökset maksutta.`
        : `This statutory request requires <strong>${{b.entity_name}}</strong> to release machine-readable purchase invoice ledgers (CSV/XLSX) and in-house shareholder agreements within 14 days at zero cost.`}}</p>
      <textarea id="active-legal-textarea" class="legal-box" readonly>${{fil.body}}</textarea>
      <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <button class="btn-primary" onclick="copyLegalBox(this)">${{fi ? "Kopioi tietopyyntö leikepöydälle" : "Copy FOIA Request"}}</button>
        <a class="btn-secondary" href="${{mailto}}">${{fi ? "Avaa sähköpostissa (" + b.kirjaamo_email + ")" : "Open in Email"}}</a>
      </div>
    </div>`
  );
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
  const q = (document.getElementById('search-box').value || '').toLowerCase().trim();
  const fi = LANG === 'fi';

  // 1. In-house cards
  let inHtml = '';
  APP.ssot.inhouse_leakage.flows.forEach((f, idx) => {{
    const txt = (f.inhouse_name + ' ' + f.inhouse_y_tunnus + ' ' + f.buyer_name + ' ' + f.private_subcontractors).toLowerCase();
    if (q && !txt.includes(q)) return;
    const isToken = f.legal_status.includes('LAITON_KUORIOSAKE');
    const accent = isToken ? 'red-accent' : 'amber-accent';
    const badge = isToken
      ? `<span class="badge badge-red">${{fi ? 'Kuoriosake (' + f.buyer_ownership_pct + ' %)' : 'Token Share (' + f.buyer_ownership_pct + '%)'}}</span>`
      : `<span class="badge badge-amber">${{fi ? 'Suorahankintamonopoli' : 'In-House Monopoly'}}</span>`;
    inHtml += `<div class="story-card ${{accent}} clickable-card" onclick="openInhouseModal(${{idx}})">
      <div class="story-top">
        <div class="story-header">
          <h3>${{f.inhouse_name}}</h3>
          ${{badge}}
        </div>
        <div class="story-meta">Y-tunnus: ${{f.inhouse_y_tunnus}} · ${{fi ? 'Tilaaja:' : 'Buyer:'}} ${{f.buyer_name}}</div>
        <p class="story-commentary">${{fi
          ? `${{f.buyer_name}} omistaa yhtiöstä vain ${{f.buyer_ownership_pct}} %, mutta ostaa siltä ilman kilpailutusta ${{fmtM(f.annual_direct_spend_m_eur)}}/v. Välikäsi ketjuttaa työtä pörssiyhtiöille (${{f.private_subcontractors}}).`
          : `${{f.buyer_name}} owns just ${{f.buyer_ownership_pct}}% yet awards ${{fmtM(f.annual_direct_spend_m_eur)}}/yr without tenders. Subcontracted to ${{f.private_subcontractors}}.`}}</p>
      </div>
      <div>
        <div class="metrics-strip">
          <div><span>${{fi ? 'Suora osto / v' : 'Direct Spend'}}</span><strong>${{fmtM(f.annual_direct_spend_m_eur)}}</strong></div>
          <div><span>${{fi ? 'Välikäden kate' : 'Markup'}}</span><strong style="color:var(--amber)">${{f.intermediary_margin_pct}} %</strong></div>
          <div><span>${{fi ? 'Vuosisäästö' : 'Annual Saving'}}</span><strong style="color:var(--red)">${{fmtM(f.estimated_annual_saving_m_eur)}}</strong></div>
        </div>
        <div class="click-hint">${{fi ? 'Klikkaa: Avaa analyysi & valmis 0 € KKV-ilmoitus →' : 'Click: Open analysis & €0 KKV complaint →'}}</div>
      </div>
    </div>`;
  }});
  document.getElementById('inhouse-cards').innerHTML = inHtml;

  // 2. Arbitrage cards (show only rows where overprice_pct > 0 so every card is an actionable finding)
  let arbHtml = '';
  APP.ssot.price_arbitrage.rows.forEach((r, idx) => {{
    if (r.overprice_pct <= 0) return;
    const txt = (r.entity_name + ' ' + r.cpv_category).toLowerCase();
    if (q && !txt.includes(q)) return;
    arbHtml += `<div class="story-card amber-accent clickable-card" onclick="openArbitrageModal(${{idx}})">
      <div class="story-top">
        <div class="story-header">
          <h3>${{r.entity_name}}</h3>
          <span class="badge badge-red">+${{r.overprice_pct}} % ${{fi ? 'ylihinta' : 'markup'}}</span>
        </div>
        <div class="story-meta">${{r.cpv_category}}</div>
        <p class="story-commentary">${{fi
          ? `Maksaa ${{Number(r.unit_price_eur).toLocaleString('fi-FI')}} € / ${{r.unit_name}}, kun parhaan neljänneksen (P25) vertailuhinta Suomessa on ${{Number(r.p25_benchmark_unit_price_eur).toLocaleString('fi-FI')}} €.`
          : `Pays €${{Number(r.unit_price_eur).toLocaleString('fi-FI')}} per ${{r.unit_name}} vs. top-quartile (P25) benchmark of €${{Number(r.p25_benchmark_unit_price_eur).toLocaleString('fi-FI')}}.`}}</p>
      </div>
      <div>
        <div class="metrics-strip">
          <div><span>${{fi ? 'Alueen hinta' : 'Unit Price'}}</span><strong style="color:var(--red)">${{Number(r.unit_price_eur).toLocaleString('fi-FI')}} €</strong></div>
          <div><span>${{fi ? 'P25-vertailu' : 'P25 Benchmark'}}</span><strong style="color:var(--accent-dark)">${{Number(r.p25_benchmark_unit_price_eur).toLocaleString('fi-FI')}} €</strong></div>
          <div><span>${{fi ? 'Säästö / v' : 'Saving / yr'}}</span><strong>${{fmtM(r.annual_saving_eur / 1e6)}}</strong></div>
        </div>
        <div class="click-hint">${{fi ? 'Klikkaa: Katso yksikköhintojen erittely →' : 'Click: Inspect unit-price breakdown →'}}</div>
      </div>
    </div>`;
  }});
  document.getElementById('arbitrage-cards').innerHTML = arbHtml;

  // 3. Hilma single-bid cards
  let hilmaHtml = '';
  APP.ssot.single_bid_cartels.forEach((t, idx) => {{
    const txt = (t.buyer_name + ' ' + t.tender_id + ' ' + t.cpv_code + ' ' + t.tailored_requirement_note).toLowerCase();
    if (q && !txt.includes(q)) return;
    hilmaHtml += `<div class="story-card red-accent clickable-card" onclick="openHilmaModal(${{idx}})">
      <div class="story-top">
        <div class="story-header">
          <h3>${{t.buyer_name}}</h3>
          <span class="badge badge-red">${{t.bids_received}} ${{fi ? 'tarjous(ta)' : 'bid(s)'}}</span>
        </div>
        <div class="story-meta">${{t.tender_id}} · ${{t.cpv_code}}</div>
        <p class="story-commentary">${{t.tailored_requirement_note}}</p>
      </div>
      <div>
        <div class="metrics-strip">
          <div><span>${{fi ? 'Hankinnan arvo' : 'Contract Value'}}</span><strong>${{fmtM(t.estimated_value_eur / 1e6)}}</strong></div>
          <div><span>${{fi ? 'Tarjousaika' : 'Days Open'}}</span><strong>${{t.days_open}} pv</strong></div>
          <div><span>${{fi ? 'Säästöpotentiaali' : 'Est. Saving'}}</span><strong style="color:var(--red)">${{fmtM(t.expected_annual_saving_eur / 1e6)}}</strong></div>
        </div>
        <div class="click-hint">${{fi ? 'Klikkaa: Avaa 0 € vaatimus tarjousehdon poistamiseksi →' : 'Click: Open €0 tender spec challenge →'}}</div>
      </div>
    </div>`;
  }});
  document.getElementById('hilma-cards').innerHTML = hilmaHtml;

  // 4. Buyer FOIA directory cards
  let buyerHtml = '';
  APP.ssot.public_buyer_directory.forEach((b, idx) => {{
    const txt = (b.entity_name + ' ' + b.y_tunnus + ' ' + b.kirjaamo_email).toLowerCase();
    if (q && !txt.includes(q)) return;
    buyerHtml += `<div class="story-card green-accent clickable-card" onclick="openBuyerFoiaModal(${{idx}})">
      <div class="story-top">
        <div class="story-header">
          <h3>${{b.entity_name}}</h3>
          <span class="badge badge-green">0,00 € FOIA</span>
        </div>
        <div class="story-meta">Y-tunnus: ${{b.y_tunnus}} · ${{b.kirjaamo_email}}</div>
        <p class="story-commentary">${{fi
          ? `Vaadi viranomaisen ostolaskut (CSV/XLSX) ja sidosyksikköjen suorahankintasopimukset julkisuuslain 13 §:n nojalla 14 vuorokaudessa.`
          : `Demand machine-readable purchase invoices (CSV/XLSX) and in-house contracts within 14 days under the Openness Act.`}}</p>
      </div>
      <div class="click-hint">${{fi ? 'Klikkaa: Avaa valmis tietopyyntö (' + b.kirjaamo_email + ') →' : 'Click: Open ready-to-send FOIA request →'}}</div>
    </div>`;
  }});
  document.getElementById('buyer-cards').innerHTML = buyerHtml;
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
