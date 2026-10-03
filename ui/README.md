# Demo — skenari (~2:30, live, pa slajd)

Një rrjedhë e vetme: **request → plan → approve → accept → problem → recovery → completion → report**

Biznesi: Magic Events (shembull). Emrat e punëtorëve janë të shpikur.

## Kush është kush (PROPOZIM, konfirmoje me ekipin)
| Roli | Kush | Çka mban | Emri te sistemi (`company.json`) |
|---|---|---|---|
| **Liderja** | Flutura | laptopi i demos (paneli) | — |
| **Klienti** | Devlete | zë, vetëm rreshti 1 | — |
| **Punëtori 1** (e nisa / përfundova) | Erza | telefoni 1 | ______ |
| **Punëtori 2** | Genti | telefoni 2 | ______ |
| **Punëtori 3** (raporton PROBLEM) | Tringa | telefoni 3 | ______ |
| **Punëtori 4** (Devlete pas rreshtit 1) | Devlete | telefoni 4 | ______ |
| **Ekrani** | Genti | projektori, `localhost:8000`, zoom 125% | — |

## Rrjedha
| # | Kush | Çka thotë / bën | Çka duhet të shihet |
|---|---|---|---|
| 1 | **Klienti → Liderja** | "A mund ta bëjmë një ditëlindje të shtunën në 16:00 në Mitrovicë me bounce dhe maskotë?" | — |
| 2 | **Liderja → Agjenti** | Shkruan te paneli: "Ditëlindje të shtunën në 16:00 në Mitrovicë, bounce + maskotë. A mundemi?" → Dërgo | "Agjenti po mendon…" |
| 3 | **Agjenti** | Analizon kërkesën: kontrollon njerëzit, aftësitë, vanët, pajisjet, punët ekzistuese dhe udhëtimin, pastaj krijon planin | Feed-i live, plani del |
| 4 | **Liderja** | E kontrollon planin dhe shtyp **MIRATO** | Statusi: dërguar |
| 5 | **Punëtorët 1–4** | 4 detyra në telefon; secili shtyp **ACCEPT** | Ekrani gjelbërohet |
| 6 | **Liderja + punëtori 3** | Liderja shtyp **⏰ Check-in**; telefonat marrin "A je gati?"; punëtori 3 shtyp **⚠️ PROBLEM** | Feed + shiriti i kuq |
| 7 | **Agjenti** | E rillogarit planin dhe propozon zëvendësimin pa prishur punët tjera; zëvendësuesi shtyp ACCEPT | Detyra kalon te tjetri |
| 8 | **Punëtori 1** | **🚗 E NISA**, pastaj **✅ PËRFUNDOVA** | Progresi në ekran |
| 9 | **Liderja → Agjenti** | "Më jep raportin për pronarin." | — |
| 10 | **Agjenti** | Raporti final: puna, kush u caktua, kush pranoi, çfarë problemi ndodhi, si u zgjidh, a përfundoi puna | Raporti në ekran |

## Para se të fillojmë
- [ ] Serveri ndezur, `.env` me çelësin, bot-i Telegram aktiv
- [ ] 4 telefonat kanë shtypur /start te bot-i; njoftimet ndezur
- [ ] Hotspot nga telefoni (jo Wi-Fi i sallës)
- [ ] Telefonat janë te `TELEGRAM_IDENTITY_MAP` (Genti)
- [ ] **Reset** i shtypur, fusha e punës bosh
- [ ] Ekrani te `localhost:8000`, zoom 125%
- [ ] Video rezervë e hapur në një tab tjetër

## Nëse diçka dështon
- Telegram s'e merr një telefon: Erza e shtyp ACCEPT / S'MUNDEM nga paneli i telefonave në ekran.
- Agjenti vonon > 30 s: Liderja vazhdon të flasë; mos e shtyp Dërgo dy herë.
- Gjithçka bie: video rezervë.