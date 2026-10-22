"""
Kartelli-Tutka — Hallinto-oikeudellisten Tutkinta-, Oikaisu- ja Tietopyyntöjen Asiallisgeneraattori.
Tuottaa 100 % maksuttomat (0,00 €), asialliset ja lakisääteiset hallintoasiakirjapohjat:
  1. KKV Toimenpidepyyntö / Valvontailmoitus (Hankintalaki 1397/2016 15 § ja 139–141 §, MAO:154/2024 & KHO 8.10.2025 taltio 2250) — 0 €
  2. Hankintaoikaisuvaatimus & Tarkastuslautakunnan arviointipyyntö (Hankintalaki 133 §, Hyvinvointialuelaki 125 §, Kuntalaki 121 §) — 0 €
  3. Julkisuuslain (621/1999) 13 §, 14.4 § ja 16.3 § mukainen ostolasku- ja osakassopimustietopyyntö — 0 €
  4. Tarjouspyynnön tarkistamispyyntö pk-yritysten osallistumisen mahdollistamiseksi (Hankintalaki 3 §, 67 §, 71 §, 75 § & 85 §) — 0 €
"""

from typing import Dict
from .engine import HilmaTenderRecord, InHouseContractFlow


def generate_kkv_complaint(flow: InHouseContractFlow, target_threshold_pct: float = 10.0) -> Dict[str, str]:
    """
    Tuottaa Kilpailu- ja kuluttajavirastolle (KKV) osoitetun asiallisen toimenpidepyynnön (Hankintalaki 139 §)
    sidosyksikköomistuksen määräysvaltaedellytyksen (Hankintalaki 15 §) tai puitesopimusten kilpailuttamisen selvittämiseksi.
    """
    effective_saving_fraction = 1.0 - (
        1.0 / ((1.0 + flow.inhouse_markup_pct / 100.0) * (1.0 + flow.subcontractor_uncompeted_premium_pct / 100.0))
    )
    annual_saving_m = round(flow.annual_spend_m_eur * effective_saving_fraction, 2)
    is_token_share = flow.buyer_equity_share_pct < target_threshold_pct

    if is_token_share:
        subject = (
            f"TOIMENPIDEPYYNTÖ (Hankintalaki 139 §): Sidosyksikköaseman edellytysten selvittäminen — "
            f"{flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) / {flow.buyer_name}"
        )
        legal_basis = f"""2. OIKEUDELLINEN PERUSTE (HANKINTALAKI 15 §, MAO:154/2024 JA KHO 8.10.2025 TALTIO 2250)
Julkisista hankinnoista ja käyttöoikeussopimuksista annetun lain (1397/2016, "hankintalaki") 15 §:n 1 momentin mukaan sidosyksikköpoikkeuksen soveltaminen edellyttää, että hankintayksikkö käyttää sidosyksikköön tosiasiallista määräysvaltaa samalla tavoin kuin omiin toimipaikkoihinsa ja tekee ratkaisevaa päätösvaltaa sidosyksikön strategisiin tavoitteisiin ja tärkeisiin päätöksiin.

Markkinaoikeuden päätöksessä MAO:154/2024 sekä korkeimman hallinto-oikeuden ennakkopäätöksessä KHO 8.10.2025 taltio 2250 on vahvistettu, ettei muodollinen pienomistus ({flow.buyer_equity_share_pct:.2f} %) ilman tosiasiallista päätösvaltaa täytä hankintalain 15 §:n edellytyksiä. Lisäksi hankintalain uudistuksen (HE 2/2026 vp) mukainen 10 prosentin vähimmäisomistusosuusraja täsmentää sidosyksikköpoikkeuksen soveltamisalaa.

Pyydämme KKV:tä selvittämään, täyttääkö pienosakkaiden ({flow.buyer_name}, viitteellinen pienomistusosuus {flow.buyer_equity_share_pct:.2f} %) suorahankintamenettely yhtiöltä {flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) hankintalain 15 §:n edellytykset vai tuleeko kyseiset palvelut kilpailuttaa avoimella menettelyllä."""
    else:
        subject = (
            f"TOIMENPIDEPYYNTÖ (Hankintalaki 139 §): Sopimusmuutosten ja puitesopimusketjujen tarkastelu — "
            f"{flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) / {flow.buyer_name}"
        )
        legal_basis = f"""2. OIKEUDELLINEN PERUSTE (HANKINTALAKI 3 §, 15 § JA 136 § / LAKI 1226/2013)
Vaikka tilaajaryhmän ({flow.buyer_name}) omistus- tai ohjausosuus yksikössä {flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) on {flow.buyer_equity_share_pct:.2f} %, hankintalain 3 §:n ja 136 §:n mukaan sopimuskauden aikaiset olennaiset sopimuslaajennukset ja markkinoilta hankittavat alihankintakokonaisuudet on kilpailutettava avoimesti ja syrjimättömästi (ks. myös hankintalain 75 § hankinnan jakamisesta osiin).

Pyydämme KKV:tä arvioimaan, ovatko yksikön ({flow.inhouse_vendor}) sopimuskokonaisuudet ja lisätilaukset hankintalain 15 §:n ja 136 §:n mukaisia ja voitaisiinko osakokonaisuuksien avoimella kilpailutuksella saavuttaa arvioitu {annual_saving_m:.2f} milj. EUR/v kustannussäästö."""

    body = f"""VASTAANOTTAJA: Kilpailu- ja kuluttajavirasto (KKV) — Hankintojen valvonta (kirjaamo@kkv.fi)
ASIA: {subject}
KÄSITTELYMAKSU: 0,00 € (Hankintalaki 1397/2016 139 § mukainen toimenpidepyyntö)

1. SELVITYSPYYNNÖN KOHDE
- Hankintayksikkö / tilaajaryhmä: {flow.buyer_name}
- Sidosyksikkö / palvelukeskus: {flow.inhouse_vendor} (Y-tunnus: {flow.inhouse_y_tunnus})
- Viitteellinen pienosakkaan tai osakkaan omistusosuus: {flow.buyer_equity_share_pct:.2f} % (vertailuraja: {target_threshold_pct:.1f} %)
- Puitesopimus- ja alihankintakategoria: {flow.subcontractor_vendor}
- Yksikön vuotuinen kokonaisliikevaihto (tilinpäätös 2024–2025): {flow.annual_spend_m_eur:.2f} milj. EUR / vuosi
- Laskennallinen tehokkuuspotentiaali (KKV/VATT-vertailumalli): {annual_saving_m:.2f} milj. EUR / vuosi (hallinnollinen koordinointikate {flow.inhouse_markup_pct:.1f} % + avoimen kilpailutuksen säästöpotentiaali {flow.subcontractor_uncompeted_premium_pct:.1f} %)

{legal_basis}

3. PYYNTÖ KILPAILU- JA KULUTTAJAVIRASTOLLE
Pyydämme Kilpailu- ja kuluttajavirastoa hankintalain 139–141 §:n nojalla:
1) Selvittämään, täyttävätkö pienosakkaiden ({flow.buyer_name}) suorahankinnat yksiköltä {flow.inhouse_vendor} (Y-tunnus {flow.inhouse_y_tunnus}) hankintalain 15 §:n ja KHO 8.10.2025 (taltio 2250) mukaiset edellytykset;
2) Antamaan tarvittaessa hankintalain 140 §:n mukaisen huomautuksen tai ohjauksen avoimen kilpailutuksen järjestämisestä.
"""
    return {
        "recipient_email": "kirjaamo@kkv.fi",
        "subject": subject,
        "body": body.strip(),
        "filing_fee_eur": "0.00",
    }


