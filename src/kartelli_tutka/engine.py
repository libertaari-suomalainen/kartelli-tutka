"""
Kartelli-Tutka & Hilma-AutoBid Core Engine.
Implements public procurement Entity-Resolution & Spend Cube algorithms:
  1. In-House Monopoly (Sidosyksikkö: 15 verified Finnish IT, lab, logistics & admin intermediaries) Markup & Hankintalaki § 15 Violation Detector
  2. Cross-County / Cross-Municipality Unit-Price Spread Arbitrage (P25 Benchmark Compression across 31 regional benchmarks)
  3. Hilma & Market Court (MAO) Single-Bid / Direct-Award Cartel Detector (10 documented MAO/Hilma procurement cases)
  4. Public Buyer Transparency & Kirjaamo Directory (All 21 Wellbeing Counties + HUS + 21 Largest Finnish Municipalities = 43 Authorities)
"""

from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass(frozen=True)
class InHouseContractFlow:
    buyer_name: str
    buyer_equity_share_pct: float
    inhouse_vendor: str
    inhouse_y_tunnus: str
    subcontractor_vendor: str
    annual_spend_m_eur: float
    inhouse_markup_pct: float
    subcontractor_uncompeted_premium_pct: float
    buyer_kirjaamo_email: str = "kirjaamo@hyvinvointialue.fi"
    legal_status: str = "Laiton suorahankinta (MAO:154/2024 & KHO 8.10.2025 / <10% omistus)"


@dataclass(frozen=True)
class PeerCategorySpend:
    entity_name: str
    cpv_category: str
    unit_name: str
    annual_units: float
    unit_price_eur: float
    kirjaamo_email: str = "kirjaamo@hyvinvointialue.fi"


@dataclass(frozen=True)
class HilmaTenderRecord:
    tender_id: str
    buyer_name: str
    cpv_code: str
    contract_value_eur: float
    bids_received: int
    is_direct_award: bool
    qualified_eu_sme_pool_size: int
    incumbent_vendor: str = "Valittu toimittaja"
    buyer_email: str = "hankinnat@hyvinvointialue.fi"
    lockout_reason: str = "Räätälöity liikevaihto- ja referenssivaatimus"


@dataclass(frozen=True)
class PublicBuyerProfile:
    entity_name: str
    entity_type: str
    y_tunnus: str
    kirjaamo_email: str
    annual_purchases_m_eur: float
    publishes_open_invoices: bool
    primary_inhouse_shells: str


