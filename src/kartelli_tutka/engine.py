"""
Kartelli-Tutka — Julkisten Hankintojen Rakenteellinen Tehokkuus- ja Sidosyksikköanalyysi.
Toteuttaa julkisten hankintojen avoimeen viranomaisdataan perustuvat laskentamallit:
  1. Sidosyksikköanalyysi (15 suomalaisen ICT-, laboratorio-, logistiikka- ja tukipalveluyksikön tilinpäätösperusteinen liikevaihto 2024–2025 sekä Hankintalain 15 §:n omistusosuustarkastelu)
  2. Hyvinvointialueiden ja kuntien yksikkökustannusten alueellinen vertailu (P25-vertailutaso 5 keskeisessä CPV-kategoriassa THL:n, HALI ry:n ja KKV:n julkaisemien yksikkökustannusvertailujen pohjalta)
  3. Markkinaoikeuden (MAO) ja korkeimman hallinto-oikeuden (KHO) todelliset julkisten hankintojen oikeustapaukset (10 vahvistettua Finlex/KKV-ratkaisua 2023–2025)
  4. Julkisten hankintayksiköiden avoimuus- ja kirjaamorekisteri (Kaikki 21 hyvinvointialuetta + HUS + 21 suurinta kaupunkia = 43 viranomaista)
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
    legal_status: str = "Hajautettu pienomistus (<10 %, Hankintalaki 15 § / HE 2/2026 vp)"


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
    incumbent_vendor: str = "Sopimustoimittaja"
    buyer_email: str = "hankinnat@hyvinvointialue.fi"
    lockout_reason: str = "Markkinaoikeuden (MAO) tai KHO:n ratkaisussa arvioitu hankintamenettely"


@dataclass(frozen=True)
class PublicBuyerProfile:
    entity_name: str
    entity_type: str
    y_tunnus: str
    kirjaamo_email: str
    annual_purchases_m_eur: float
    publishes_open_invoices: bool
    primary_inhouse_shells: str


# Virallisiin tilinpäätöksiin (2024–2025) ja PRH:n avoimeen dataan perustuva 15 sidosyksikön ja valtion IT-palvelukeskuksen vertailu (M€/v).
# Huom: Yksityiset alihankkijat ja puitesopimustoimittajat toimivat laillisina kaupallisina toimittajina; tarkastelu kohdistuu
# julkisten hankintayksiköiden sidosyksikköomistuksen rakenteeseen (Hankintalaki 15 §) ja avoimen kilpailutuksen tehokkuuspotentiaaliin.
BASELINE_INHOUSE_FLOWS: List[InHouseContractFlow] = [
    InHouseContractFlow(
        "HUS-yhtymä (44,7 %), Helsingin kaupunki (36,6 %) & Vantaan ja Keravan HVA",
        18.7,
        "Oy Apotti Ab",
        "2699989-5",
        "Epic Systems Corporation / järjestelmä- ja käyttöpalvelutoimittajat (lailliset sopimustoimittajat)",
        147.7,
        6.0,
        8.0,
        "kirjaamo@hus.fi",
        "Tilinpäätös 2025: liikevaihto 147,7 M€ (2024: 159,0 M€). Enemmistöomisteinen sidosyksikkö (>10 %); tarkastelussa pitkäaikainen järjestelmäsidonnaisuus ja yksikkökustannus.",
    ),
    InHouseContractFlow(
        "Pirha, Pshyva (pääomistajat) sekä kymmenet pienomistajakunnat ja -HVA:t (<10 %)",
        0.4,
        "Istekki Oy",
        "2292633-0",
        "Kaupalliset ICT-laite-, lisenssi- ja asiantuntijapuitesopimustoimittajat (Tietoevry, CGI, Atea ym.)",
        264.6,
        6.5,
        7.5,
        "kirjaamo@pirha.fi",
        "Tilinpäätös 2025: liikevaihto 264,6 M€ (2024: 260,5 M€). Pääomistajilla vahva osuus, mutta lukuisilla pienosakkailla alle 10 % omistusosuus (Hankintalaki 15 § / HE 2/2026 vp).",
    ),
    InHouseContractFlow(
        "15 hyvinvointialuetta ja sairaanhoitopiiritaustaista omistajaa (hajautettu omistus)",
        2.5,
        "2M-IT Oy",
        "2859795-3",
        "Kaupalliset sote-ICT- ja ohjelmistotoimittajat (CGI, Tietoevry, Gofore ym.)",
        199.6,
        6.0,
        7.5,
        "kirjaamo@varha.fi",
        "Tilinpäätös 2025: liikevaihto 199,6 M€ (2024: 189,0 M€). Useiden hyvinvointialueiden yhteinen sote-IT-sidosyksikkö, jossa yksittäisten pienomistajien osuus alittaa 10 % rajan.",
    ),
    InHouseContractFlow(
        "Hyvinvointialueet ja yli 200 kuntaa (esim. Vake 0,04 % MAO:154/2024)",
        0.04,
        "Numera Palvelut Oy (ent. Sarastia Oy)",
        "2360731-5",
        "Talous- ja palkkahallinnon järjestelmä- ja palvelutoimittajat",
        115.6,
        7.0,
        8.0,
        "kirjaamo@vakehyva.fi",
        "Tilinpäätös 2024: konsernin liikevaihto 115,6 M€ (emoyhtiö 76,3 M€). KHO 8.10.2025 (T2250) ja MAO:154/2024 vahvistivat, ettei 0,04 % pienomistus täyttänyt hankintalain 15 §:n määräysvaltaedellytystä.",
    ),
    InHouseContractFlow(
        "Oulu, Tampere, Jyväskylä, Kuopio, HVA:t sekä pienomistajakunnat",
        1.2,
        "Monetra Oy (Monetra-konserni)",
        "2930159-5",
        "Talous- ja HR-ohjelmistojen kaupalliset puitesopimustoimittajat (CGI, Visma ym.)",
        114.7,
        6.0,
        7.0,
        "kirjaamo@pohde.fi",
        "Tilinpäätös 2025: konsernin liikevaihto 114,7 M€. Alueellisilla pääomistajilla merkittävä osuus tytäryhtiöissä, mutta pienosakaskunnilla alle 10 % omistusosuus.",
    ),
    InHouseContractFlow(
        "Yli 300 kuntaa, kuntayhtymää ja hyvinvointialuetta",
        0.04,
        "Tiera Oy (Kuntien Tiera)",
        "2362180-3",
        "Kaupalliset ICT-ohjelmisto- ja laitepuitesopimustoimittajat",
        76.0,
        7.0,
        8.0,
        "kirjaamo@espoo.fi",
        "Tilinpäätös 2025: liikevaihto 76,0 M€. Laajasti hajautettu yli 300 julkisyhteisön omistus (yksittäinen pienosakas tyypillisesti 0,01–2,5 %); KKV:n sidosyksikkövalvonnan kohteena.",
    ),
    InHouseContractFlow(
        "Valtion virastot ja laitokset (lakisääteinen käyttövelvoite, Laki 1226/2013)",
        100.0,
        "Valtori (Valtion TVT-keskus)",
        "2574261-7",
        "Kaupalliset ICT- ja tietoliikennetoimittajat (kilpailutetut puitesopimukset)",
        465.0,
        5.5,
        6.5,
        "kirjaamo@valtori.fi",
        "Valtion talousarvio / tilinpäätös 2024–2025: n. 465,0 M€. Valtion virasto (Laki 1226/2013, ei osakeyhtiömuotoinen sidosyksikkö); tehokkuustarkastelu koskee sisäistä palveluhinnoittelua ja puitesopimusketjuja.",
    ),
    InHouseContractFlow(
        "Pirha (pääomistaja), Kanta-Häme, Keski-Suomi, Päijät-Häme & Pohjanmaa",
        2.5,
        "Fimlab Laboratoriot Oy",
        "2392519-6",
        "Kansainväliset diagnostiikka-, analysaattori- ja reagenssitoimittajat",
        173.5,
        5.5,
        6.5,
        "kirjaamo@pirha.fi",
        "Tilinpäätös 2025: liikevaihto 173,5 M€. Viiden hyvinvointialueen yhteinen laboratorioyhtiö (Pirha suurin omistaja; pienemmillä osakkailla alle 10 % omistusosuus).",
    ),
    InHouseContractFlow(
        "Pirha, Tampereen kaupunki (pääomistajat) & Pirkanmaan kehyskunnat",
        0.6,
        "Tuomi Logistiikka Oy",
        "2722581-6",
        "Kuljetuspalvelu- ja hoitotarvikesopimustoimittajat",
        112.0,
        5.5,
        6.5,
        "kirjaamo@tampere.fi",
        "Tilinpäätös 2024–2025: liikevaihto n. 112,0 M€. Pirkanmaan yhteinen logistiikka- ja hankintayhtiö; pääomistajina Pirha ja Tampere, kehyskunnilla alle 10 % pienomistus.",
    ),
    InHouseContractFlow(
        "Ekhva, Kymenhva, Eloisa & Kaakkois-Suomen kunnat",
        0.9,
        "Meita Oy (Meidän IT ja talous Oy)",
        "2945110-4",
        "Talous- ja ICT-järjestelmien kaupalliset sopimustoimittajat",
        58.5,
        6.0,
        7.0,
        "kirjaamo@ekhva.fi",
        "Tilinpäätös 2024–2025: liikevaihto n. 58,5 M€. Kaakkois- ja Itä-Suomen kuntien sekä hyvinvointialueiden ICT- ja taloussidosyksikkö; pienosakkailla alle 10 % osuus.",
    ),
    InHouseContractFlow(
        "Varha, Turun kaupunki (pääomistajat) & Varsinais-Suomen kunnat",
        1.1,
        "Kaarea Oy",
        "2925981-7",
        "Elintarvike-, puhtaus- ja kiinteistöpalveluiden sopimustoimittajat",
        68.2,
        5.5,
        6.5,
        "kirjaamo@turku.fi",
        "Tilinpäätös 2024–2025: liikevaihto n. 68,2 M€. Varsinais-Suomen ruoka- ja tukipalveluiden sidosyksikkö; pienosakaskunnilla alle 10 % omistusosuus.",
    ),
    InHouseContractFlow(
        "Siun sote (Pohjois-Karjalan HVA), Joensuu & alueen kunnat",
        1.5,
        "Polkka - Pohjois-Karjalan tukipalvelut oy",
        "2775939-1",
        "Elintarvike- ja tukipalvelutoimittajat",
        39.4,
        5.5,
        6.5,
        "kirjaamo@siunsote.fi",
        "Tilinpäätös 2024–2025: liikevaihto n. 39,4 M€. Pohjois-Karjalan ruoka- ja puhtauspalveluiden sidosyksikkö; pienkunnilla alle 10 % omistusosuus.",
    ),
    InHouseContractFlow(
        "Pohjois-Savon HVA, Pohjois-Karjalan HVA & Etelä-Savon HVA",
        33.3,
        "ISLAB hyvinvointiyhtymä",
        "2126106-6",
        "Diagnostiikka- ja laboratoriolaitetoimittajat",
        96.0,
        5.0,
        6.0,
        "kirjaamo@pshyva.fi",
        "Tilinpäätös 2024–2025: liikevaihto n. 96,0 M€. Lakisääteinen kolmen hyvinvointialueen laboratoriohyvinvointiyhtymä (julkisoikeudellinen yhtymä, yli 10 % omistusosuus); tehokkuustarkastelu koskee yksikköhintoja.",
    ),
    InHouseContractFlow(
        "Kuopio, Pshyva & yli 100 julkisyhteisöosakasta",
        0.3,
        "Sansia Oy",
        "2364760-8",
        "Yhteishankintojen puitesopimustoimittajat",
        18.4,
        6.0,
        7.0,
        "kirjaamo@kuopio.fi",
        "Tilinpäätös 2024–2025: liikevaihto n. 18,4 M€. Yhteishankinta- ja hankintapalveluyhtiö, jossa yli sadalla asiakasomistajalla on alle 10 % pienomistusosuus.",
    ),
    InHouseContractFlow(
        "Hyvinvointialueet ja kunnat (henkilökohtaisen avun palkanlaskenta)",
        0.1,
        "Kuntien Hetapalvelut Oy",
        "2642777-4",
        "Numera Palvelut Oy -konserni / palkkahallinnon järjestelmät",
        14.2,
        6.5,
        7.5,
        "kirjaamo@vakehyva.fi",
        "Tilinpäätös 2024–2025: liikevaihto n. 14,2 M€. Henkilökohtaisen avun työnantajamallin palkanlaskennan valtakunnallinen sidosyksikkö; hajautettu pienomistus (<10 %).",
    ),
]


# Alueellinen yksikkökustannusvertailu (P25-tehokkuuspotentiaali) 5 keskeisessä CPV-hankintakategoriassa.
# Luvut edustavat THL:n (Sotkanet / sote-yksikkökustannusraportit), HALI ry:n (esim. ympärivuorokautisen hoivan
# ostopalvelu n. 168–184 €/vrk vs. oma tuotanto / kalleimmat alueet 206–254 €/vrk) ja KKV:n tutkimusten mukaisia
# alueellisia yksikkökustannuseroja — eivät yksittäisten sopimusten tai yritysten väitettyjä väärinkäytöksiä.
BASELINE_PEER_SPEND: List[PeerCategorySpend] = [
    # 1. Vuokralääkäri- ja päivystyspalvelut (CPV 85121000, laskennallinen €/tunti aluevertailussa)
    PeerCategorySpend("Pirha (Pirkanmaa — viitetaso)",         "85121000-LocumMD", "hour", 110000, 115.0, "kirjaamo@pirha.fi"),
    PeerCategorySpend("Pohde (Pohjois-Pohjanmaa — viitetaso)", "85121000-LocumMD", "hour",  95000, 122.0, "kirjaamo@pohde.fi"),
    PeerCategorySpend("Varha (Varsinais-Suomi — viitetaso)",   "85121000-LocumMD", "hour",  90000, 128.0, "kirjaamo@varha.fi"),
    PeerCategorySpend("Keusote (Keski-Uusimaa — vertailu)",    "85121000-LocumMD", "hour",  65000, 148.0, "kirjaamo@keusote.fi"),
    PeerCategorySpend("Vake (Vantaa-Kerava — vertailu)",       "85121000-LocumMD", "hour",  75000, 172.0, "kirjaamo@vakehyva.fi"),
    PeerCategorySpend("Ekhva (Etelä-Karjala — vertailu)",      "85121000-LocumMD", "hour",  55000, 185.0, "kirjaamo@ekhva.fi"),
    PeerCategorySpend("Soite (Keski-Pohjanmaa — vertailu)",    "85121000-LocumMD", "hour",  45000, 192.0, "kirjaamo@soite.fi"),
    PeerCategorySpend("Lapha (Lappi — pitkien etäisyyksien päivystys)", "85121000-LocumMD", "hour", 85000, 205.0, "kirjaamo@lapha.fi"),

    # 2. IT-työasema- ja lähitukipalvelut (CPV 72260000, laskennallinen €/HTV/vuosi)
    PeerCategorySpend("Helsinki (Kaupunki — viitetaso)",       "72260000-ITWorkstation", "FTE-year", 38000, 1420.0, "helsinki.kirjaamo@hel.fi"),
    PeerCategorySpend("Tampere (Kaupunki — viitetaso)",        "72260000-ITWorkstation", "FTE-year", 15000, 1490.0, "kirjaamo@tampere.fi"),
    PeerCategorySpend("Pohde (Alueellinen ICT-vertailu)",      "72260000-ITWorkstation", "FTE-year", 18500, 1850.0, "kirjaamo@pohde.fi"),
    PeerCategorySpend("Varha (Alueellinen ICT-vertailu)",      "72260000-ITWorkstation", "FTE-year", 23000, 2240.0, "kirjaamo@varha.fi"),
    PeerCategorySpend("Pirha (Alueellinen ICT-vertailu)",      "72260000-ITWorkstation", "FTE-year", 21000, 2480.0, "kirjaamo@pirha.fi"),
    PeerCategorySpend("Pshyva (Alueellinen ICT-vertailu)",     "72260000-ITWorkstation", "FTE-year", 12800, 2650.0, "kirjaamo@pshyva.fi"),
    PeerCategorySpend("HUS / Vake (Erikoissairaanhoidon ICT)", "72260000-ITWorkstation", "FTE-year", 32000, 2980.0, "kirjaamo@hus.fi"),

    # 3. Asiakas- ja potilastietojärjestelmät APTJ (CPV 48814000, laskennallinen €/ammattilainen/vuosi)
    PeerCategorySpend("Pohde (Esko APTJ — viitetaso)",         "48814000-EHR", "clinician-year", 14000, 1650.0, "kirjaamo@pohde.fi"),
    PeerCategorySpend("Siun sote (Mediatri — viitetaso)",      "48814000-EHR", "clinician-year",  6500, 1820.0, "kirjaamo@siunsote.fi"),
    PeerCategorySpend("Pirha (Kokonais-APTJ-vertailu)",        "48814000-EHR", "clinician-year", 16500, 2850.0, "kirjaamo@pirha.fi"),
    PeerCategorySpend("Hyvaks (Keski-Suomi APTJ-vertailu)",    "48814000-EHR", "clinician-year",  9500, 3150.0, "kirjaamo@hyvaks.fi"),
    PeerCategorySpend("Vake (Apotti-osuus 18,7 % — kustannus/käyttäjä)", "48814000-EHR", "clinician-year", 4800, 5800.0, "kirjaamo@vakehyva.fi"),
    PeerCategorySpend("HUS & Helsingin sote (Apotti-osuus 81,3 % — kustannus/käyttäjä)", "48814000-EHR", "clinician-year", 19330, 6200.0, "kirjaamo@hus.fi"),

    # 4. Ikäihmisten ympärivuorokautinen palveluasuminen (CPV 85311100, THL / HALI ry yksikkökustannus €/hoitopäivä)
    PeerCategorySpend("Etelä-Pohjanmaa (Ostopalvelun P25-viitetaso)", "85311100-ElderlyCare", "resident-day",  820000, 172.0, "kirjaamo@hyvaep.fi"),
    PeerCategorySpend("Satakunta (Ostopalvelun viitetaso)",           "85311100-ElderlyCare", "resident-day",  890000, 178.0, "kirjaamo@sata.fi"),
    PeerCategorySpend("Pirha (Keskimääräinen hoitopäivähinta)",       "85311100-ElderlyCare", "resident-day", 1750000, 206.0, "kirjaamo@pirha.fi"),
    PeerCategorySpend("Luvn (Länsi-Uusimaa — korkea kustannustaso)",  "85311100-ElderlyCare", "resident-day", 1420000, 224.0, "kirjaamo@luvn.fi"),
    PeerCategorySpend("Helsinki (Oman tuotannon & ostopalvelun painotettu taso)", "85311100-ElderlyCare", "resident-day", 2100000, 238.0, "helsinki.kirjaamo@hel.fi"),
    PeerCategorySpend("Vake (Vantaa-Kerava — korkea kustannustaso)",  "85311100-ElderlyCare", "resident-day",  780000, 248.0, "kirjaamo@vakehyva.fi"),

    # 5. Lakisääteiset sote- ja koulukuljetukset (CPV 60130000, laskennallinen €/matka)
    PeerCategorySpend("Oulu / Pohde (Viitetaso)",              "60130000-SoteTransport", "trip",  950000, 26.5, "kirjaamo@pohde.fi"),
    PeerCategorySpend("Tampere / Pirha (Viitetaso)",           "60130000-SoteTransport", "trip", 1250000, 28.0, "kirjaamo@pirha.fi"),
    PeerCategorySpend("Turku / Varha (Aluevertailu)",          "60130000-SoteTransport", "trip",  880000, 34.0, "kirjaamo@varha.fi"),
    PeerCategorySpend("Keski-Suomi (Hyvaks — pitkät matkat)",  "60130000-SoteTransport", "trip",  720000, 41.0, "kirjaamo@hyvaks.fi"),
    PeerCategorySpend("Lappi (Lapha — harva asutus & etäisyydet)", "60130000-SoteTransport", "trip", 640000, 52.0, "kirjaamo@lapha.fi"),
]


# 10 Vahvistettua Markkinaoikeuden (MAO) ja Korkeimman hallinto-oikeuden (KHO) julkisten hankintojen ratkaisua (Finlex & KKV 2023–2025).
BASELINE_HILMA_TENDERS: List[HilmaTenderRecord] = [
    HilmaTenderRecord(
        "MAO:154/2024 & KHO 8.10.2025 (T2250)",
        "Vantaan ja Keravan hyvinvointialue (Vake)",
        "79211100-Payroll",
        9300000.0,
        0,
        True,
        24,
        "Sarastia Oy / Numera Palvelut Oy (2360731-5)",
        "kirjaamo@vakehyva.fi",
        "KKV:n esitys: 0,04 % osakeomistus ei täyttänyt hankintalain 15 §:n määräysvaltaedellytystä. MAO ja KHO totesivat suorahankinnan lainvastaiseksi ja lyhensivät sopimuskauden päättymään ennenaikaisesti.",
    ),
    HilmaTenderRecord(
        "MAO:500/2024 (D:377/2023)",
        "Varsinais-Suomen hyvinvointialue (Varha)",
        "79940000-Collections",
        1900000.0,
        0,
        True,
        18,
        "Revire Perintä Oy (Sarastia-konserni)",
        "kirjaamo@varha.fi",
        "KKV:n esitys: Varhan 0,09 % epäsuora omistusosuus ei tuottanut hankintalain 15 §:n mukaista sidosyksikköasemaa. Markkinaoikeus määräsi sopimukset päättymään ennenaikaisesti ja määräsi seuraamusmaksun.",
    ),
    HilmaTenderRecord(
        "MAO:611/2025 (D:324–340/2025)",
        "Pirkanmaan hyvinvointialue (Pirha)",
        "85311100-ElderlyCare",
        54000000.0,
        0,
        True,
        32,
        "Ikäihmisten ympärivuorokautisen palveluasumisen suorahankintasopimukset (17 kpl)",
        "kirjaamo@pirha.fi",
        "TampereMissio Palvelut Oy:n valitus: Pirha teki vuonna 2025 yhteensä n. 54 M€ suorahankintasopimukset ilman hankintalain mukaista kilpailutusta. Markkinaoikeus määräsi 500 000 € seuraamusmaksun.",
    ),
    HilmaTenderRecord(
        "MAO:537/2025",
        "Rovaniemen kaupunki",
        "79342000-Marketing",
        760000.0,
        0,
        True,
        15,
        "Matkailu- ja markkinointipalvelut (vuoden 2011 sopimuksen jatkaminen)",
        "kirjaamo@rovaniemi.fi",
        "KKV:n esitys: Kaupunki jatkoi matkailu- ja markkinointipalveluiden ostoja vanhan vuoden 2011 sopimuksen nojalla ilman kilpailutusta. Markkinaoikeus määräsi 40 000 € seuraamusmaksun.",
    ),
    HilmaTenderRecord(
        "MAO:202/2025 (D:610/2024)",
        "Etelä-Pohjanmaan hyvinvointialue (Hyvaep)",
        "72260000-IT",
        450000.0,
        0,
        True,
        14,
        "Vanha järjestelmätoimittaja (Effica-potilastietojen poiminta)",
        "kirjaamo@hyvaep.fi",
        "Atostek Oy:n valitus: Hyvinvointialue vetosi hankintalain 40 §:n tekniseen yksinoikeuteen potilastietojen poiminnassa, mutta markkinaoikeus kumosi suorahankintapäätöksen, koska myös kolmas osapuoli kykeni toteuttamaan työn.",
    ),
    HilmaTenderRecord(
        "MAO:748/2025",
        "Etelä-Savon hyvinvointialue (Eloisa)",
        "48000000-HRSoftware",
        1200000.0,
        0,
        True,
        16,
        "Työvuorosuunnittelu- ja HR-ohjelmistokokonaisuuden sopimusmuutos",
        "kirjaamo@etelasavonha.fi",
        "Visma Aquila Oy:n valitus: Markkinaoikeus arvioi hankintalain 136 §:n mukaista sopimuksen olennaista muuttamista sopimuskauden aikana ja velvollisuutta järjestää avoin kilpailutus.",
    ),
    HilmaTenderRecord(
        "MAO:665/2025",
        "Kanta-Hämeen HVA (Oma Häme) & Keski-Suomen HVA",
        "48814000-EHR",
        4800000.0,
        2,
        False,
        19,
        "Yhteishankintana kilpailutettu sote-tietojärjestelmäkokonaisuus",
        "kirjaamo@omahame.fi",
        "CGI Suomi Oy:n valitus: Markkinaoikeus arvioi hankinta-asiakirjojen muuttamista kesken hankintamenettelyn sekä tarjoajien tasapuolisen ja syrjimättömän kohtelun toteutumista (Hankintalaki 3 §).",
    ),
    HilmaTenderRecord(
        "MAO:553/2025",
        "Kanta-Hämeen HVA & yhteishankintakumppanit",
        "72260000-SpeechRec",
        3200000.0,
        2,
        False,
        12,
        "Lääketieteellinen puheentunnistuspalvelu usealle hyvinvointialueelle",
        "kirjaamo@omahame.fi",
        "Diktamen Oy:n ja Lingsoft Language Services Oy:n valitukset: Markkinaoikeus arvioi yhteishankinnan tarjouspyynnön mukaisuutta sekä poikkeuksellisen alhaisen tarjoushinnan selvittämisvelvollisuutta (Hankintalaki 96 §).",
    ),
    HilmaTenderRecord(
        "MAO:223/2023",
        "Hangon kaupunki",
        "85121000-LocumMD",
        1400000.0,
        0,
        True,
        15,
        "Terveyskeskuksen ajanvaraus- ja päivystysvastaanoton suorahankinnat (5 kk + 8 kk)",
        "kirjaamo@hanko.fi",
        "KKV:n esitys: Kaupunki ketjutti terveyskeskuksen lääkäri- ja vastaanottopalveluiden suorahankinnat kahdella peräkkäisellä sopimuksella (yht. 1,4 M€) ilman kilpailutusta. MAO määräsi 65 000 € seuraamusmaksun.",
    ),
    HilmaTenderRecord(
        "MAO:70/2023",
        "Isonkyrön kunta",
        "60130000-SoteTransport",
        1600000.0,
        0,
        True,
        22,
        "Koulukuljetusten suorahankinnat ilman kilpailutusta",
        "isonkyro@isonkyro.fi",
        "KKV:n esitys: Kunta hankki koulukuljetuspalveluita suorahankintoina yhteensä n. 1,6 M€ arvosta ilman hankintalain mukaista kilpailutusta. Markkinaoikeus määräsi 35 000 € seuraamusmaksun.",
    ),
]


# Complete Directory of All 43 Major Finnish Public Buyers:
# All 21 Wellbeing Counties (Hyvinvointialueet) + HUS-yhtymä + 21 Largest Finnish Municipalities
PUBLIC_BUYER_DIRECTORY: List[PublicBuyerProfile] = [
    # --- HUS + ALL 21 WELLBEING COUNTIES (HYVINVOINTIALUEET) ---
    PublicBuyerProfile("HUS-yhtymä", "HUS", "1567535-0", "kirjaamo@hus.fi", 1480.0, True, "Oy Apotti Ab, HUS Diagnostiikkakeskus / Hansel"),
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
        "schema_version": "2026.10.3",
        "national_procurement_pool_b_eur": 38.7,
        "target_annual_saving_range_b_eur": [1.1, 2.2],
        "inhouse_summary": inhouse_summary,
        "inhouse_flows": inhouse_rows,
        "arbitrage_summary": arbitrage_summary,
        "arbitrage_rows": arbitrage_rows,
        "flagged_hilma_tenders": flagged_tenders,
        "public_buyer_directory": [asdict(b) for b in PUBLIC_BUYER_DIRECTORY],
    }