def generate_hankintaoikaisu(flow: InHouseContractFlow, buyer_kirjaamo_email: str = "kirjaamo@hyvinvointialue.fi") -> Dict[str, str]:
    """
    Tuottaa asiallisen hankintaoikaisupyynnön (Hankintalaki 133 §) ja tarkastuslautakunnalle
    osoitetun taloudellisen tarkoituksenmukaisuuden arviointipyynnön (Hyvinvointialuelaki 125 § / Kuntalaki 121 §).
    """
    is_token_share = flow.buyer_equity_share_pct < 10.0
    reason_line = (
        f"Pienosakkaiden omistusosuus ({flow.buyer_equity_share_pct:.2f} %) alittaa korkeimman hallinto-oikeuden ennakkopäätöksessä "
        f"(KHO 8.10.2025 taltio 2250 & MAO:154/2024) linjatun tosiasiallisen määräysvallan kynnyksen sekä 10,0 % sidosyksikkörajan."
        if is_token_share
        else f"Yksikön ({flow.inhouse_vendor}) sopimuskokonaisuuksien yksikkökustannuksia ja osakokonaisuuksien suoraa kilpailuttamista "
        f"(Hankintalaki 75 § & 136 §) tulisi verrata avoimen markkinan hintatasoon."
    )
    subject = (
        f"HANKINTAOIKAISUPYYNTÖ (Hankintalaki 133 §) & TARKASTUSLAUTAKUNNAN ARVIOINTIPYYNTÖ: "
        f"{flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) hankintojen kilpailuttaminen"
    )
    body = f"""VASTAANOTTAJA: {flow.buyer_name} — Kirjaamo & Tarkastuslautakunta ({buyer_kirjaamo_email})
ASIA: {subject}
KÄSITTELYMAKSU: 0,00 € (Hankintalaki 133 § / Hyvinvointialuelaki 125 § / Kuntalaki 121 §)

1. PYYNTÖ HANKINTAMENETTELYN JA KUSTANNUSTEHOKKUUDEN ARVIOIMISEKSI
Esitämme hankintalain (1397/2016) 133 §:n sekä hyvinvointialuelain 125 §:n (tai kuntalain 121 §:n) nojalla, että hankintayksikkö ({flow.buyer_name}) ja sen tarkastuslautakunta arvioivat yksiköltä {flow.inhouse_vendor} (Y-tunnus {flow.inhouse_y_tunnus}, kokonaisliikevaihto {flow.annual_spend_m_eur:.2f} milj. EUR/v) tehtävien sidosyksikköhankintojen lainmukaisuuden ja kustannustehokkuuden verrattuna avoimeen kilpailutukseen.

2. OIKEUDELLISET JA TALOUDELLISET PERUSTELUT (MAO:154/2024 & KHO 8.10.2025)
{reason_line}

Pyydämme tarkastuslautakuntaa arvioimaan osana lakisääteistä tuloksellisuuden ja tarkoituksenmukaisuuden arviointiaan, kuinka suuri kustannussäästö saavutettaisiin kilpailuttamalla palvelut avoimella menettelyllä ja jakamalla hankinnat osiin hankintalain 75 §:n mukaisesti.
"""
    return {
        "recipient_email": buyer_kirjaamo_email,
        "subject": subject,
        "body": body.strip(),
        "filing_fee_eur": "0.00",
    }