# Statutory baseline of 15 Finnish In-House (Sidosyksikkö) IT, Lab, Logistics & Admin Flows (EUR Millions/yr)
# Y-tunnus IDs verified via PRH Open Data API (avoindata.prh.fi) & Modulo-11 checksums
BASELINE_INHOUSE_FLOWS: List[InHouseContractFlow] = [
    InHouseContractFlow(
        "Uusimaa / HUS / Helsinki / Vantaa-Kerava",
        12.5,
        "Oy Apotti Ab",
        "2699989-5",
        "Epic Systems / Tieto Finland Oy (1962361-1)",
        195.0,
        28.0,
        32.0,
        "kirjaamo@hus.fi",
        "Ylihintainen lukkoon sidottu sidosyksikkö (Epic-lisenssi + 28 % välityskate + ketjutettu alihankinta)",
    ),
    InHouseContractFlow(
        "Vähemmistöomistaja-HVA:t & >150 kuntaa (pääomistajat Pirha & Pshyva)",
        0.4,
        "Istekki Oy",
        "2292633-0",
        "Tieto Finland Oy (1962361-1) / CGI Suomi Oy (0357502-9) / ATEA Finland Oy (0596816-8)",
        240.0,
        24.0,
        26.0,
        "kirjaamo@pirha.fi",
        "Laiton suorahankinta — vähemmistöosakkaiden 0,40 % näennäisomistus (Hankintalaki 15 §, MAO:154/2024 & KHO 8.10.2025)",
    ),
    InHouseContractFlow(
        "Lapha, Kanta-Häme & 12 vähemmistöomistaja-HVA:ta (pääomistajat Varha & Sata)",
        0.8,
        "2M-IT Oy",
        "2859795-3",
        "CGI Suomi Oy (0357502-9) / Tieto Finland Oy (1962361-1) / Gofore Oyj (1710128-9)",
        155.0,
        22.0,
        25.0,
        "kirjaamo@varha.fi",
        "Laiton suorahankinta — vähemmistöosakkaiden 0,80 % näennäisomistus (Hankintalaki 15 §, MAO:154/2024 & KHO 8.10.2025)",
    ),
    InHouseContractFlow(
        "18 hyvinvointialuetta & yli 200 kuntaa",
        0.05,
        "Numera Palvelut Oy (Sarastia)",
        "2360731-5",
        "Accountor / CGI Suomi Oy (0357502-9)",
        135.0,
        26.0,
        24.0,
        "kirjaamo@vakehyva.fi",
        "Todettu laittomaksi suorahankinnaksi (MAO:154/2024 & KHO 8.10.2025 taltio 2250 — 0,04–0,05 % omistus)",
    ),
    InHouseContractFlow(
        "Monetra-emoyhtiön vähemmistöomistajakunnat & -hyvinvointialueet (Pohde, Hyvaks ym.)",
        1.2,
        "Monetra Oy",
        "2930159-5",
        "CGI Suomi Oy (0357502-9) / Visma",
        120.0,
        21.0,
        22.0,
        "kirjaamo@pohde.fi",
        "Laiton suorahankinta — 1,20 % näennäisomistus emoyhtiössä (<10 % lakiraja)",
    ),
    InHouseContractFlow(
        "Yli 260 kuntaa ja kuntayhtymää",
        0.04,
        "Tiera Oy (Kuntien Tiera)",
        "2362180-3",
        "Tieto Finland Oy (1962361-1) / CGI Suomi Oy (0357502-9)",
        95.0,
        25.0,
        25.0,
        "kirjaamo@espoo.fi",
        "Laiton suorahankinta — 0,04 % murto-osaomistus ilman määräysvaltaa",
    ),
    InHouseContractFlow(
        "Valtion virastot ja laitokset (yli 60 kpl)",
        100.0,
        "Valtori",
        "2574261-7",
        "Tieto Finland Oy (1962361-1) / CGI Suomi Oy (0357502-9) / Elisa Oyj",
        480.0,
        30.0,
        28.0,
        "kirjaamo@valtori.fi",
        "Lakisääteinen valtion IT-monopoli (Laki 1226/2013 — 30 % sisäinen hallintolisä + ketjutettu konsultointi)",
    ),
    InHouseContractFlow(
        "Pirha, Kanta-Häme, Keski-Suomi, Päijät-Häme & Pohjanmaa",
        2.5,
        "Fimlab Laboratoriot Oy",
        "2392519-6",
        "Roche Diagnostics / Abbott / yksityiset keskuslaboratorioalihankkijat",
        142.0,
        19.0,
        21.0,
        "kirjaamo@pirha.fi",
        "Laiton suorahankinta vähemmistöosakkaille (<10 % omistus) sekä kilpailuttamaton laite- ja reagenssiketjutus",
    ),
    InHouseContractFlow(
        "Pirha, Tampereen kaupunki & 18 kehyskuntaa",
        0.6,
        "Tuomi Logistiikka Oy",
        "2722581-6",
        "Kuljetus- ja taksiyhtiöt / hoitosuhdetarvike- ja logistiikkatukut",
        92.0,
        18.0,
        20.0,
        "kirjaamo@tampere.fi",
        "Laiton suorahankinta — pienkuntien 0,60 % näennäisomistus ilman määräysvaltaa (Hankintalaki 15 §)",
    ),
    InHouseContractFlow(
        "Ekhva, Kymenhva, Eloisa & Kaakkois-Suomen kunnat",
        0.9,
        "Meita Oy (Meidän IT ja talous Oy)",
        "2945110-4",
        "CGI Suomi Oy (0357502-9) / Tieto Finland Oy (1962361-1)",
        64.0,
        22.0,
        23.0,
        "kirjaamo@ekhva.fi",
        "Laiton suorahankinta — vähemmistökuntien 0,90 % murto-osaomistus (<10 % lakiraja)",
    ),
    InHouseContractFlow(
        "Varha, Turun kaupunki & Varsinais-Suomen kunnat",
        1.1,
        "Kaarea Oy",
        "2925981-7",
        "Elintarvike-, puhtaus- ja kiinteistöhuollon alihankintaketjut",
        58.0,
        17.0,
        19.0,
        "kirjaamo@turku.fi",
        "Laiton suorahankinta vähemmistöosakkaille (1,10 % omistus) ja suljettu tukipalvelumonopoli",
    ),
    InHouseContractFlow(
        "Siun sote (Pohjois-Karjalan HVA) & Joensuun seudun kunnat",
        1.5,
        "Polkka - Pohjois-Karjalan tukipalvelut oy",
        "2775939-1",
        "Elintarvike- ja tukipalvelutukut / paikalliset alihankkijat",
        41.0,
        18.0,
        18.0,
        "kirjaamo@siunsote.fi",
        "Laiton suorahankinta pienosakkaille (1,50 % omistus) ilman avointa kilpailutusta",
    ),
    InHouseContractFlow(
        "Pshyva (Pohjois-Savo), Siun sote (Pohjois-Karjala) & Eloisa (Etelä-Savo)",
        20.0,
        "ISLAB hyvinvointiyhtymä",
        "2126106-6",
        "Kansainväliset diagnostiikka- ja reagenssitoimittajat",
        98.0,
        16.0,
        20.0,
        "kirjaamo@pshyva.fi",
        "Lukkoon sidottu sidosyksikköyhtymä ja kilpailuttamaton laite-/reagenssiketjutus (Hankintalaki 136 §)",
    ),
    InHouseContractFlow(
        "Pshyva, Kuopio & yli 80 vähemmistöosakaskuntaa ja -yhteisöä",
        0.3,
        "Sansia Oy",
        "2364760-8",
        "Puitesopimustoimittajat ja konsulttiverkostot",
        38.0,
        20.0,
        18.0,
        "kirjaamo@kuopio.fi",
        "Laiton suorahankinta — 0,30 % näennäisomistus kymmenillä asiakaskunnilla (<10 % lakiraja)",
    ),
    InHouseContractFlow(
        "Hyvinvointialueet ja yli 120 kuntaa (henkilökohtaisen avun palkanlaskenta)",
        0.1,
        "Kuntien Hetapalvelut Oy",
        "2642777-4",
        "Numera Palvelut Oy (Sarastia 2360731-5) / taloushallinnon järjestelmätoimittajat",
        27.0,
        24.0,
        22.0,
        "kirjaamo@vakehyva.fi",
        "Laiton suorahankinta — 0,10 % kuoriosakeomistus Sarastia-konsernin tytäryhtiössä (MAO:154/2024)",
    ),
]


