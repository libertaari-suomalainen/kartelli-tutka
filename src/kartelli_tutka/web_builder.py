"""
Kartelli-Tutka Zero-Backend Static Web Explorer Compiler.
Compiles the canonical SSOT payload and pre-generated legal filings into a self-contained
single-page application (`dist/index.html`) that runs 100% offline or on static hosting ($0/mo).
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

    # Pre-compile deterministic legal filings for every flow, tender, and public buyer
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
<title>Kartelli-Purkaja 2026 — Julkisten Hankintojen (38,7 Mrd €) Röntgen & 1-Click Oikeusohjus</title>
<style>
  :root {{
    --bg: #0b1120;
    --panel: #111827;
    --panel-alt: #1e293b;
    --border: #334155;
    --text: #f8fafc;
    --muted: #94a3b8;
    --red: #ef4444;
    --red-bg: rgba(239, 68, 68, 0.14);
    --amber: #f59e0b;
    --amber-bg: rgba(245, 158, 11, 0.14);
    --green: #10b981;
    --green-bg: rgba(16, 185, 129, 0.14);
    --blue: #3b82f6;
    --blue-bg: rgba(59, 130, 246, 0.15);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.45;
    padding: 20px 28px 60px;
  }}
  .container {{ max-width: 1440px; margin: 0 auto; }}
  header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
    padding-bottom: 18px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
  }}
  .badge-Top {{
    display: inline-block;
    background: var(--red-bg);
    color: #fca5a5;
    border: 1px solid var(--red);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 3px 10px;
    border-radius: 999px;
    margin-bottom: 8px;
  }}
  h1 {{ font-size: 26px; font-weight: 800; letter-spacing: -0.02em; }}
  .subtitle {{ color: var(--muted); font-size: 14px; margin-top: 4px; max-width: 880px; }}
  .header-actions {{ display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }}
  .btn {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    border-radius: 6px;
    font-size: 12.5px;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid transparent;
    text-decoration: none;
    transition: all 0.15s ease;
  }}
  .btn-red {{ background: var(--red); color: #fff; }}
  .btn-red:hover {{ background: #dc2626; }}
  .btn-blue {{ background: var(--blue); color: #fff; }}
  .btn-blue:hover {{ background: #2563eb; }}
  .btn-outline {{ background: var(--panel-alt); color: var(--text); border-color: var(--border); }}
  .btn-outline:hover {{ border-color: var(--blue); background: #26354d; }}
  .btn-green {{ background: var(--green); color: #052e16; font-weight: 700; }}

  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 20px;
  }}
  .kpi-card {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 18px;
  }}
  .kpi-label {{ font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; }}
  .kpi-val {{ font-size: 28px; font-weight: 800; margin: 6px 0 4px; }}
  .kpi-sub {{ font-size: 12px; color: var(--muted); }}
  .text-red {{ color: #f87171; }}
  .text-amber {{ color: #fbbf24; }}
  .text-green {{ color: #34d399; }}
  .text-blue {{ color: #60a5fa; }}

  .controls-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 16px;
  }}
  .control-group {{ display: flex; align-items: center; gap: 10px; font-size: 13px; }}
  .control-group label {{ color: var(--muted); font-weight: 600; }}
  select, input[type="text"] {{
    background: var(--panel-alt);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 13px;
  }}

  .section-box {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 22px;
  }}
  .section-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
  }}
  .section-title {{ font-size: 17px; font-weight: 700; }}
  .section-desc {{ font-size: 13px; color: var(--muted); }}

  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{
    text-align: left;
    padding: 10px 10px;
    background: var(--panel-alt);
    color: var(--muted);
    font-weight: 600;
    font-size: 11.5px;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    border-bottom: 1px solid var(--border);
  }}
  td {{
    padding: 11px 10px;
    border-bottom: 1px solid rgba(51, 65, 85, 0.6);
    vertical-align: middle;
  }}
  tr:hover td {{ background: rgba(30, 41, 59, 0.55); }}
  .pill {{
    display: inline-block;
    padding: 3px 9px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 700;
    white-space: nowrap;
  }}
  .pill-red {{ background: var(--red-bg); color: #fca5a5; border: 1px solid rgba(239,68,68,0.4); }}
  .pill-amber {{ background: var(--amber-bg); color: #fcd34d; border: 1px solid rgba(245,158,11,0.4); }}
  .pill-green {{ background: var(--green-bg); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.4); }}

  .flow-arrow {{ color: var(--amber); font-weight: 700; padding: 0 4px; }}
  .bar-track {{
    width: 140px;
    height: 8px;
    background: #1e293b;
    border-radius: 4px;
    overflow: hidden;
    display: inline-block;
    vertical-align: middle;
    margin-right: 8px;
  }}
  .bar-fill {{ height: 100%; border-radius: 4px; }}

  /* Modal */
  .modal-backdrop {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(2, 6, 23, 0.82);
    z-index: 1000;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }}
  .modal-backdrop.active {{ display: flex; }}
  .modal {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    max-width: 880px;
    width: 100%;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7);
  }}
  .modal-head {{
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .modal-body {{ padding: 18px 20px; overflow-y: auto; }}
  .modal-body pre {{
    background: #090d16;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
    color: #e2e8f0;
    font-family: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
    font-size: 12.5px;
    white-space: pre-wrap;
    line-height: 1.5;
  }}
  .modal-foot {{
    padding: 14px 20px;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }}
</style>
</head>
<body>
<div class="container">
  <header>
    <div>
      <span class="badge-Top">100% Avoin Data • Hankintalaki 15 § & MAO:154/2024 • 0 € Käsittelymaksu</span>
      <h1>KARTELLI-PURKAJA — Julkisten Hankintojen (38,7 Mrd €/v) Röntgen & Oikeusohjus</h1>
      <p class="subtitle">
        Paljastaa hyvinvointialueiden ja kuntien laittomat <strong>0,04 % – 1,2 % sidosyksikkösuorahankinnat</strong> (Istekki, 2M-IT, Sarastia/Numera, Monetra, Tiera, Apotti),
        alueiden väliset <strong>2–3x yksikköhintaerot</strong> sekä <strong>1 tarjouksen Hilma-kartellit</strong> — ja generoi valmiin KKV-tutkintapyynnön tai hankintaoikaisun yhdellä klikkauksella.
      </p>
    </div>
    <div class="header-actions">
      <a class="btn btn-green" href="Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx" download>⬇ Lataa CFO / VM Excel-Leikkuri (.xlsx)</a>
      <button class="btn btn-red" onclick="openKKVModal('2292633-0')">⚖ Kokeile 1-Click KKV-Tutkintapyyntöä (0 €)</button>
    </div>
  </header>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Julkiset Ulkoiset Ostot (S.13)</div>
      <div class="kpi-val text-blue">38,70 Mrd €/v</div>
      <div class="kpi-sub">Valtio 13,9B € • 21 HVA 13,8B € • 308 Kuntaa 11,0B €</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Sidosyksikköjen Ketjutettu Laskutus</div>
      <div class="kpi-val text-amber" id="kpi-inhouse-total">1 420,0 M€/v</div>
      <div class="kpi-sub">Laiton &lt;<span id="kpi-thresh-label">10</span>% näennäisomistus: <strong class="text-red" id="kpi-illegal-spend">745,0 M€/v</strong></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Sidosyksikkökartellien Purkusäästö</div>
      <div class="kpi-val text-green" id="kpi-inhouse-saving">540,3 M€/v</div>
      <div class="kpi-sub">Välikäsikate (21–30 %) + kilpailuttamaton alihankintalisä</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Kansallinen Kokonaissäästöhaarukka</div>
      <div class="kpi-val text-green" id="kpi-total-national">2,46 Mrd €/v</div>
      <div class="kpi-sub">Sidosyksiköt + P25-hintakuri + Hilma 1-tarjouskilpailutus</div>
    </div>
  </div>

  <div class="controls-bar">
    <div class="control-group">
      <label for="sel-threshold">Sidosyksikön lakisääteinen omistusraja (Hankintalaki 15 §):</label>
      <select id="sel-threshold" onchange="recalcDashboard()">
        <option value="10" selected>10,0 % vähimmäisomistusraja (Hallitusohjelma & MAO:154/2024)</option>
        <option value="5">5,0 % määräysvaltaraja (Nykyinen KHO / MAO tulkintakynnys)</option>
      </select>
    </div>
    <div class="control-group">
      <label for="sel-cpv">Suodata yksikköhintakategoria (P25-Arbitraasi):</label>
      <select id="sel-cpv" onchange="renderArbitrageTable()">
        <option value="ALL">Kaikki 5 kärkikategoriaa (Vuokralääkärit, IT, APTJ, Hoiva, Kuljetukset)</option>
        <option value="85121000-LocumMD">85121000 — Vuokralääkärit & Päivystys (€/h)</option>
        <option value="72260000-ITWorkstation">72260000 — Työasema- ja lähitukipalvelut (€/HTV/v)</option>
        <option value="48814000-EHR">48814000 — Potilastietojärjestelmät Apotti/Lifecare/Esko (€/lääkäri/v)</option>
        <option value="85311100-ElderlyCare">85311100 — Ympärivuorokautinen hoiva (€/hoitopäivä)</option>
        <option value="60130000-SoteTransport">60130000 — Sote- ja koulukuljetukset (€/matka)</option>
      </select>
    </div>
  </div>

  <!-- SECTION 1: SIDOSYKSIKKÖ MONEY TRAIL -->
  <div class="section-box">
    <div class="section-header">
      <div>
        <div class="section-title">1. Sidosyksikkökartellien Rahavirta-Röntgen (Hankintalaki 15 § & MAO:154/2024)</div>
        <div class="section-desc">
          Hyvinvointialue tai kunta ostaa 0,04 % – 1,2 % "kuoriosakkeen" ja ohjaa satoja miljoonia ilman kilpailutusta sidosyksikölle, joka ottaa 21–30 % katteen ja ketjuttaa työn suoraan TietoEvrylle tai CGI:lle.
        </div>
      </div>
    </div>
    <table>
      <thead>
        <tr>
          <th>Julkinen Ostajaryhmä</th>
          <th>Omistus-%</th>
          <th>Sidosyksikkö (Välikäsi) &rarr; Todelliset Alihankkijat</th>
          <th>Vuosiostot</th>
          <th>Välikäsikate + Ylihinta</th>
          <th>Vuosisäästö</th>
          <th>1-Click Oikeusohjukset (0 € maksu)</th>
        </tr>
      </thead>
      <tbody id="tbody-inhouse"></tbody>
    </table>
  </div>

  <!-- SECTION 2: CROSS-COUNTY PRICE GOUGING RADAR -->
  <div class="section-box">
    <div class="section-header">
      <div>
        <div class="section-title">2. Hyvinvointialueiden & Kuntien Yksikköhintojen Ylihintatutka (P25-Arbitraasi)</div>
        <div class="section-desc">
          Vertaa saman palvelun yksikköhintaa eri hyvinvointialueiden välillä. Kun yli P25-vertailutason maksavat alueet leikkaavat yksikköhinnan parhaan neljänneksen (P25) tasolle, syntyy välitön säästö ilman yhdenkään hoitajan tai lääkärin irtisanomista.
        </div>
      </div>
      <div>
        <span class="pill pill-green" id="arb-total-badge">Otoksen P25-säästö: 0,0 M€/v</span>
      </div>
    </div>
    <table>
      <thead>
        <tr>
          <th>Julkinen Ostaja (HVA / Kunta)</th>
          <th>CPV-Kategoria</th>
          <th>Volyymi / v</th>
          <th>Maksettu Yksikköhinta</th>
          <th>Kansallinen P25-Hinta</th>
          <th>Ylihinta vs. P25</th>
          <th>P25-Vuosisäästö</th>
          <th>Haasta / Tietopyyntö</th>
        </tr>
      </thead>
      <tbody id="tbody-arbitrage"></tbody>
    </table>
  </div>

  <!-- SECTION 3: HILMA 1-BID CARTELS & JULKISUUSLAKI FOIA -->
  <div class="section-box">
    <div class="section-header">
      <div>
        <div class="section-title">3. Hilma 1–2 Tarjouksen Kartellitutka & Julkisuuslain (13 §) Ostolasku-Avaaja</div>
        <div class="section-desc">
          45 % Hilma-kilpailutuksista saa vain 1–2 tarjousta, koska soveltuvuusvaatimukset on räätälöity nykyiselle toimittajalle. Yhden klikkauksen vaatimuksella pk-yritys pakottaa hankintayksikön poistamaan syrjivät ehdot (Hankintalaki 67 §).
        </div>
      </div>
    </div>
    <table>
      <thead>
        <tr>
          <th>Hilma-ID & Ostaja</th>
          <th>Kategoria & Nykyinen Toimittaja</th>
          <th>Sopimusarvo</th>
          <th>Saadut Tarjoukset</th>
          <th>PK-Haastajia Markkinassa</th>
          <th>Tunnistettu Lukitusmekanismi</th>
          <th>Odotettu Säästö (-25%)</th>
          <th>1-Click Toimenpide</th>
        </tr>
      </thead>
      <tbody id="tbody-hilma"></tbody>
    </table>
  </div>

  <!-- SECTION 4: 21-COUNTY FOlA TRANSPARENCY TABLE -->
  <div class="section-box">
    <div class="section-header">
      <div>
        <div class="section-title">4. Ostolaskudatan Julkisuustutka (Julkisuuslaki 621/1999 13 § & 16 §)</div>
        <div class="section-desc">
          Salassapidon murtaminen: jokaisella kansalaisella, toimittajalla ja yrittäjällä on lakisääteinen oikeus saada hyvinvointialueen ja kunnan ostolaskut koneluettavassa CSV/XLSX-muodossa 14 vuorokaudessa.
        </div>
      </div>
    </div>
    <table>
      <thead>
        <tr>
          <th>Julkinen Yksikkö</th>
          <th>Y-tunnus</th>
          <th>Ulkoiset Ostot (M€/v)</th>
          <th>Käytetyt Sidosyksiköt</th>
          <th>Avoin Ostolaskudata Verkossa?</th>
          <th>Pakota Luovutus (14 vrk lakiraja)</th>
        </tr>
      </thead>
      <tbody id="tbody-buyers"></tbody>
    </table>
  </div>
</div>

<!-- LEGAL FILING MODAL -->
<div class="modal-backdrop" id="legal-modal">
  <div class="modal">
    <div class="modal-head">
      <div>
        <div style="font-size:15px;font-weight:800;" id="modal-title">Valmis Viranomaisasiakirja (0,00 € käsittelymaksu)</div>
        <div style="font-size:12px;color:var(--muted);" id="modal-recipient">Vastaanottaja: kirjaamo@kkv.fi</div>
      </div>
      <button class="btn btn-outline" onclick="closeModal()">✕ Sulje</button>
    </div>
    <div class="modal-body">
      <pre id="modal-content"></pre>
    </div>
    <div class="modal-foot">
      <span style="font-size:12px;color:var(--muted);">Lakiviitteet tarkistettu: Hankintalaki (1397/2016) 15 §, 67 §, 133 §, 139 § • MAO:154/2024 • Julkisuuslaki (621/1999) 13 § & 16 §</span>
      <div style="display:flex;gap:8px;">
        <button class="btn btn-outline" onclick="copyModalText()">📋 Kopioi teksti</button>
        <button class="btn btn-blue" onclick="downloadModalText()">⬇ Lataa asiakirja (.txt)</button>
        <a class="btn btn-red" id="modal-mailto" href="#">✉ Avaa valmiina sähköpostina</a>
      </div>
    </div>
  </div>
</div>

<script>
const DATA = {json_blob};
let currentModalDoc = {{ subject: "", body: "", recipient_email: "" }};

function fmtM(val) {{
  return val.toLocaleString("fi-FI", {{ minimumFractionDigits: 1, maximumFractionDigits: 1 }}) + " M€";
}}
function fmtEur(val) {{
  return val.toLocaleString("fi-FI", {{ maximumFractionDigits: 0 }}) + " €";
}}

function recalcDashboard() {{
  const thresh = parseFloat(document.getElementById("sel-threshold").value);
  document.getElementById("kpi-thresh-label").textContent = thresh.toFixed(0);

  let totalSpend = 0;
  let illegalSpend = 0;
  let totalSaving = 0;

  const tbody = document.getElementById("tbody-inhouse");
  tbody.innerHTML = "";

  DATA.ssot.inhouse_flows.forEach(f => {{
    totalSpend += f.annual_spend_m_eur;
    const isIllegal = f.buyer_equity_share_pct < thresh;
    if (isIllegal) illegalSpend += f.annual_spend_m_eur;
    totalSaving += f.recoverable_saving_m_eur;

    const tr = document.createElement("tr");
    const statusBadge = isIllegal
      ? `<span class="pill pill-red">LAITON (${{f.buyer_equity_share_pct.toFixed(2).replace('.', ',')}} % &lt; ${{thresh}} %)</span>`
      : `<span class="pill pill-amber">YLIHINTAINEN MONOPOLI (${{f.buyer_equity_share_pct.toFixed(1).replace('.', ',')}} %)</span>`;

    tr.innerHTML = `
      <td><strong>${{f.buyer_name}}</strong><br><span style="font-size:11.5px;color:var(--muted)">${{f.legal_status}}</span></td>
      <td>${{statusBadge}}</td>
      <td>
        <strong>${{f.inhouse_vendor}}</strong> <span style="color:var(--muted);font-size:11.5px">(${{f.inhouse_y_tunnus}})</span>
        <span class="flow-arrow">&rarr;</span>
        <span style="color:#93c5fd">${{f.subcontractor_vendor}}</span>
      </td>
      <td><strong>${{fmtM(f.annual_spend_m_eur)}}/v</strong></td>
      <td><span class="pill pill-amber">+${{f.inhouse_markup_pct}}% välikäsi / +${{f.subcontractor_uncompeted_premium_pct}}% alihankinta</span></td>
      <td><strong class="text-green">${{fmtM(f.recoverable_saving_m_eur)}}/v</strong></td>
      <td>
        <div style="display:flex;gap:6px;flex-wrap:wrap;">
          <button class="btn btn-red" style="padding:5px 9px;font-size:11.5px" onclick="openKKVModal('${{f.inhouse_y_tunnus}}')">⚖ KKV-Valitus (0 €)</button>
          <button class="btn btn-outline" style="padding:5px 9px;font-size:11.5px" onclick="openOikaisuModal('${{f.inhouse_y_tunnus}}')">🏛 Hankintaoikaisu</button>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  }});

  document.getElementById("kpi-inhouse-total").textContent = fmtM(totalSpend) + "/v";
  document.getElementById("kpi-illegal-spend").textContent = fmtM(illegalSpend) + "/v";
  document.getElementById("kpi-inhouse-saving").textContent = fmtM(totalSaving) + "/v";
}}

function renderArbitrageTable() {{
  const filter = document.getElementById("sel-cpv").value;
  const tbody = document.getElementById("tbody-arbitrage");
  tbody.innerHTML = "";
  let totalArbSaving = 0;

  DATA.ssot.arbitrage_rows.forEach(r => {{
    if (filter !== "ALL" && r.cpv_category !== filter) return;
    totalArbSaving += r.recoverable_saving_eur;

    const pct = r.overpay_vs_p25_pct;
    const barWidth = Math.min(100, Math.round((r.unit_price_eur / r.max_peer_eur) * 100));
    const barColor = pct > 35 ? "var(--red)" : (pct > 0 ? "var(--amber)" : "var(--green)");
    const badge = pct > 0
      ? `<span class="pill pill-red">+${{pct.toFixed(1).replace('.', ',')}} % yli P25</span>`
      : `<span class="pill pill-green">P25-Vertailutaso (Tehokas)</span>`;

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${{r.entity_name}}</strong></td>
      <td><span style="color:var(--muted)">${{r.cpv_category}}</span></td>
      <td>${{r.annual_units.toLocaleString("fi-FI")}} ${{r.unit_name}}</td>
      <td>
        <div class="bar-track"><div class="bar-fill" style="width:${{barWidth}}%;background:${{barColor}}"></div></div>
        <strong>${{r.unit_price_eur.toLocaleString("fi-FI")}} €</strong>
      </td>
      <td><strong class="text-green">${{r.p25_benchmark_eur.toLocaleString("fi-FI")}} €</strong></td>
      <td>${{badge}}</td>
      <td><strong class="${{r.recoverable_saving_eur > 0 ? 'text-green' : ''}}">${{fmtEur(r.recoverable_saving_eur)}}/v</strong></td>
      <td>
        ${{r.recoverable_saving_eur > 0
          ? `<a class="btn btn-outline" style="padding:4px 9px;font-size:11.5px" href="mailto:${{r.kirjaamo_email}}?subject=${{encodeURIComponent('Vaihtoehtoinen tarjous & Hankintaoikaisu: ' + r.cpv_category + ' (' + r.entity_name + ')')}}">📉 Tarjoa -20 % alle</a>`
          : `<span style="color:var(--muted);font-size:11.5px">Vertailukärki</span>`
        }}
      </td>
    `;
    tbody.appendChild(tr);
  }});

  document.getElementById("arb-total-badge").textContent =
    "Valitun otoksen P25-säästö: " + (totalArbSaving / 1e6).toLocaleString("fi-FI", {{ minimumFractionDigits: 1, maximumFractionDigits: 1 }}) + " M€/v";
}}

function renderHilmaTable() {{
  const tbody = document.getElementById("tbody-hilma");
  tbody.innerHTML = "";
  DATA.ssot.flagged_hilma_tenders.forEach(t => {{
    const bidBadge = t.is_direct_award
      ? `<span class="pill pill-red">0 tarjousta (Suorahankinta)</span>`
      : `<span class="pill pill-amber">${{t.bids_received}} tarjous(ta)</span>`;
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${{t.tender_id}}</strong><br><span style="color:var(--muted);font-size:12px">${{t.buyer_name}}</span></td>
      <td><strong>${{t.cpv_code}}</strong><br><span style="color:#93c5fd;font-size:12px">${{t.incumbent_vendor}}</span></td>
      <td><strong>${{fmtEur(t.contract_value_eur)}}</strong></td>
      <td>${{bidBadge}}</td>
      <td><span class="pill pill-green">${{t.qualified_eu_sme_pool_size}} kelpoista PK-yritystä</span></td>
      <td style="max-width:290px;font-size:12px;color:#cbd5e1">${{t.lockout_reason}}</td>
      <td><strong class="text-green">${{fmtEur(t.expected_annual_saving_eur)}}/v</strong></td>
      <td>
        <button class="btn btn-blue" style="padding:5px 10px;font-size:11.5px" onclick="openHilmaModal('${{t.tender_id}}')">⚡ Avaa kilpailulle (67 §)</button>
      </td>
    `;
    tbody.appendChild(tr);
  }});
}}

function renderBuyersTable() {{
  const tbody = document.getElementById("tbody-buyers");
  tbody.innerHTML = "";
  DATA.ssot.public_buyer_directory.forEach(b => {{
    const status = b.publishes_open_invoices
      ? `<span class="pill pill-green">Julkaisee avoimena</span>`
      : `<span class="pill pill-red">Piilottaa rivitason ostolaskut</span>`;
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${{b.entity_name}}</strong></td>
      <td><code>${{b.y_tunnus}}</code></td>
      <td><strong>${{fmtM(b.annual_purchases_m_eur)}}/v</strong></td>
      <td style="color:var(--muted)">${{b.primary_inhouse_shells}}</td>
      <td>${{status}}</td>
      <td>
        <button class="btn btn-outline" style="padding:5px 10px;font-size:11.5px" onclick="openFoiaModal('${{b.y_tunnus}}')">📂 1-Click Julkisuuslaki 13 § Tietopyyntö</button>
      </td>
    `;
    tbody.appendChild(tr);
  }});
}}

function showModal(doc, titleLabel) {{
  currentModalDoc = doc;
  document.getElementById("modal-title").textContent = titleLabel;
  document.getElementById("modal-recipient").textContent = "Vastaanottaja: " + doc.recipient_email + " | Käsittelymaksu: " + doc.filing_fee_eur + " €";
  document.getElementById("modal-content").textContent = doc.body;
  document.getElementById("modal-mailto").href =
    "mailto:" + encodeURIComponent(doc.recipient_email) +
    "?subject=" + encodeURIComponent(doc.subject) +
    "&body=" + encodeURIComponent(doc.body);
  document.getElementById("legal-modal").classList.add("active");
}}

function openKKVModal(ytunnus) {{
  showModal(DATA.kkv_filings[ytunnus], "KKV Toimenpidepyyntö Laittomasta Suorahankinnasta (Hankintalaki 139 §)");
}}
function openOikaisuModal(ytunnus) {{
  showModal(DATA.oikaisu_filings[ytunnus], "Hankintaoikaisuvaatimus & Virkavastuu-ilmoitus (Hankintalaki 133 §)");
}}
function openHilmaModal(tenderId) {{
  showModal(DATA.hilma_filings[tenderId], "Vaatimus Syrjivien Tarjousvaatimusten Poistamiseksi (Hankintalaki 67 §)");
}}
function openFoiaModal(ytunnus) {{
  showModal(DATA.foia_filings[ytunnus], "Pakottava Ostolaskujen & Osakassopimusten Tietopyyntö (Julkisuuslaki 13 § & 16 §)");
}}
function closeModal() {{
  document.getElementById("legal-modal").classList.remove("active");
}}
function copyModalText() {{
  navigator.clipboard.writeText(currentModalDoc.body);
}}
function downloadModalText() {{
  const blob = new Blob([currentModalDoc.body], {{ type: "text/plain;charset=utf-8" }});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "Kartelli_Purkaja_Asiakirja.txt";
  a.click();
}}

recalcDashboard();
renderArbitrageTable();
renderHilmaTable();
renderBuyersTable();
</script>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path
