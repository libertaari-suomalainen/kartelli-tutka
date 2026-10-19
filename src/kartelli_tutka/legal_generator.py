"""
Kartelli-Tutka Zero-Fee Legal & Regulatory Filing Compiler.
Generates deterministic, statutory Finnish filings:
  1. KKV Toimenpidepyyntö (Hankintalaki 1397/2016 § 15, § 139–141 & MAO:154/2024) — 0€ fee
  2. Hankintaoikaisuvaatimus & Alue-/Kuntalaisvalitus (Hankintalaki § 133) — 0€ fee
  3. Julkisuuslaki (621/1999) § 13 & § 16 Ostolaskudata & Osakassopimus FOIA Request — 0€ fee
  4. Hilma Pre-Award Discriminatory Spec Challenge (Hankintalaki § 2, § 67–68) — 0€ fee
"""

from typing import Dict
from .engine import HilmaTenderRecord, InHouseContractFlow


def generate_kkv_complaint(flow: InHouseContractFlow, target_threshold_pct: float = 10.0) -> Dict[str, str]:
    """
    Generates a ready-to-file Kilpailu- ja kuluttajavirasto (KKV) supervision complaint
    for illegal direct awards (laiton suorahankinta) via nominal Sidosyksikkö shareholding.
    """
    effective_saving_fraction = 1.0 - (
        1.0 / ((1.0 + flow.inhouse_markup_pct / 100.0) * (1.0 + flow.subcontractor_uncompeted_premium_pct / 100.0))
    )
    annual_overcharge_m = round(flow.annual_spend_m_eur * effective_saving_fraction, 2)

    subject = (
        f"TOIMENPIDEPYYNTÖ (Hankintalaki 139 §): Laiton suorahankinta / näennäinen sidosyksikköasema — "
        f"{flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) / {flow.buyer_name}"
    )

    body = f"""VASTAANOTTAJA: Kilpailu- ja kuluttajavirasto (KKV) — Hankintojen valvonta (kirjaamo@kkv.fi)
ASIA: {subject}
KÄSITTELYMAKSU: 0,00 € (Hankintalaki 1397/2016 § 139 mukainen valvontailmoitus)

1. VALVONTAILMOITUKSEN KOHDE
- Hankintayksikkö / ostajaryhmä: {flow.buyer_name}
- Välikätenä toimiva sidosyksikkö: {flow.inhouse_vendor} (Y-tunnus: {flow.inhouse_y_tunnus})
- Hankintayksikön omistusosuus sidosyksikössä: {flow.buyer_equity_share_pct:.2f} % (lakisääteinen vähimmäisvaatimus / määräysvaltaraja: {target_threshold_pct:.1f} %)
- Tosiasialliset alihankkijat / toimittajat: {flow.subcontractor_vendor}
- Suorahankintojen vuotuinen arvo: {flow.annual_spend_m_eur:.2f} milj. EUR / vuosi
- Arvioitu ylihinta / välikäsikate veronmaksajille: {annual_overcharge_m:.2f} milj. EUR / vuosi (sidosyksikkökate {flow.inhouse_markup_pct:.0f} % + kilpailuttamaton alihankintapreemio {flow.subcontractor_uncompeted_premium_pct:.0f} %)

2. OIKEUDELLINEN PERUSTE (HANKINTALAKI 15 §, MAO:154/2024 JA KHO:N OIKEUSKÄYTÄNTÖ)
Julkisista hankinnoista ja käyttöoikeussopimuksista annetun lain (1397/2016, "hankintalaki") 15 §:n 1 momentin mukaan sidosyksikköpoikkeuksen soveltaminen edellyttää, että hankintayksikkö käyttää sidosyksikköön tosiasiallista määräysvaltaa samalla tavoin kuin omiin toimipaikkoihinsa ja tekee ratkaisevaa päätösvaltaa sidosyksikön strategisiin tavoitteisiin ja tärkeisiin päätöksiin.

Markkinaoikeuden lainvoimaisessa päätöksessä MAO:154/2024 (sekä KHO:n ennakkopäätöksessä) on vahvistettu, ettei muodollinen pienomistus ({flow.buyer_equity_share_pct:.2f} %) ja näennäinen nimitysoikeus ilman todellista päätösvaltaa täytä hankintalain 15 §:n edellytyksiä. Lisäksi hallitusohjelman mukainen 10 prosentin vähimmäisomistusosuusraja estää keinotekoiset osakekaupat.

Koska {flow.buyer_name} omistaa yhtiöstä {flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) ainoastaan {flow.buyer_equity_share_pct:.2f} %, yhtiö ei ole hankintalain 15 §:ssä tarkoitettu sidosyksikkö. Lisäksi {flow.inhouse_vendor} ketjuttaa hankinnat ilman avointa kilpailutusta suoraan yksityisille suuryrityksille ({flow.subcontractor_vendor}). Jokainen hankintayksikön tekemä tilaus on siten hankintalain 15 §:n ja 40 §:n vastainen LAITON SUORAHANKINTA.

3. VAATIMUKSET KILPAILU- JA KULUTTAJAVIRASTOLLE
Pyydämme Kilpailu- ja kuluttajavirastoa hankintalain 139–141 §:n nojalla:
1) Käynnistämään välittömästi tutkinnan {flow.buyer_name}n ja {flow.inhouse_vendor}n ({flow.inhouse_y_tunnus}) välisistä suorahankinnoista ({flow.annual_spend_m_eur:.2f} milj. EUR/v);
2) Esittämään markkinaoikeudelle hankintalain 156 §:n mukaisen TEHOTTOMUUSSEURAAMUKSEN määräämistä voimassa oleville sopimuksille;
3) Esittämään markkinaoikeudelle hankintalain 158 §:n mukaisen SEURAAMUSMAKSUN määräämistä sekä sopimuskauden lyhentämistä siten, että palvelut avataan välittömästi avoimeen kilpailutukseen.
"""
    return {
        "recipient_email": "kirjaamo@kkv.fi",
        "subject": subject,
        "body": body.strip(),
        "filing_fee_eur": "0.00",
    }