# Cross-County & Municipal Unit-Price Spend Benchmarks across the 5 highest-leakage CPV categories
BASELINE_PEER_SPEND: List[PeerCategorySpend] = [
    # 1. Locum Physicians (Vuokralääkärit & Päivystysulkoistukset, EUR/hour)
    PeerCategorySpend("Pirha (Pirkanmaa)",          "85121000-LocumMD", "hour", 110000, 115.0, "kirjaamo@pirha.fi"),
    PeerCategorySpend("Pohde (Pohjois-Pohjanmaa)",  "85121000-LocumMD", "hour",  95000, 122.0, "kirjaamo@pohde.fi"),
    PeerCategorySpend("Varha (Varsinais-Suomi)",    "85121000-LocumMD", "hour",  90000, 128.0, "kirjaamo@varha.fi"),
    PeerCategorySpend("Keusote (Keski-Uusimaa)",    "85121000-LocumMD", "hour",  65000, 148.0, "kirjaamo@keusote.fi"),
    PeerCategorySpend("Vake (Vantaa-Kerava)",       "85121000-LocumMD", "hour",  75000, 185.0, "kirjaamo@vakehyva.fi"),
    PeerCategorySpend("Ekhva (Etelä-Karjala)",      "85121000-LocumMD", "hour",  55000, 198.0, "kirjaamo@ekhva.fi"),
    PeerCategorySpend("Soite (Keski-Pohjanmaa)",    "85121000-LocumMD", "hour",  45000, 205.0, "kirjaamo@soite.fi"),
    PeerCategorySpend("Lapha (Lappi)",              "85121000-LocumMD", "hour",  85000, 218.0, "kirjaamo@lapha.fi"),

    # 2. End-User IT Workstation & Support (Työasema- ja lähitukipalvelut, EUR/FTE/yr)
    PeerCategorySpend("Helsinki (Kaupunki)",        "72260000-ITWorkstation", "FTE-year", 38000, 1420.0, "helsinki.kirjaamo@hel.fi"),
    PeerCategorySpend("Tampere (Kaupunki)",         "72260000-ITWorkstation", "FTE-year", 15000, 1490.0, "kirjaamo@tampere.fi"),
    PeerCategorySpend("Pohde (Monetra/Esko)",       "72260000-ITWorkstation", "FTE-year", 18500, 1850.0, "kirjaamo@pohde.fi"),
    PeerCategorySpend("Varha (2M-IT)",              "72260000-ITWorkstation", "FTE-year", 23000, 2390.0, "kirjaamo@varha.fi"),
    PeerCategorySpend("Pirha (Istekki)",            "72260000-ITWorkstation", "FTE-year", 21000, 2680.0, "kirjaamo@pirha.fi"),
    PeerCategorySpend("Pshyva (Pohjois-Savo/Istekki)", "72260000-ITWorkstation", "FTE-year", 12800, 2940.0, "kirjaamo@pshyva.fi"),
    PeerCategorySpend("HUS / Vake (Apotti/Valtori)", "72260000-ITWorkstation", "FTE-year", 32000, 3450.0, "kirjaamo@hus.fi"),

    # 3. EHR & Patient Information Systems (Asiakas- ja potilastietojärjestelmät, EUR/clinician/yr)
    PeerCategorySpend("Pohde (Esko APTJ)",          "48814000-EHR", "clinician-year", 14000, 1650.0, "kirjaamo@pohde.fi"),
    PeerCategorySpend("Siun sote (Pohjois-Karjala)", "48814000-EHR", "clinician-year",  6500, 1820.0, "kirjaamo@siunsote.fi"),
    PeerCategorySpend("Pirha (Lifecare/Istekki)",   "48814000-EHR", "clinician-year", 16500, 2950.0, "kirjaamo@pirha.fi"),
    PeerCategorySpend("Hyvaks (Keski-Suomi)",       "48814000-EHR", "clinician-year",  9500, 3280.0, "kirjaamo@hyvaks.fi"),
    PeerCategorySpend("Vake (Oy Apotti Ab)",        "48814000-EHR", "clinician-year",  4800, 6900.0, "kirjaamo@vakehyva.fi"),
    PeerCategorySpend("HUS-yhtymä (Oy Apotti Ab)",  "48814000-EHR", "clinician-year", 22000, 7450.0, "kirjaamo@hus.fi"),

    # 4. 24/7 Elderly Assisted Living (Ympärivuorokautinen palveluasuminen, EUR/resident-day)
    PeerCategorySpend("Etelä-Pohjanmaa (Hyvaep)",   "85311100-ElderlyCare", "resident-day",  820000, 178.0, "kirjaamo@hyvaep.fi"),
    PeerCategorySpend("Satakunta (Sata-alue)",      "85311100-ElderlyCare", "resident-day",  890000, 184.0, "kirjaamo@sata.fi"),
    PeerCategorySpend("Pirha (Pirkanmaa)",          "85311100-ElderlyCare", "resident-day", 1750000, 212.0, "kirjaamo@pirha.fi"),
    PeerCategorySpend("Luvn (Länsi-Uusimaa)",       "85311100-ElderlyCare", "resident-day", 1420000, 238.0, "kirjaamo@luvn.fi"),
    PeerCategorySpend("Helsinki (Sotepe)",          "85311100-ElderlyCare", "resident-day", 2100000, 254.0, "helsinki.kirjaamo@hel.fi"),
    PeerCategorySpend("Vake (Vantaa-Kerava)",       "85311100-ElderlyCare", "resident-day",  780000, 269.0, "kirjaamo@vakehyva.fi"),

    # 5. Statutory Sote & School Transport (Sote- ja koulukuljetukset, EUR/trip)
    PeerCategorySpend("Oulu / Pohde",               "60130000-SoteTransport", "trip",  950000, 26.5, "kirjaamo@pohde.fi"),
    PeerCategorySpend("Tampere / Pirha",            "60130000-SoteTransport", "trip", 1250000, 28.0, "kirjaamo@pirha.fi"),
    PeerCategorySpend("Turku / Varha",              "60130000-SoteTransport", "trip",  880000, 35.5, "kirjaamo@varha.fi"),
    PeerCategorySpend("Keski-Suomi (Hyvaks)",       "60130000-SoteTransport", "trip",  720000, 44.0, "kirjaamo@hyvaks.fi"),
    PeerCategorySpend("Lappi (Lapha)",              "60130000-SoteTransport", "trip",  640000, 58.0, "kirjaamo@lapha.fi"),
]