def generate_julkisuuslaki_foia(entity_name: str, kirjaamo_email: str, year: int = 2026) -> Dict[str, str]:
    """
    Generates a mandatory Julkisuuslaki (621/1999) § 13, § 14.4 & § 16.3 digital FOIA request
    requesting a municipality or Wellbeing County to release machine-readable purchase invoices within 14 days.
    """
    subject = f"TIETOPYYNTÖ (Julkisuuslaki 621/1999 13 § ja 16 §): {entity_name} — ostolaskuaineisto ja sidosyksikkösopimukset ({year})"
    body = f"""VASTAANOTTAJA: {entity_name} — Kirjaamo ({kirjaamo_email})
ASIA: {subject}

Pyydän viranomaisten toiminnan julkisuudesta annetun lain (621/1999, "julkisuuslaki") 9 §:n, 13 §:n ja 16 §:n 3 momentin nojalla toimittamaan sähköisesti koneluettavassa muodossa (CSV- tai XLSX-taulukko) seuraavat julkiset asiakirjat:

1. Viranomaisen ({entity_name}) maksetut ostolaskut (ostolaskudata) ajalta 1.1.{year - 1}–tähän päivään, sisältäen julkiset sarakkeet:
   - Toimittajan virallinen nimi ja Y-tunnus
   - Laskun päivämäärä, tositenumero ja euromäärä (alv 0 %)
   - Tiliöinti (tililuokka / tehtäväluokka / kustannuspaikka / CPV-koodi)
   - Tieto siitä, perustuuko hankinta avoimeen kilpailutukseen (Hilma-ilmoitusnumero), suorahankintaan vai sidosyksikköhankintaan.

2. Voimassa olevat sidosyksikköjen (mm. Istekki Oy, 2M-IT Oy, Numera Palvelut Oy / Sarastia, Monetra Oy, Tiera Oy, Oy Apotti Ab, Fimlab Laboratoriot Oy) osakassopimukset, viranomaisen omistusosuus (% osakekannasta ja äänivallasta) sekä palvelusopimusten julkiset hinnastoliitteet.

Julkisuuslain 14 §:n 4 momentin mukaan tietopyyntö on käsiteltävä viivytyksettä ja tiedot on luovutettava viimeistään 14 vuorokauden kuluessa (tai laajoissa erityistapauksissa viimeistään 1 kuukauden kuluessa) pyynnön vastaanottamisesta. Pyydän toimittamaan aineiston vastauksena tähän sähköpostiin.
"""
    return {
        "recipient_email": kirjaamo_email,
        "subject": subject,
        "body": body.strip(),
        "filing_fee_eur": "0.00",
    }


