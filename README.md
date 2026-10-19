# Kartelli-Purkaja (`kartelli-tutka`) — Julkisten Hankintojen (38,7 Mrd €/v) Röntgen & 1-Click Oikeusohjus

### 🌐 **[AVAA LIVE-SOVELLUS SELAIMESSA: https://libertaari-suomalainen.github.io/kartelli-tutka/](https://libertaari-suomalainen.github.io/kartelli-tutka/)**

* **Live-verkkosivu (GitHub Pages):** [https://libertaari-suomalainen.github.io/kartelli-tutka/](https://libertaari-suomalainen.github.io/kartelli-tutka/)
* **Valmis CFO / VM Excel-leikkuri (`.xlsx`):** [`dist/Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx`](https://github.com/libertaari-suomalainen/kartelli-tutka/raw/main/dist/Sote_ja_Kunta_Kartelli_Matriisi_2026.xlsx)
* **Sisartyökalu (Yritys- ja järjestötukien 11,5 Mrd €/v leikkuri):** [`tukipalkkio-purku`](https://github.com/libertaari-suomalainen/tukipalkkio-purku) ([Live-sovellus](https://libertaari-suomalainen.github.io/tukipalkkio-purku/))
* **Tekijä / Ylläpitäjä:** [`@libertaari-suomalainen`](https://github.com/libertaari-suomalainen) | **Lisenssi:** MIT (100 % vapaa avoin lähdekoodi)

---

## 1. Miksi tämä työkalu on olemassa?

Suomen valtio, 21 hyvinvointialuetta ja 308 kuntaa käyttävät **38,7 miljardia euroa vuodessa** ulkoisiin ostoihin (`Tilastokeskus S.13: P.2 + D.632`). Vähintään **1,5–3,5 miljardia euroa vuodessa** valuu hukkaan kolmen rakenteellisen kartellimekanismin vuoksi:

1. **Laittomat sidosyksikkösuorahankinnat (*Hankintalaki 15 § & MAO:154/2024*):**
   Hyvinvointialueet ja kunnat ostavat `0,04 % – 1,2 %` nimellisen "kuoriosakkeen" yhtiöistä (`Istekki Oy`, `2M-IT Oy`, `Numera Palvelut Oy / Sarastia`, `Monetra Oy`, `Tiera Oy`, `Oy Apotti Ab`) ja ohjaavat niille yli **1,4 miljardia euroa vuodessa** ilman kilpailutusta. Välikädet perivät **21–30 % sisäisen katteen** ja ketjuttavat työn suoraan yksityisille suuryrityksille (`Tietoevry`, `CGI`, `Atea`, `Accountor`).
2. **Alueiden välinen 2–3x yksikköhintojen ylihinta (`P25-Arbitraasi`):**
   Sama vuokralääkäritunti, työasema-IT-tuki, potilastietojärjestelmälisenssi tai hoivavuorokausi maksaa yhdellä hyvinvointialueella 50–300 % enemmän kuin parhaan neljänneksen (`P25`) vertailualueella.
3. **Hilman 1 tarjouksen näennäiskilpailutukset:**
   45 % julkisista kilpailutuksista saa vain 1–2 tarjousta, koska soveltuvuus- ja referenssivaatimukset on räätälöity nykyiselle toimittajalle.

---

## 2. Mitä `kartelli-tutka` tekee? (0 € Käsittelymaksu)

Markkinaoikeuden valitusmaksu (`2 120 € – 6 350 €`) estää tavallista pk-yrittäjää valittamasta. Tämä työkalu generoi suoraan selaimessa **neljä maksutonta (`0,00 €`) viranomaisasiakirjaa**:

1. **KKV Toimenpidepyyntö (*Hankintalaki 139 § & MAO:154/2024*):** Valmis valvontailmoitus Kilpailu- ja kuluttajavirastolle (`kirjaamo@kkv.fi`), joka velvoittaa KKV:n tutkimaan alle 10 % omistusosuudella tehdyt laittomat sidosyksikkösuorahankinnat ja vaatimaan sopimusten tehottomuutta valtion varoin.
2. **Hankintaoikaisuvaatimus & Virkavastuu-ilmoitus (*Hankintalaki 133 § & RL 40:9–10 §*):** Valmis vaatimus hyvinvointialueen tai kunnan hallitukselle ja tarkastuslautakunnalle.
3. **Pakottava Ostolaskudatan Tietopyyntö (*Julkisuuslaki 621/1999 13 § & 16.3 §*):** Pakottaa ostolaskujaan piilottelevan hyvinvointialueen tai kunnan luovuttamaan koneluettavan CSV/XLSX-ostolaskuaineiston ja sidosyksikköjen osakassopimukset 14 vuorokaudessa.
4. **Syrjivien Tarjousvaatimusten Poistovaatimus (*Hankintalaki 67 § & 73 §*):** Avaa yhden tarjouksen Hilma-kilpailutukset pk-yrityksille.

---

## 3. Käyttö & Kääntäminen Lähdekoodista (0 Riippuvuutta)

Projekti toimii pelkällä Python 3.10+ standardikirjastolla (ei ulkoisia `pip`-riippuvuuksia):

```bash
# Käännä kaikki artefaktit (SSOT JSON + 4-välilehden .xlsx + staattinen index.html):
PYTHONPATH=src python3 -B -m kartelli_tutka.build_all

# Aja yksikkötestit:
PYTHONPATH=src python3 -B -m unittest discover -v -s tests
```
