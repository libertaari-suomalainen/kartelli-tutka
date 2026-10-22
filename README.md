# Suomen Talousinstituutti (STI) — Julkisten Hankintojen (38,7 mrd. €/v) Rakenteellinen Tehokkuusanalyysi (`kartelli-tutka`)

### 🌐 **[AVAA LIVE-SOVELLUS SELAIMESSA: https://libertaari-suomalainen.github.io/kartelli-tutka/](https://libertaari-suomalainen.github.io/kartelli-tutka/)**

* **Live-verkkosivu (GitHub Pages):** [https://libertaari-suomalainen.github.io/kartelli-tutka/](https://libertaari-suomalainen.github.io/kartelli-tutka/)
* **Valmis 5-välilehtinen Excel-työkirja (`.xlsx`):** [`dist/Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx`](https://github.com/libertaari-suomalainen/kartelli-tutka/raw/main/dist/Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx)
* **Sisartyökalu (STEA-järjestöavustusten ja Business Finland / TEM yritystukien läpivalaisu):** [`tukipalkkio-purku`](https://github.com/libertaari-suomalainen/tukipalkkio-purku) ([Live-sovellus](https://libertaari-suomalainen.github.io/tukipalkkio-purku/))
* **Lisenssi:** MIT (100 % vapaa avoin lähdekoodi, nolla ulkoista Python-riippuvuutta)

---

## 1. Aineiston Kattavuus & Keskeiset Tulokset (100 % Virallisiin Primaarilähteisiin Perustuva Data)

Suomen valtio, **kaikki 21 hyvinvointialuetta**, **HUS-yhtymä** ja **308 kuntaa** käyttävät **38,70 miljardia euroa vuodessa** ulkoisiin ostoihin (`Tilastokeskus S.13: P.2 + D.632`). Tässä tutkimusjulkaisussa on mallinnettu suoraan **832,63 miljoonan euron vuotuinen tehostamispotentiaali** (ja koko 38,7 mrd. € kansalliseen hankintakantaan suhteutettuna **1,1–2,2 miljardia euroa vuodessa**) kolmesta julkisen hankintajärjestelmän rakenteellisesta tekijästä:

1. **15 Sidosyksikköä ja Palvelukeskusta (`1 963,40 milj. €/v` tilinpäätösliikevaihto 2024–2025, `230,99 milj. €/v` kilpailupotentiaali — *Hankintalaki 15 §, MAO:154/2024, MAO:500/2024 & KHO 8.10.2025 taltio 2250*):**
   * Kattaa 15 keskeistä julkista ICT-, laboratorio-, logistiikka- ja tukipalveluyksikköä virallisten tilinpäätöstietojen (2024–2025) mukaisesti (`Istekki Oy` 264,6 M€, `2M-IT Oy` 199,6 M€, `Fimlab Laboratoriot Oy` 173,5 M€, `Oy Apotti Ab` 147,7 M€, `Numera Palvelut Oy / Sarastia` 115,6 M€, `Monetra-konserni` 114,7 M€, `Tuomi Logistiikka Oy` 112,0 M€, `ISLAB hyvinvointiyhtymä` 96,0 M€, `Tiera Oy` 76,0 M€, `Kaarea Oy` 68,2 M€, `Meita Oy` 58,5 M€, `Polkka Oy` 39,4 M€, `Sansia Oy` 18,4 M€, `Kuntien Hetapalvelut Oy` 14,2 M€ sekä `Valtori` 465,0 M€).
   * *Huomautus:* Kaupalliset puitesopimus- ja alihankintatoimittajat toimivat laillisesti; tarkastelu kohdistuu julkisen sektorin sidosyksikköomistuksen rakenteeseen (`Hankintalaki 15 §` ja `HE 2/2026 vp` 10 % vähimmäisomistusraja) sekä KKV/VATT-tutkimuksiin pohjautuvaan avoimen kilpailutuksen tehokkuuspotentiaaliin (`11–14 %`).
2. **Alueellinen yksikkökustannusvertailu (`582,71 milj. €/v` säästöpotentiaali — `P25-vertailutaso`):**
   * 31 alueellista yksikkökustannusvertailua 5 keskeisessä sote- ja ICT-hankintakategoriassa (`THL`, `Sotkanet`, `HALI ry` ja `KKV` julkaistujen yksikkökustannusvertailujen pohjalta, esim. ympärivuorokautisen hoivan ostopalvelun viitetaso vs. kalleimpien alueiden kokonaiskustannustaso).
3. **Markkinaoikeuden (`MAO`) ja Korkeimman hallinto-oikeuden (`KHO`) vahvistetut julkisten hankintojen ratkaisut (`10` Finlex/KKV-ratkaisua 2023–2025, `18,93 milj. €/v` säästöpotentiaali):**
   * Sisältää 10 vahvistettua oikeustapausta: `MAO:154/2024 & KHO 8.10.2025 (T2250)`, `MAO:500/2024`, `MAO:611/2025`, `MAO:537/2025`, `MAO:202/2025`, `MAO:748/2025`, `MAO:665/2025`, `MAO:553/2025`, `MAO:223/2023` ja `MAO:70/2023`.
4. **Kaikki 43 Suurinta Julkista Ostajaa (`21` hyvinvointialuetta + `HUS` + `21` suurinta kaupunkia):**
   * Jokaiselle 43 viranomaiselle Modulo-11-tarkistettu Y-tunnus, virallinen kirjaamo-sähköposti, ulkoisten ostojen volyymi ja valmis `0,00 €` Julkisuuslain (`621/1999 13 § & 16.3 §`) tietopyyntö.

---

## 2. Tuotanto-ominaisuudet Selainsovelluksessa ja Excelissä

* **Interaktiivinen hallintoasiakirjojen räätälöinti (`.txt` & PDF-tulostus):** Käyttäjä voi täyttää oman nimensä ja organisaationsa suoraan modaalissa, ladata valmiin `.txt`-asiakirjan, tulostaa sen PDF:ksi tai avata suoraan sähköpostissa (`0,00 €` käsittelymaksu).
* **Kaksisuuntainen sarakelajittelu (`▲`/`▼`) & välitön CSV-vienti (`UTF-8 BOM`):** Sekä 15 sidosyksikön taulukko että kaikkien 43 julkisen ostajan taulukko ovat lajiteltavissa ja vietävissä `.csv`-muotoon.
* **Suorat URL-syvälinkit (`#inhouse-<y_tunnus>`, `#buyer-<y_tunnus>`, `#tender-<idx>`, `#arb-<idx>`):** Jokaisen kortin ja modaalin voi jakaa suoralla linkillä.

---

## 3. Kääntäminen ja Testaus (0 Ulkoista Riippuvuutta)

```bash
# Käännä kaikki artefaktit (SSOT JSON + 5-välilehtinen .xlsx + staattinen index.html):
PYTHONPATH=src python3 -B -m kartelli_tutka.build_all

# Aja yksikkötestit:
PYTHONPATH=src python3 -B -m unittest discover -v -s tests
```