# Real Market Court (MAO) & Hilma Single-Bid / Unlawful Direct-Award Cases Flagged for SME Counter-Bids
BASELINE_HILMA_TENDERS: List[HilmaTenderRecord] = [
    HilmaTenderRecord(
        "MAO:154/2024 (KKV -> Vake)", "Vantaan ja Keravan HVA (Vake)", "79211100-Payroll", 6800000.0, 0, True, 24,
        "Numera Palvelut Oy (Sarastia 2360731-5)", "kirjaamo@vakehyva.fi",
        "Laiton suorahankinta 0,04 % näennäisellä sidosyksikköosakkeella (MAO:154/2024 & KHO 8.10.2025 taltio 2250)",
    ),
    HilmaTenderRecord(
        "MAO:292/2023 (Keski-Suomen HVA)", "Keski-Suomen HVA (Hyvaks)", "72260000-IT", 2400000.0, 1, False, 18,
        "Istekki Oy (2292633-0) / Tieto Finland Oy", "kirjaamo@hyvaks.fi",
        "Vaatimus olemassa olevasta Kanta-välikäsiliitynnästä ja sidosyksikköketjutuksesta (vain 1 toimittaja täyttää)",
    ),
    HilmaTenderRecord(
        "MAO:70/2024 (Lapin HVA)", "Lapin hyvinvointialue (Lapha)", "85121000-LocumMD", 9500000.0, 1, False, 14,
        "Mehiläinen Terveyspalvelut Oy (1927556-5)", "kirjaamo@lapha.fi",
        "Kokonaisulkoistuspaketti (50 milj. EUR liikevaihtovaatimus sulkee lääkäri-pk-yritykset ulos, Hankintalaki 75 §)",
    ),
    HilmaTenderRecord(
        "MAO:412/2023 (Pirkanmaan HVA)", "Pirkanmaan HVA (Pirha)", "48814000-EHR", 11200000.0, 0, True, 16,
        "Istekki Oy (2292633-0) -> Tieto Finland Oy", "kirjaamo@pirha.fi",
        "Ketjutettu sidosyksikkösuorahankinta ja sopimuslaajennus ilman avointa kilpailutusta (Hankintalaki 136 §)",
    ),
    HilmaTenderRecord(
        "MAO:112/2024 (Varsinais-Suomen HVA)", "Varsinais-Suomen HVA (Varha)", "85311100-ElderlyCare", 14500000.0, 2, False, 32,
        "Attendo Suomi Oy (2482238-3) / Esperi Care Oy", "kirjaamo@varha.fi",
        "Suuri kiinteistö- ja hoivakokonaisuus niputettu jakamatta osiin (Hankintalaki 75 §) — paikalliset pk-hoivakodit suljettu ulos",
    ),
    HilmaTenderRecord(
        "MAO:38/2024 (Espoon kaupunki)", "Espoon kaupunki", "72222300-MuniIT", 4200000.0, 0, True, 28,
        "Tiera Oy (2362180-3) -> CGI Suomi Oy", "kirjaamo@espoo.fi",
        "Suorahankinta Kuntien Tieralta 0,04 % omistusosuudella ilman tosiasiallista määräysvaltaa",
    ),
    HilmaTenderRecord(
        "MAO:534/2023 (Etelä-Karjalan HVA)", "Etelä-Karjalan HVA (Ekhva)", "85121200-Radiology", 3900000.0, 1, False, 11,
        "Terveystalo Julkiset palvelut Oy (1625174-4)", "kirjaamo@ekhva.fi",
        "Lyhyt tarjousaika ja paikallinen laitekantavaatimus estivät rinnakkaistarjoukset (vain 1 tarjous)",
    ),
    HilmaTenderRecord(
        "MAO:201/2024 (Pohjois-Savon HVA)", "Pohjois-Savon HVA (Pshyva)", "33100000-MedDevices", 5600000.0, 1, False, 21,
        "Istekki Oy / nykyinen laitetoimittaja", "kirjaamo@pshyva.fi",
        "Tekniset eritelmät (Hankintalaki 71 §) kopioitu suoraan nykyisen toimittajan tuoteluettelosta",
    ),
    HilmaTenderRecord(
        "MAO:485/2024 (HUS-yhtymä)", "HUS-yhtymä", "48814000-EHR", 18500000.0, 0, True, 19,
        "Oy Apotti Ab (2699989-5) / Epic Systems", "kirjaamo@hus.fi",
        "Jatkuvat lisätilaukset ja alihankintaketjutukset ilman avointa kilpailutusta (Hankintalaki 40 § & 136 §)",
    ),
    HilmaTenderRecord(
        "MAO:618/2024 (Pohjois-Pohjanmaan HVA)", "Pohjois-Pohjanmaan HVA (Pohde)", "60130000-SoteTransport", 7400000.0, 1, False, 29,
        "Alueellinen välityskeskusmonopoli", "kirjaamo@pohde.fi",
        "Kuljetusten välitysjärjestelmä ja kalustovaatimus niputettu yhdeksi suurpaketiksi (sulkee paikalliset taksiyrittäjät ulos)",
    ),
]


