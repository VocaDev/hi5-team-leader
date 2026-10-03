# Demo — skenari FINAL (~2:30, live, pa slajd)

**Rrjedha kryesore (e fiksuar, s'ndryshohet):**
request → conflict detected → plan → MIRATO → all ACCEPT → Check-in → one KAM PROBLEM → agent replans → optional progress → owner report

S'MUNDEM dhe manager override mbeten të disponueshme, por **nuk janë pjesë e rrjedhës kryesore 2:30**.

Biznesi: Magic Events (shembull). Emrat e punëtorëve janë të shpikur.

## Kush është kush (FINAL, 16:30, zëvendëson propozimin)
| Roli | Kush | Pajisja | Emri te sistemi |
|---|---|---|---|
| **Lideri / Manageri** | **Genti** | laptopi (paneli në projektor) + Telegram (merr planin me MIRATO dhe njoftimet) | `leader` |
| **Klienti** (vetëm rreshti 1, me zë) | Flutura | — | — |
| Punëtori 1 (progresi: 🚗 / ✅) | Erza | telefoni | **Leart** (`w_leart`) |
| Punëtori 2 | Flutura | telefoni | **Arta** (`w_arta`) |
| Punëtori 3 (shtyp **⚠️ KAM PROBLEM**) | Tringa | telefoni | **Erioni** (`w_erioni`) |
| Punëtori 4 (i vjen detyra pas problemit) | Devlete | telefoni | **Naim** (`w_naim`) |

## Rrjedha
| # | Hapi | Kush | Çka thotë / bën | Çka duhet të shihet |
|---|---|---|---|---|
| 1 | **Request** | Klienti (Flutura) → Lideri (Genti) | "A mund ta bëjmë një ditëlindje të shtunën në 16:00 në Mitrovicë me bounce dhe maskotë?" | — |
| 2 | **Request te agjenti** | Lideri (Genti) | Shkruan te paneli: "Ditëlindje të shtunën në 16:00 në Mitrovicë, bounce + maskotë. A mundemi?" → Dërgo | "Agjenti po mendon…" |
| 3 | **Conflict detected** | Agjenti | Kontrollon njerëzit, aftësitë, vanët, pajisjet, punët ekzistuese, udhëtimin; e kap konfliktin | Feed-i live + shiriti i kuq (blocked) me arsyen |
| 4 | **Plan** | Agjenti | Krijon planin që e shmang konfliktin | Plani, detyrat sipas personit |
| 5 | **MIRATO** | Lideri (Genti) | E kontrollon planin dhe shtyp **MIRATO** | Statusi: dërguar |
| 6 | **All ACCEPT** | Punëtorët 1–4 | 4 detyra në telefon; secili shtyp **ACCEPT** | Ekrani gjelbërohet, puna konfirmuar |
| 7 | **Check-in** | Lideri (Genti) | Shtyp **⏰ Check-in**; telefonat marrin "A je gati?" | Detyrat tregojnë "⏰ check-in" |
| 8 | **Një KAM PROBLEM** | Punëtori 3 | Shtyp **⚠️ KAM PROBLEM** (të tjerët 👍 GATI) | Feed: problemi |
| 9 | **Agent replans** | Agjenti | E rillogarit planin dhe propozon zëvendësimin pa prishur punët tjera | Detyra kalon te tjetri, lideri njoftohet |
| 10 | **Progress (opsional, ~20 s)** | Punëtori 1 | **🚗 E NISA**, pastaj **✅ PËRFUNDOVA** | Progresi në ekran |
| 11 | **Owner report** | Liderja → Agjenti | "Më jep raportin për pronarin." | Raporti: puna, kush u caktua, kush pranoi, problemi, si u zgjidh, a përfundoi |

Nëse koha mbaron, hapi 10 anashkalohet; rrjedha mbyllet te hapi 11.

## Të disponueshme, jo në rrjedhën kryesore
- **S'MUNDEM** te një detyrë `sent` → detyra kalon te personi tjetër.
- **Manager override** ("vendose X gjithsesi") → BLOCKED me arsyen.
- Përdoren vetëm për Q&A ose nëse e kërkon juria.

## Para se të fillojmë
- [ ] Serveri ndezur (`python -m src.server`), `.env` me çelësin, bot-i Telegram aktiv
- [ ] Hotspot nga telefoni (jo Wi-Fi i sallës)
- [ ] Telefonat kanë dërguar `/start` te bot-i dhe janë te `TELEGRAM_IDENTITY_MAP` (Genti)
- [ ] **Reset** i shtypur, fusha e punës bosh
- [ ] Ekrani te `localhost:8000`, zoom 125%
- [ ] Video rezervë e hapur në një tab tjetër

## Nëse diçka dështon
- Telegram s'e merr një telefon: Erza e shtyp ACCEPT nga paneli i telefonave në ekran.
- Agjenti vonon > 30 s: Liderja vazhdon të flasë; mos e shtyp Dërgo dy herë.
- Gjithçka bie: video rezervë.