def generate_hankintaoikaisu(flow: InHouseContractFlow, buyer_kirjaamo_email: str = "kirjaamo@hyvinvointialue.fi") -> Dict[str, str]:
    """
    Generates a Hankintaoikaisuvaatimus (Hankintalaki § 133) + Municipal/Regional Complaint
    putting the buyer's board on formal legal notice of personal liability (virkavastuu).
    """
    subject = (
        f"HANKINTAOIKAISUVAATIMUS (Hankintalaki 133 §) & ALUE-/KUNTALAISVALITUS: "
        f"{flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) suorahankintojen välitön keskeyttäminen"
    )
    body = f"""VASTAANOTTAJA: {flow.buyer_name} — Kirjaamo & Hallitus / Tarkastuslautakunta ({buyer_kirjaamo_email})
ASIA: {subject}
KÄSITTELYMAKSU: 0,00 € (Hankintalaki 133 § / Hyvinvointialuelaki 140 § / Kuntalaki 135 §)

1. VAATIMUS HANKINTAPÄÄTÖSTEN OIKAISEMISEKSI JA SOPIMUSTEN IRTISANOMISEKSI
Vaadimme hankintalain (1397/2016) 133 §:n nojalla, että {flow.buyer_name} oikaisee välittömästi {flow.inhouse_vendor}lta (Y-tunnus {flow.inhouse_y_tunnus}) tehdyt suorahankintapäätökset ({flow.annual_spend_m_eur:.2f} milj. EUR/v), irtisanoo lainvastaiset puitesopimukset ja kilpailuttaa palvelut avoimella menettelyllä.

2. PERUSTELUT JA VIRKAVASTUU (MAO:154/2024)
Hankintayksikön omistusosuus ({flow.buyer_equity_share_pct:.2f} %) alittaa sekä tosiasiallisen määräysvallan kynnyksen (MAO:154/2024) että lakisääteisen 10,0 % sidosyksikkörajan. Välikätenä toimiva {flow.inhouse_vendor} perii {flow.inhouse_markup_pct:.0f} % sisäisen katteen ja ohjaa tilaukset kilpailuttamatta edelleen toimittajille ({flow.subcontractor_vendor}).

Mikäli hallitus jatkaa suorahankintoja tietoisena MAO:154/2024 ja KHO:n ratkaisuista, päätöksentekijät syyllistyvät tahalliseen hankintalain rikkomiseen (virkavelvollisuuden rikkominen, RL 40:9–10 §) ja aiheuttavat veronmaksajille korvattavan vahingon. Vaadimme asian viemistä tarkastuslautakunnan ja tilintarkastajan käsittelyyn.
"""
    return {
        "recipient_email": buyer_kirjaamo_email,
        "subject": subject,
        "body": body.strip(),
        "filing_fee_eur": "0.00",
    }