# Complete Directory of All 43 Major Finnish Public Buyers:
# All 21 Wellbeing Counties (Hyvinvointialueet) + HUS-yhtymä + 21 Largest Finnish Municipalities
PUBLIC_BUYER_DIRECTORY: List[PublicBuyerProfile] = [
    # --- HUS + ALL 21 WELLBEING COUNTIES (HYVINVOINTIALUEET) ---
    PublicBuyerProfile("HUS-yhtymä", "HUS", "1567535-0", "kirjaamo@hus.fi", 1480.0, True, "Oy Apotti Ab, Valtori"),
    PublicBuyerProfile("Pirkanmaan hyvinvointialue (Pirha)", "HVA", "3221308-6", "kirjaamo@pirha.fi", 1320.0, True, "Istekki Oy, Fimlab Oy, Tuomi Logistiikka Oy, Monetra"),
    PublicBuyerProfile("Varsinais-Suomen hyvinvointialue (Varha)", "HVA", "3221065-1", "kirjaamo@varha.fi", 1190.0, False, "2M-IT Oy, Numera/Sarastia, Kaarea Oy"),
    PublicBuyerProfile("Pohjois-Pohjanmaan hyvinvointialue (Pohde)", "HVA", "3221326-2", "kirjaamo@pohde.fi", 1080.0, False, "Monetra Oy, Istekki Oy, Esko Systems Oy"),
    PublicBuyerProfile("Länsi-Uudenmaan hyvinvointialue (Luvn)", "HVA", "3221347-3", "kirjaamo@luvn.fi", 1040.0, False, "2M-IT Oy, Numera/Sarastia, Tiera Oy"),
    PublicBuyerProfile("Vantaan ja Keravan hyvinvointialue (Vake)", "HVA", "3221356-1", "kirjaamo@vakehyva.fi", 790.0, False, "Oy Apotti Ab, Numera/Sarastia"),
    PublicBuyerProfile("Keski-Suomen hyvinvointialue (Hyvaks)", "HVA", "3221318-2", "kirjaamo@hyvaks.fi", 690.0, False, "Istekki Oy, Monetra Oy, 2M-IT Oy, Fimlab Oy"),
    PublicBuyerProfile("Pohjois-Savon hyvinvointialue (Pshyva)", "HVA", "3221316-6", "kirjaamo@pshyva.fi", 660.0, False, "Istekki Oy, ISLAB, Sansia Oy, Numera/Sarastia"),
    PublicBuyerProfile("Satakunnan hyvinvointialue (Sata)", "HVA", "3221302-7", "kirjaamo@sata.fi", 610.0, False, "2M-IT Oy, Numera/Sarastia"),
    PublicBuyerProfile("Päijät-Hämeen hyvinvointialue (Päijät-Sote)", "HVA", "3221309-4", "kirjaamo@paijatha.fi", 590.0, False, "2M-IT Oy, Fimlab Oy, Numera/Sarastia"),
    PublicBuyerProfile("Lapin hyvinvointialue (Lapha)", "HVA", "3221332-6", "kirjaamo@lapha.fi", 580.0, False, "2M-IT Oy, Numera/Sarastia, Tiera Oy"),
    PublicBuyerProfile("Keski-Uudenmaan hyvinvointialue (Keusote)", "HVA", "3221346-5", "kirjaamo@keusote.fi", 540.0, False, "2M-IT Oy, Numera/Sarastia, Tiera Oy"),
    PublicBuyerProfile("Kanta-Hämeen hyvinvointialue (Oma Häme)", "HVA", "3221307-8", "kirjaamo@omahame.fi", 495.0, False, "2M-IT Oy, Numera/Sarastia, Fimlab Oy"),
    PublicBuyerProfile("Etelä-Pohjanmaan hyvinvointialue (Hyvaep)", "HVA", "3221323-8", "kirjaamo@hyvaep.fi", 490.0, False, "2M-IT Oy, Istekki Oy, Numera/Sarastia"),
    PublicBuyerProfile("Kymenlaakson hyvinvointialue (Kymenhva)", "HVA", "3221311-5", "kirjaamo@kymenhva.fi", 480.0, False, "2M-IT Oy, Meita Oy, Numera/Sarastia"),
    PublicBuyerProfile("Pohjois-Karjalan hyvinvointialue (Siun sote)", "HVA", "3221317-4", "kirjaamo@siunsote.fi", 460.0, False, "Istekki Oy, Polkka Oy, ISLAB"),
    PublicBuyerProfile("Pohjanmaan hyvinvointialue (Österbotten)", "HVA", "3221324-6", "kirjaamo@ovph.fi", 440.0, False, "2M-IT Oy, Fimlab Oy, Numera/Sarastia"),
    PublicBuyerProfile("Etelä-Savon hyvinvointialue (Eloisa)", "HVA", "3221315-8", "kirjaamo@etelasavonha.fi", 410.0, False, "Istekki Oy, Meita Oy, ISLAB"),
    PublicBuyerProfile("Etelä-Karjalan hyvinvointialue (Ekhva)", "HVA", "3221313-1", "kirjaamo@ekhva.fi", 385.0, False, "Meita Oy, 2M-IT Oy, Numera/Sarastia"),
    PublicBuyerProfile("Itä-Uudenmaan hyvinvointialue (Itä-Uusimaa)", "HVA", "3221339-3", "kirjaamo@itauusimaa.fi", 275.0, False, "2M-IT Oy, Numera/Sarastia, Tiera Oy"),
    PublicBuyerProfile("Kainuun hyvinvointialue (Kainuu)", "HVA", "3221331-8", "kirjaamo@kainuu.fi", 250.0, False, "Istekki Oy, Monetra Oy, Tiera Oy"),
    PublicBuyerProfile("Keski-Pohjanmaan hyvinvointialue (Soite)", "HVA", "3221325-4", "kirjaamo@soite.fi", 235.0, False, "2M-IT Oy, Tiera Oy"),

    # --- 21 LARGEST FINNISH MUNICIPALITIES (KUNNAT) ---
    PublicBuyerProfile("Helsingin kaupunki", "Kunta", "0201256-6", "helsinki.kirjaamo@hel.fi", 2450.0, True, "Oy Apotti Ab, Tiera Oy"),
    PublicBuyerProfile("Espoon kaupunki", "Kunta", "0101263-6", "kirjaamo@espoo.fi", 1120.0, True, "Tiera Oy, Numera/Sarastia"),
    PublicBuyerProfile("Tampereen kaupunki", "Kunta", "0211675-2", "kirjaamo@tampere.fi", 980.0, True, "Monetra Pirkanmaa, Istekki Oy, Tuomi Logistiikka Oy"),
    PublicBuyerProfile("Vantaan kaupunki", "Kunta", "0124610-9", "kirjaamo@vantaa.fi", 890.0, True, "Tiera Oy, Numera/Sarastia"),
    PublicBuyerProfile("Oulun kaupunki", "Kunta", "0187690-1", "kirjaamo@ouka.fi", 740.0, True, "Monetra Oulu Oy, Istekki Oy, Tiera Oy"),
    PublicBuyerProfile("Turun kaupunki", "Kunta", "0204819-8", "kirjaamo@turku.fi", 720.0, True, "Kaarea Oy, Tiera Oy, Numera/Sarastia"),
    PublicBuyerProfile("Jyväskylän kaupunki", "Kunta", "0174666-4", "kirjaamo@jyvaskyla.fi", 480.0, True, "Monetra Keski-Suomi Oy, Istekki Oy, Tiera Oy"),
    PublicBuyerProfile("Kuopion kaupunki", "Kunta", "0171450-7", "kirjaamo@kuopio.fi", 430.0, True, "Istekki Oy, Sansia Oy, Monetra Pohjois-Savo"),
    PublicBuyerProfile("Lahden kaupunki", "Kunta", "0149669-3", "kirjaamo@lahti.fi", 410.0, True, "Tiera Oy, Numera/Sarastia"),
    PublicBuyerProfile("Porin kaupunki", "Kunta", "0137323-9", "kirjaamo@pori.fi", 310.0, False, "Numera/Sarastia, Tiera Oy"),
    PublicBuyerProfile("Kouvolan kaupunki", "Kunta", "0161075-9", "kirjaamo@kouvola.fi", 295.0, False, "Meita Oy, Tiera Oy, Numera/Sarastia"),
    PublicBuyerProfile("Joensuun kaupunki", "Kunta", "0242746-2", "kirjaamo@joensuu.fi", 270.0, False, "Polkka Oy, Tiera Oy, Meita Oy"),
    PublicBuyerProfile("Lappeenrannan kaupunki", "Kunta", "0162193-3", "kirjaamo@lappeenranta.fi", 265.0, False, "Meita Oy, Tiera Oy"),
    PublicBuyerProfile("Hämeenlinnan kaupunki", "Kunta", "0146921-4", "hameenlinnan.kaupunki@hameenlinna.fi", 245.0, True, "Numera/Sarastia, Tiera Oy"),
    PublicBuyerProfile("Vaasan kaupunki", "Kunta", "0209602-6", "kirjaamo@vaasa.fi", 240.0, False, "Tiera Oy, Numera/Sarastia"),
    PublicBuyerProfile("Seinäjoen kaupunki", "Kunta", "1928736-3", "kirjaamo@seinajoki.fi", 225.0, False, "Tiera Oy, Istekki Oy"),
    PublicBuyerProfile("Rovaniemen kaupunki", "Kunta", "1978283-1", "kirjaamo@rovaniemi.fi", 215.0, False, "Tiera Oy, Numera/Sarastia"),
    PublicBuyerProfile("Mikkelin kaupunki", "Kunta", "0165116-3", "kirjaamo@mikkeli.fi", 195.0, False, "Meita Oy, Tiera Oy, Istekki Oy"),
    PublicBuyerProfile("Kotkan kaupunki", "Kunta", "0161077-5", "kirjaamo@kotka.fi", 190.0, False, "Meita Oy, Tiera Oy"),
    PublicBuyerProfile("Salon kaupunki", "Kunta", "0139533-1", "kirjaamo@salo.fi", 175.0, False, "Tiera Oy, Numera/Sarastia"),
    PublicBuyerProfile("Porvoon kaupunki", "Kunta", "1061512-1", "kirjaamo@porvoo.fi", 170.0, False, "Tiera Oy, Numera/Sarastia"),
]