def generate_hilma_spec_challenge(tender: HilmaTenderRecord, buyer_email: str = "hankinnat@hankintayksikko.fi") -> Dict[str, str]:
    """
    Tuottaa asiallisen pyynnön hankintamenettelyn avoimuuden ja osiin jakamisen (Hankintalaki 3 §, 67 §, 75 § & 133 §)
    varmistamiseksi markkinaoikeuden (MAO) ja KHO:n ratkaisukäytännön mukaisesti.
    """
    expected_saving_eur = round(tender.contract_value_eur * (0.25 if (tender.bids_received <= 1 or tender.is_direct_award) else 0.16), 2)
    subject = (
        f"ESITYS AVOIMEN KILPAILUTUKSEN JA OSIIN JAKAMISEN TOTEUTTAMISEKSI (Hankintalaki 67 §, 75 § & 133 §): "
        f"{tender.tender_id} — {tender.buyer_name} ({tender.cpv_code})"
    )
    body = f"""VASTAANOTTAJA: {tender.buyer_name} — Hankintatoimi & Kirjaamo ({buyer_email})
ASIA: {subject}

1. OIKEustapausviite JA KILPAILUN AVAAMINEN ({tender.tender_id})
Viitaten hankintatapaukseen {tender.tender_id} (CPV-luokka {tender.cpv_code}, sopimusarvo {tender.contract_value_eur:,.0f} EUR, tarjoukset: {tender.bids_received} kpl; oikeustapauskuvaus: {tender.lockout_reason}), toimialalla toimii arviolta vähintään {tender.qualified_eu_sme_pool_size} kelpoisuusehdot täyttävää suomalaista ja EU-alueen toimittajaa.

Hankintalain (1397/2016) 3 §:n, 67 §:n, 71 §:n, 75 §:n ja 85 §:n mukaan hankinnat on kilpailutettava avoimesti ja jaettava tarkoituksenmukaisiin osakokonaisuuksiin siten, että myös pk-yrityksillä on tasapuolinen mahdollisuus jättää tarjous.

2. ESITYS HANKINTAYKSIKÖLLE
Esitämme hankintalain 3 §:n, 67 §:n, 75 §:n ja 133 §:n nojalla, että {tender.buyer_name} tulevissa vastaavissa hankinnoissa:
1) Varmistaa avoimen kilpailutuksen ilman hankintalain 15 §:n tai 40 §:n vastaista suorahankintaa;
2) Jakaa hankinnan hankintalain 75 §:n mukaisesti osakokonaisuuksiin useamman tarjoajan osallistumisen turvaamiseksi;
3) Asettaa soveltuvuus- ja liikevaihtovaatimukset hankintalain 85 §:n suhteellisuusperiaatteen mukaisiksi.
"""
    return {
        "recipient_email": buyer_email,
        "subject": subject,
        "body": body.strip(),
        "filing_fee_eur": "0.00",
    }