def generate_julkisuuslaki_foia(entity_name: str, kirjaamo_email: str, year: int = 2026) -> Dict[str, str]:
    """
    Generates a mandatory Julkisuuslaki (621/1999) § 13 & § 16 digital FOIA request
    forcing a municipality or Wellbeing County to release machine-readable purchase invoices within 14 days.
    """
    subject = f"TIETOPYYNTÖ (Julkisuuslaki 621/1999 13 § ja 16 §): {entity_name} ostolaskuaineisto ja sidosyksikkösopimukset ({year})"
    body = f"""VASTAANOTTAJA: {entity_name} — Kirjaamo ({kirjaamo_email})
ASIA: {subject}

Pyydän viranomaisten toiminnan julkisuudesta annetun lain (621/1999, "julkisuuslaki") 9 §:n, 13 §:n ja 16 §:n 3 momentin nojalla toimittamaan sähköisesti koneluettavassa muodossa (CSV- tai XLSX-taulukko) seuraavat julkiset asiakirjat:

1. {entity_name}n kaikki maksetut ostolaskut (ostolaskudata) ajalta 1.1.{year - 1}–tähän päivään, sisältäen sarakkeet:
   - Toimittajan virallinen nimi ja Y-tunnus
   - Laskun päivämäärä, tositenumero ja euromäärä (alv 0 %)
   - Tiliöinti (tililuokka / tehtäväluokka / kustannuspaikka / CPV-koodi)
   - Tieto siitä, perustuuko hankinta avoimeen kilpailutukseen (Hilma-ilmoitusnumero), suorahankintaan vai sidosyksikköhankintaan.

2. Kaikki voimassa olevat sidosyksikköjen (mm. Istekki Oy, 2M-IT Oy, Numera Palvelut Oy / Sarastia, Monetra Oy, Tiera Oy, Oy Apotti Ab) osakassopimukset, omistusosuudet (% osakekannasta ja äänivallasta) sekä palvelusopimusten hinnastoliitteet.

Julkisuuslain 14 §:n 4 momentin mukaan tietopyyntö on käsiteltävä viivytyksettä ja tiedot on luovutettava viimeistään 14 vuorokauden kuluessa pyynnön vastaanottamisesta. Pyydän toimittamaan aineiston vastauksena tähän sähköpostiin.
"""
    return {
        "recipient_email": kirjaamo_email,
        "subject": subject,
        "body": body.strip(),
        "filing_fee_eur": "0.00",
    }


def generate_hilma_spec_challenge(tender: HilmaTenderRecord, buyer_email: str = "hankinnat@hankintayksikko.fi") -> Dict[str, str]:
    """
    Generates a Pre-Award Discriminatory Spec Challenge (Hankintalaki § 2, § 67–68 & § 133)
    forcing the buyer to open a rigged 1-bid tender to qualified SMEs.
    """
    expected_saving_eur = round(tender.contract_value_eur * (0.25 if (tender.bids_received <= 1 or tender.is_direct_award) else 0.16), 2)
    subject = (
        f"VAATIMUS SYRJIVIEN VAATIMUSTEN POISTAMISEKSI (Hankintalaki 67 § & 133 §): "
        f"Hilma {tender.tender_id} — {tender.buyer_name} ({tender.cpv_code})"
    )
    body = f"""VASTAANOTTAJA: {tender.buyer_name} — Hankintatoimi & Kirjaamo ({buyer_email})
ASIA: {subject}

1. KILPAILUA RAJOITTAVAN HANKINTAILMOITUKSEN / SUORAHANKINNAN OIKAISUVAATIMUS
Viitaten hankintaan {tender.tender_id} (CPV-luokka {tender.cpv_code}, ennakoitu arvo {tender.contract_value_eur:,.0f} EUR, saadut tarjoukset: {tender.bids_received} kpl), huomautamme, että markkinoilla toimii vähintään {tender.qualified_eu_sme_pool_size} täysin kelpoisuusehdot täyttävää suomalaista ja EU-alueen pk-toimittajaa.

Hankintalain (1397/2016) 2 §:n ja 67 §:n mukaan hankinnan teknisiä eritelmiä ja soveltuvuusvaatimuksia ei saa laatia siten, että ne keinotekoisesti rajoittavat kilpailua tai suosivat yhtä vakiintunutta toimittajaa. Yhden tai kahden tarjouksen kilpailutus tässä kokoluokassa aiheuttaa veronmaksajille arviolta {expected_saving_eur:,.0f} EUR vuotuisen ylihinnan.

2. VAATIMUKSET HANKINTAYKSIKÖLLE
Vaadimme hankintalain 67 §:n, 73 §:n (hankinnan jakaminen osiin) ja 133 §:n nojalla, että {tender.buyer_name}:
1) Poistaa tarjouspyynnöstä kilpailua rajoittavat, tietylle toimittajalle räätälöidyt viite- ja sertifikaattivaatimukset;
2) Jakaa hankinnan hankintalain 73 §:n mukaisesti osakokonaisuuksiin pk-yritysten osallistumisen mahdollistamiseksi;
3) Jatkaa tarjousaikaa vähintään 14 vuorokaudella korjatun hankintailmoituksen julkaisemisesta.
"""
    return {
        "recipient_email": buyer_email,
        "subject": subject,
        "body": body.strip(),
        "filing_fee_eur": "0.00",
    }
