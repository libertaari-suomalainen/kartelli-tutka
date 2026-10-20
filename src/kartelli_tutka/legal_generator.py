"""
Kartelli-Tutka Zero-Fee Legal & Regulatory Filing Compiler.
Generates deterministic, statutory Finnish filings:
  1. KKV Toimenpidepyyntö (Hankintalaki 1397/2016 § 15, § 139–141, MAO:154/2024 & KHO 8.10.2025 taltio 2250) — 0€ fee
  2. Hankintaoikaisuvaatimus & Alue-/Kuntalaisvalitus (Hankintalaki § 133) — 0€ fee
  3. Julkisuuslaki (621/1999) § 13, § 14.4 & § 16.3 Ostolaskudata & Osakassopimus FOIA Request — 0€ fee
  4. Hilma Pre-Award Discriminatory Spec Challenge (Hankintalaki § 3, § 67, § 71, § 75 & § 85) — 0€ fee
"""

from typing import Dict
from .engine import HilmaTenderRecord, InHouseContractFlow


def generate_kkv_complaint(flow: InHouseContractFlow, target_threshold_pct: float = 10.0) -> Dict[str, str]:
    """
    Generates a ready-to-file Kilpailu- ja kuluttajavirasto (KKV) supervision complaint
    for illegal direct awards (laiton suorahankinta) via nominal Sidosyksikkö shareholding
    or uncompeted subcontracting chain / monopoly lock-in.
    """
    effective_saving_fraction = 1.0 - (
        1.0 / ((1.0 + flow.inhouse_markup_pct / 100.0) * (1.0 + flow.subcontractor_uncompeted_premium_pct / 100.0))
    )
    annual_overcharge_m = round(flow.annual_spend_m_eur * effective_saving_fraction, 2)
    is_token_share = flow.buyer_equity_share_pct < target_threshold_pct

    if is_token_share:
        subject = (
            f"TOIMENPIDEPYYNTÖ (Hankintalaki 139 §): Laiton suorahankinta / näennäinen sidosyksikköasema — "
            f"{flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) / {flow.buyer_name}"
        )
        legal_basis = f"""2. OIKEUDELLINEN PERUSTE (HANKINTALAKI 15 §, MAO:154/2024 JA KHO 8.10.2025 TALTIO 2250)
Julkisista hankinnoista ja käyttöoikeussopimuksista annetun lain (1397/2016, "hankintalaki") 15 §:n 1 momentin mukaan sidosyksikköpoikkeuksen soveltaminen edellyttää, että hankintayksikkö käyttää sidosyksikköön tosiasiallista määräysvaltaa samalla tavoin kuin omiin toimipaikkoihinsa ja tekee ratkaisevaa päätösvaltaa sidosyksikön strategisiin tavoitteisiin ja tärkeisiin päätöksiin.

Markkinaoikeuden päätöksessä MAO:154/2024 sekä korkeimman hallinto-oikeuden päätöksessä KHO 8.10.2025 taltio 2250 on vahvistettu, ettei muodollinen pienomistus ({flow.buyer_equity_share_pct:.2f} %) ja näennäinen nimitysoikeus ilman todellista päätösvaltaa täytä hankintalain 15 §:n edellytyksiä. Lisäksi hankintalain uudistuksen (HE 2/2026 vp) mukainen 10 prosentin vähimmäisomistusosuusraja estää keinotekoiset kuoriosakejärjestelyt.

Koska tilaaja ({flow.buyer_name}) omistaa yhtiöstä {flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) ainoastaan {flow.buyer_equity_share_pct:.2f} %, yhtiö ei ole kyseisille vähemmistöosakkaille hankintalain 15 §:ssä tarkoitettu sidosyksikkö. Lisäksi {flow.inhouse_vendor} ketjuttaa hankinnat ilman avointa kilpailutusta edelleen yksityisille suuryrityksille ({flow.subcontractor_vendor}). Jokainen ilman kilpailutusta tehty tilaus on siten hankintalain 15 §:n ja 40 §:n vastainen LAITON SUORAHANKINTA."""
    else:
        subject = (
            f"TOIMENPIDEPYYNTÖ (Hankintalaki 139 §): Kilpailuttamaton alihankintaketjutus ja sopimuslukitus — "
            f"{flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) / {flow.buyer_name}"
        )
        legal_basis = f"""2. OIKEUDELLINEN PERUSTE (HANKINTALAKI 3 §, 15 §, 40 § JA 136 § / LAKI 1226/2013)
Vaikka tilaajaryhmän ({flow.buyer_name}) omistus- tai ohjausosuus yksikössä {flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) on {flow.buyer_equity_share_pct:.2f} %, hankintalain 15 §:n sidosyksikköpoikkeus tai valtion yhteisten tieto- ja viestintäteknisten palvelujen järjestämisestä annettu laki (1226/2013) ei oikeuta ketjuttamaan hankintoja kilpailuttamatta yksityisille toimittajille ({flow.subcontractor_vendor}) eikä tekemään hankintalain 136 §:n vastaisia olennaisia sopimuslaajennuksia ilman uutta kilpailutusta.

Välikätenä toimiva {flow.inhouse_vendor} perii arviolta {flow.inhouse_markup_pct:.0f} % sisäisen hallintokatteen ja ohjaa tilaukset edelleen toimittajille ({flow.subcontractor_vendor}), mikä vääristää markkinakilpailua hankintalain 3 §:n vastaisesti ja aiheuttaa arviolta {annual_overcharge_m:.2f} milj. EUR/v ylihinnan."""

    body = f"""VASTAANOTTAJA: Kilpailu- ja kuluttajavirasto (KKV) — Hankintojen valvonta (kirjaamo@kkv.fi)
ASIA: {subject}
KÄSITTELYMAKSU: 0,00 € (Hankintalaki 1397/2016 § 139 mukainen valvontailmoitus)

1. VALVONTAILMOITUKSEN KOHDE
- Hankintayksikkö / ostajaryhmä: {flow.buyer_name}
- Välikätenä toimiva yksikkö: {flow.inhouse_vendor} (Y-tunnus: {flow.inhouse_y_tunnus})
- Hankintayksikön omistusosuus: {flow.buyer_equity_share_pct:.2f} % (lakisääteinen sidosyksikköraja: {target_threshold_pct:.1f} %)
- Tosiasialliset alihankkijat / toimittajat: {flow.subcontractor_vendor}
- Suorahankintojen vuotuinen arvo: {flow.annual_spend_m_eur:.2f} milj. EUR / vuosi
- Arvioitu ylihinta / välikäsikate veronmaksajille: {annual_overcharge_m:.2f} milj. EUR / vuosi (välikäsikate {flow.inhouse_markup_pct:.0f} % + kilpailuttamaton alihankintapreemio {flow.subcontractor_uncompeted_premium_pct:.0f} %)

{legal_basis}

3. VAATIMUKSET KILPAILU- JA KULUTTAJAVIRASTOLLE
Pyydämme Kilpailu- ja kuluttajavirastoa hankintalain 139–141 §:n nojalla:
1) Käynnistämään välittömästi tutkinnan hankintayksikön ({flow.buyer_name}) ja toimittajan ({flow.inhouse_vendor}, Y-tunnus {flow.inhouse_y_tunnus}) välisistä suorahankinnoista ja ketjutetuista alihankintasopimuksista ({flow.annual_spend_m_eur:.2f} milj. EUR/v);
2) Esittämään markkinaoikeudelle hankintalain 156 §:n mukaisen TEHOTTOMUUSSEURAAMUKSEN määräämistä lainvastaisille suorahankintasopimuksille;
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
    requesting audit committee review of official liability (virkavastuu).
    """
    is_token_share = flow.buyer_equity_share_pct < 10.0
    reason_line = (
        f"Hankintayksikön omistusosuus ({flow.buyer_equity_share_pct:.2f} %) alittaa sekä tosiasiallisen määräysvallan kynnyksen "
        f"(MAO:154/2024 & KHO 8.10.2025 taltio 2250) että lakisääteisen 10,0 % sidosyksikkörajan."
        if is_token_share
        else f"Yksikkö ({flow.inhouse_vendor}) perii {flow.inhouse_markup_pct:.0f} % sisäisen hallintolisän ja ketjuttaa lisätilaukset "
        f"ilman hankintalain 136 §:n edellyttämää avointa kilpailutusta toimittajille ({flow.subcontractor_vendor})."
    )
    subject = (
        f"HANKINTAOIKAISUVAATIMUS (Hankintalaki 133 §) & ALUE-/KUNTALAISVALITUS: "
        f"{flow.inhouse_vendor} ({flow.inhouse_y_tunnus}) suorahankintojen välitön tarkastaminen"
    )
    body = f"""VASTAANOTTAJA: {flow.buyer_name} — Kirjaamo & Hallitus / Tarkastuslautakunta ({buyer_kirjaamo_email})
ASIA: {subject}
KÄSITTELYMAKSU: 0,00 € (Hankintalaki 133 § / Hyvinvointialuelaki 140 § / Kuntalaki 135 §)

1. VAATIMUS HANKINTAPÄÄTÖSTEN OIKAISEMISEKSI JA SOPIMUSTEN KILPAILUTTAMISEKSI
Vaadimme hankintalain (1397/2016) 133 §:n nojalla, että hankintayksikkö ({flow.buyer_name}) oikaisee välittömästi toimittajalta {flow.inhouse_vendor} (Y-tunnus {flow.inhouse_y_tunnus}) tehdyt suorahankintapäätökset ({flow.annual_spend_m_eur:.2f} milj. EUR/v), irtisanoo lainvastaiset puitesopimukset ja kilpailuttaa palvelut avoimella menettelyllä.

2. PERUSTELUT JA VIRKAVASTUUN SELVITTÄMINEN (MAO:154/2024 & KHO 8.10.2025)
{reason_line} Välikätenä toimiva {flow.inhouse_vendor} perii {flow.inhouse_markup_pct:.0f} % sisäisen katteen ja ohjaa tilaukset edelleen toimittajille ({flow.subcontractor_vendor}).

Pyydämme tarkastuslautakuntaa ja tilintarkastajaa selvittämään, täyttääkö suorahankintojen jatkaminen MAO:154/2024- ja KHO 8.10.2025 (taltio 2250) -ratkaisujen jälkeen virkavelvollisuuden rikkomisen (RL 40:9–10 §) sekä vahingonkorvausvastuun edellytykset.
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
    forcing a municipality or Wellbeing County to release machine-readable purchase invoices within 14 days.
    """
    subject = f"TIETOPYYNTÖ (Julkisuuslaki 621/1999 13 § ja 16 §): {entity_name} — ostolaskuaineisto ja sidosyksikkösopimukset ({year})"
    body = f"""VASTAANOTTAJA: {entity_name} — Kirjaamo ({kirjaamo_email})
ASIA: {subject}

Pyydän viranomaisten toiminnan julkisuudesta annetun lain (621/1999, "julkisuuslaki") 9 §:n, 13 §:n ja 16 §:n 3 momentin nojalla toimittamaan sähköisesti koneluettavassa muodossa (CSV- tai XLSX-taulukko) seuraavat julkiset asiakirjat:

1. Viranomaisen ({entity_name}) kaikki maksetut ostolaskut (ostolaskudata) ajalta 1.1.{year - 1}–tähän päivään, sisältäen sarakkeet:
   - Toimittajan virallinen nimi ja Y-tunnus
   - Laskun päivämäärä, tositenumero ja euromäärä (alv 0 %)
   - Tiliöinti (tililuokka / tehtäväluokka / kustannuspaikka / CPV-koodi)
   - Tieto siitä, perustuuko hankinta avoimeen kilpailutukseen (Hilma-ilmoitusnumero), suorahankintaan vai sidosyksikköhankintaan.

2. Kaikki voimassa olevat sidosyksikköjen (mm. Istekki Oy, 2M-IT Oy, Numera Palvelut Oy / Sarastia, Monetra Oy, Tiera Oy, Oy Apotti Ab) osakassopimukset, omistusosuudet (% osakekannasta ja äänivallasta) sekä palvelusopimusten hinnastoliitteet.

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
    Generates a Pre-Award Discriminatory Spec Challenge (Hankintalaki § 3, § 67, § 71, § 75, § 85 & § 133)
    forcing the buyer to open a rigged 1-bid tender to qualified SMEs.
    """
    expected_saving_eur = round(tender.contract_value_eur * (0.25 if (tender.bids_received <= 1 or tender.is_direct_award) else 0.16), 2)
    subject = (
        f"VAATIMUS SYRJIVIEN VAATIMUSTEN POISTAMISEKSI (Hankintalaki 67 §, 75 § & 133 §): "
        f"Hilma {tender.tender_id} — {tender.buyer_name} ({tender.cpv_code})"
    )
    body = f"""VASTAANOTTAJA: {tender.buyer_name} — Hankintatoimi & Kirjaamo ({buyer_email})
ASIA: {subject}

1. KILPAILUA RAJOITTAVAN HANKINTAILMOITUKSEN / SUORAHANKINNAN OIKAISUVAATIMUS
Viitaten hankintaan {tender.tender_id} (CPV-luokka {tender.cpv_code}, ennakoitu arvo {tender.contract_value_eur:,.0f} EUR, saadut tarjoukset: {tender.bids_received} kpl), huomautamme, että markkinoilla toimii vähintään {tender.qualified_eu_sme_pool_size} täysin kelpoisuusehdot täyttävää suomalaista ja EU-alueen pk-toimittajaa.

Hankintalain (1397/2016) 3 §:n, 67 §:n, 71 §:n ja 85 §:n mukaan hankinnan teknisiä eritelmiä ja soveltuvuusvaatimuksia (kuten liikevaihto- ja referenssivaatimuksia) ei saa laatia suhteettomiksi tai siten, että ne keinotekoisesti rajoittavat kilpailua ja suosivat yhtä vakiintunutta toimittajaa. Yhden tai kahden tarjouksen kilpailutus tässä kokoluokassa aiheuttaa veronmaksajille arviolta {expected_saving_eur:,.0f} EUR vuotuisen ylihinnan.

2. VAATIMUKSET HANKINTAYKSIKÖLLE
Vaadimme hankintalain 3 §:n, 67 §:n, 75 §:n (hankinnan jakaminen osiin), 85 §:n ja 133 §:n nojalla, että {tender.buyer_name}:
1) Poistaa tarjouspyynnöstä kilpailua rajoittavat, tietylle toimittajalle räätälöidyt viite-, liikevaihto- ja rajapintavaatimukset;
2) Jakaa hankinnan hankintalain 75 §:n mukaisesti osakokonaisuuksiin pk-yritysten osallistumisen mahdollistamiseksi;
3) Jatkaa tarjousaikaa vähintään 14 vuorokaudella korjatun hankintailmoituksen julkaisemisesta.
"""
    return {
        "recipient_email": buyer_email,
        "subject": subject,
        "body": body.strip(),
        "filing_fee_eur": "0.00",
    }
