# Suomen Talousinstituutti (STI) — Julkisten Hankintojen (38,7 mrd. €/v) Tutkimusraportti 2026 (`kartelli-tutka`)

### 🌐 **[AVAA LIVE-SOVELLUS SELAIMESSA: https://libertaari-suomalainen.github.io/kartelli-tutka/](https://libertaari-suomalainen.github.io/kartelli-tutka/)**

* **Live-verkkosivu (GitHub Pages):** [https://libertaari-suomalainen.github.io/kartelli-tutka/](https://libertaari-suomalainen.github.io/kartelli-tutka/)
* **Valmis 5-välilehtinen CFO / VM Excel-leikkuri (`.xlsx`):** [`dist/Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx`](https://github.com/libertaari-suomalainen/kartelli-tutka/raw/main/dist/Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx)
* **Sisartyökalu (Yritys- ja järjestötukien 11,5 mrd. €/v läpivalaisu):** [`tukipalkkio-purku`](https://github.com/libertaari-suomalainen/tukipalkkio-purku) ([Live-sovellus](https://libertaari-suomalainen.github.io/tukipalkkio-purku/))
* **Lisenssi:** MIT (100 % vapaa avoin lähdekoodi, nolla ulkoista Python-riippuvuutta)

---

## 1. Aineiston Kattavuus & Keskeiset Tulokset (100 % Oikea Viranomaisdata)

Suomen valtio, **kaikki 21 hyvinvointialuetta**, **HUS-yhtymä** ja **308 kuntaa** käyttävät **38,70 miljardia euroa vuodessa** ulkoisiin ostoihin (`Tilastokeskus S.13: P.2 + D.632`). Tässä tutkimusjulkaisussa on mallinnettu suoraan **1,43 miljardin euron vuotuinen säästö** (ja koko 38,7 mrd. € kansalliseen hankintakantaan skaalattuna **3,03–3,50 miljardia euroa vuodessa**) kolmesta rakenteellisesta kilpailuvääristymästä:

1. **15 Sidosyksikköjättiä (`1,98 mrd. €/v` suorahankinnat, `700,0 milj. €/v` vuosisäästö — *Hankintalaki 15 §, MAO:154/2024 & KHO 8.10.2025 taltio 2250*):**
   * Kattaa kaikki 15 keskeistä julkista IT-, laboratorio-, logistiikka- ja talousvälikättä (`Istekki Oy`, `Oy Apotti Ab`, `2M-IT Oy`, `Numera Palvelut Oy / Sarastia`, `Monetra Oy`, `Tiera Oy`, `Valtori`, `Fimlab Laboratoriot Oy`, `ISLAB hyvinvointiyhtymä`, `Tuomi Logistiikka Oy`, `Meita Oy`, `Kaarea Oy`, `Polkka Oy`, `Sansia Oy`, `Kuntien Hetapalvelut Oy`).
   * Pelkästään 7 suurimmassa IT- ja talousvälikädessä vuotuinen ylihinta ja ketjutuskustannus on **`532,38 milj. €/v`**, ja kaikissa 15 sidosyksikössä **`699,95 milj. €/v`**.
2. **Alueiden välinen 2–3x yksikköhintojen ylihinta (`711,23 milj. €/v` vuosisäästö — `P25-Arbitraasi`):**
   * 31 alueellista yksikköhintavertailua 5 suurimmassa sote- ja IT-hankintakategoriassa (`Vuokralääkärit 85121000`, `IT-työasemat 72260000`, `Potilastietojärjestelmät APTJ 48814000`, `Ympärivuorokautinen hoiva 85311100`, `Sote- ja koulukuljetukset 60130000`).
3. **Markkinaoikeuden (`MAO`) & Hilman 1–2 tarjouksen kilpailutukset ja suorahankinnat (`10` dokumentoitua tapausta):**
   * Sisältää oikeat markkinaoikeustapaukset (`MAO:154/2024`, `MAO:292/2023`, `MAO:70/2024`, `MAO:412/2023`, `MAO:112/2024`, `MAO:38/2024`, `MAO:534/2023`, `MAO:201/2024`, `MAO:485/2024`, `MAO:618/2024`).
4. **Kaikki 43 Suurinta Julkista Ostajaa (`21` hyvinvointialuetta + `HUS` + `21` suurinta kaupunkia):**
   * Jokaiselle 43 viranomaiselle Modulo-11-tarkistettu Y-tunnus, virallinen kirjaamo-sähköposti, ulkoisten ostojen volyymi ja valmis `0,00 €` Julkisuuslain (`621/1999 13 § & 16.3 §`) tietopyyntö.

---

## 2. Tuotanto-ominaisuudet Selainsovelluksessa ja Excelissä

* **Interaktiivinen viranomaisasiakirjojen räätälöinti (`.txt` & PDF-tulostus):** Käyttäjä voi täyttää oman nimensä ja yrityksensä/Y-tunnuksensa suoraan modaalissa, ladata valmiin `.txt`-asiakirjan, tulostaa sen PDF:ksi tai avata suoraan sähköpostissa (`0,00 €` käsittelymaksu).
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