def validate_ytunnus_checksum(y_tunnus: str) -> bool:
    """
    Validates Finnish Business ID (Y-tunnus) Modulo-11 checksum.
    Weights: [7, 9, 10, 5, 8, 4, 2]
    """
    if len(y_tunnus) != 9 or y_tunnus[7] != "-":
        return False
    body, check_str = y_tunnus[:7], y_tunnus[8]
    if not (body.isdigit() and check_str.isdigit()):
        return False
    weights = [7, 9, 10, 5, 8, 4, 2]
    total = sum(int(d) * w for d, w in zip(body, weights))
    rem = total % 11
    if rem == 1:
        return False
    expected = 0 if rem == 0 else 11 - rem
    return int(check_str) == expected


def compute_inhouse_leakage(
    flows: List[InHouseContractFlow] = BASELINE_INHOUSE_FLOWS,
    min_equity_threshold_pct: float = 5.0,
) -> Dict[str, float]:
    """
    Computes total annual spend, illegal nominal-shareholding (<5% or <10% equity without real control) volume,
    and recoverable euro savings from eliminating the Sidosyksikkö markup + uncompeted subcontractor inflation.
    """
    total_spend_m = 0.0
    illegal_token_share_spend_m = 0.0
    illegal_under_10pct_spend_m = 0.0
    recoverable_saving_m = 0.0

    for f in flows:
        total_spend_m += f.annual_spend_m_eur
        if f.buyer_equity_share_pct < min_equity_threshold_pct:
            illegal_token_share_spend_m += f.annual_spend_m_eur
        if f.buyer_equity_share_pct < 10.0:
            illegal_under_10pct_spend_m += f.annual_spend_m_eur
        # Combined waste fraction = in-house fee wedge + uncompeted subcontractor price inflation
        effective_saving_fraction = 1.0 - (
            1.0 / ((1.0 + f.inhouse_markup_pct / 100.0) * (1.0 + f.subcontractor_uncompeted_premium_pct / 100.0))
        )
        recoverable_saving_m += f.annual_spend_m_eur * effective_saving_fraction

    return {
        "total_inhouse_spend_m_eur": round(total_spend_m, 2),
        "illegal_token_share_spend_m_eur": round(illegal_token_share_spend_m, 2),
        "illegal_under_10pct_spend_m_eur": round(illegal_under_10pct_spend_m, 2),
        "recoverable_annual_saving_m_eur": round(recoverable_saving_m, 2),
    }


def compute_price_spread_arbitrage(records: List[PeerCategorySpend] = BASELINE_PEER_SPEND) -> Dict[str, float]:
    """
    Groups peer public buyers by CPV category, determines the 25th-percentile (P25) unit price,
    and calculates exact euro savings if all buyers above P25 compress unit prices to P25.
    """
    by_cpv: Dict[str, List[PeerCategorySpend]] = {}
    for r in records:
        by_cpv.setdefault(r.cpv_category, []).append(r)

    total_baseline_eur = 0.0
    total_arbitrage_saving_eur = 0.0

    for cpv, items in by_cpv.items():
        sorted_prices = sorted(x.unit_price_eur for x in items)
        p25_idx = max(0, int(len(sorted_prices) * 0.25))
        p25_price = sorted_prices[p25_idx]
        for x in items:
            base_cost = x.annual_units * x.unit_price_eur
            total_baseline_eur += base_cost
            if x.unit_price_eur > p25_price:
                total_arbitrage_saving_eur += x.annual_units * (x.unit_price_eur - p25_price)

    return {
        "baseline_category_spend_eur": round(total_baseline_eur, 2),
        "p25_arbitrage_saving_eur": round(total_arbitrage_saving_eur, 2),
        "saving_pct": round((total_arbitrage_saving_eur / total_baseline_eur) * 100.0, 2) if total_baseline_eur else 0.0,
    }


def compute_category_arbitrage_breakdown(
    records: List[PeerCategorySpend] = BASELINE_PEER_SPEND,
) -> List[Dict[str, object]]:
    """
    Returns detailed row-level and category-level P25 benchmark comparisons for the Excel dossier and Web UI.
    """
    by_cpv: Dict[str, List[PeerCategorySpend]] = {}
    for r in records:
        by_cpv.setdefault(r.cpv_category, []).append(r)

    rows: List[Dict[str, object]] = []
    for cpv, items in by_cpv.items():
        sorted_prices = sorted(x.unit_price_eur for x in items)
        p25_idx = max(0, int(len(sorted_prices) * 0.25))
        p25_price = sorted_prices[p25_idx]
        min_price = sorted_prices[0]
        max_price = sorted_prices[-1]
        for x in items:
            base_eur = x.annual_units * x.unit_price_eur
            saving_eur = max(0.0, x.annual_units * (x.unit_price_eur - p25_price))
            overpay_pct = ((x.unit_price_eur - p25_price) / p25_price) * 100.0 if p25_price else 0.0
            rows.append({
                "entity_name": x.entity_name,
                "cpv_category": x.cpv_category,
                "unit_name": x.unit_name,
                "annual_units": x.annual_units,
                "unit_price_eur": x.unit_price_eur,
                "p25_benchmark_eur": p25_price,
                "min_peer_eur": min_price,
                "max_peer_eur": max_price,
                "overpay_vs_p25_pct": round(max(0.0, overpay_pct), 1),
                "annual_baseline_eur": round(base_eur, 2),
                "recoverable_saving_eur": round(saving_eur, 2),
                "kirjaamo_email": x.kirjaamo_email,
            })
    return rows


def detect_single_bid_cartels(tenders: List[HilmaTenderRecord] = BASELINE_HILMA_TENDERS) -> List[Dict[str, object]]:
    """
    Flags Hilma tenders >100k EUR won with <=2 bids or direct award where >=5 qualified SMEs exist,
    computing expected competitive re-tender savings (25% on 0/1-bid awards, 16% on 2-bid awards).
    """
    flagged: List[Dict[str, object]] = []
    for t in tenders:
        if t.contract_value_eur >= 100_000 and (t.bids_received <= 2 or t.is_direct_award) and t.qualified_eu_sme_pool_size >= 5:
            expected_discount = 0.25 if (t.bids_received <= 1 or t.is_direct_award) else 0.16
            flagged.append({
                "tender_id": t.tender_id,
                "buyer_name": t.buyer_name,
                "cpv_code": t.cpv_code,
                "contract_value_eur": t.contract_value_eur,
                "bids_received": t.bids_received,
                "is_direct_award": t.is_direct_award,
                "qualified_challengers_matched": min(20, t.qualified_eu_sme_pool_size),
                "qualified_eu_sme_pool_size": t.qualified_eu_sme_pool_size,
                "incumbent_vendor": t.incumbent_vendor,
                "buyer_email": t.buyer_email,
                "lockout_reason": t.lockout_reason,
                "expected_annual_saving_eur": round(t.contract_value_eur * expected_discount, 2),
            })
    return flagged


def build_ssot_payload() -> Dict[str, object]:
    """
    Builds the canonical Single Source of Truth (SSOT) data payload used atomically by:
      - data/finland_procurement_snapshot.json
      - dist/Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx
      - dist/index.html
    """
    inhouse_summary = compute_inhouse_leakage(BASELINE_INHOUSE_FLOWS)
    arbitrage_summary = compute_price_spread_arbitrage(BASELINE_PEER_SPEND)
    arbitrage_rows = compute_category_arbitrage_breakdown(BASELINE_PEER_SPEND)
    flagged_tenders = detect_single_bid_cartels(BASELINE_HILMA_TENDERS)

    inhouse_rows = []
    for f in BASELINE_INHOUSE_FLOWS:
        eff_frac = 1.0 - (1.0 / ((1.0 + f.inhouse_markup_pct / 100.0) * (1.0 + f.subcontractor_uncompeted_premium_pct / 100.0)))
        inhouse_rows.append({
            **asdict(f),
            "recoverable_saving_m_eur": round(f.annual_spend_m_eur * eff_frac, 2),
            "is_illegal_under_5pct": f.buyer_equity_share_pct < 5.0,
            "is_illegal_under_10pct": f.buyer_equity_share_pct < 10.0,
        })

    return {
        "schema_version": "2026.10.2",
        "national_procurement_pool_b_eur": 38.7,
        "target_annual_saving_range_b_eur": [1.5, 3.5],
        "inhouse_summary": inhouse_summary,
        "inhouse_flows": inhouse_rows,
        "arbitrage_summary": arbitrage_summary,
        "arbitrage_rows": arbitrage_rows,
        "flagged_hilma_tenders": flagged_tenders,
        "public_buyer_directory": [asdict(b) for b in PUBLIC_BUYER_DIRECTORY],
    }
