# demo — Erza + Tringa (skenarin e shkruani ju)

> Demoja është **live, me tekst të lirë**. Agjenti s'ka përgjigje të gatshme. E përgatitur është vetëm bota (kompania, njerëzit, punët e ditës).

## Kush është kush (FINAL, 17:00): telefona kanë vetëm Erza dhe Flutura
| Roli | Kush | Ku përgjigjet | Çka i ndodh në demo |
|---|---|---|---|
| **Lideri / Manageri** | **Genti** | laptopi (paneli) | shkruan punën, kurthi, MIRATO, Check-in; përgjigjet për Devleten dhe Tringën te "Telefonat (rezervë)" |
| Punëtorja | **Erza** | **📱 Telegram** | **Shofere + Van 1** → ACCEPT → te check-in **⚠️ KAM PROBLEM** |
| Punëtorja | **Flutura** | **📱 Telegram** | **Maskota + Kostumi Ariu** → ACCEPT → 👍 GATI → **🚗 E NISA / ✅ PËRFUNDOVA** |
| Punëtorja | Devlete | paneli | **Montimi + Çmontimi** → ACCEPT (në panel) |
| Punëtorja | Tringa | paneli | **pas problemit të Erzës i vjen shoferi** → ACCEPT (në panel) |
| (vetëm në ekran) | Dritoni, Blerta | — | të zënë në Vushtrri; kurthi me Dritonin → BLOCKED |

## Rrjedha (2:30, nga 0:50 deri 3:20 te prezantimi)
1. Lideri e shkruan punën me fjalët e veta (p.sh. ditëlindje, ora, vendi, shërbimet)
2. Ekrani: "si mendon agjenti", përfshirë konfliktin që e kap (dikush s'arrin në kohë / vani i zënë)
3. Plani → **MIRATO**
4. 4 telefona marrin detyrat në detaje → ACCEPT
5. Njëri shtyp **S'MUNDEM** → detyra kalon te tjetri, lideri njoftohet
6. *(opsional)* lideri: "vendose X gjithsesi" → **BLOCKED**

## Skena IT (me PM): ❌ JO NË DEMO (vendimi 15:55: korporata = next step në slajdin 3). Mbetet në kod për Q&A nëse pyesin.
1. Ndërruesi → **IT** (`it_services`)
2. PM-i: *"Klienti raportoi bug kritik në login, duhet në prodhim deri 18:00. A mundemi?"* → "PO" + plani
3. *"Le ta bëjë Drita edhe review-n e kodit të vet"* → **BLOCKED 4-eyes**
4. *(opsional)* *"Më jep raportin për Product Manager-in"*

## Check-in (te skena kryesore, pas ACCEPT)
Butoni ⏰ Check-in → telefonat marrin "A je gati?" → njëri shtyp **⚠️ KAM PROBLEM** → zëvendësim ose eskalim.

## Progresi live + raporti (opsional, 20 s)
Pas ACCEPT: punëtori shtyp **🚗 E NISA** / **✅ PËRFUNDOVA** → ekrani përditësohet. Lideri: *"Më jep raportin për pronarin"* → orët për person, rreziku i orëve shtesë, problemet.

## Skena 2: Ndërtim me PM (20–30 s, në fund, në vend të raportit nëse s'ka kohë)
1. Butoni **"Ndërtim · me PM"** lart
2. PM-i: *"Të shtunën betonimi i pllakës te objekti B në Ferizaj, nisim në 07:00. A mundemi?"* (thoni **"të shtunën"**, jo "nesër": plani është për 10 tetor)
3. Shihet: Fatmiri s'arrin nga objekti A (09:00 + 35 min) → Valoni · Pompa 1 e zënë → Pompa 2 · kontrolli i cilësisë te Teuta (4-eyes)
4. *(opsional)* *"Le ta bëjë Agroni edhe kontrollin e cilësisë"* → **BLOCKED 4-eyes**
5. Genti: *"Same agent, a construction company with a PM. Different rulebook, same guarantees."*

## Checklist para demos
- [ ] `POST /api/reset` (butoni Reset)
- [ ] 5 telefonat e kanë dërguar `/start` te bot-i dhe janë te `TELEGRAM_IDENTITY_MAP` (Genti)
- [ ] hotspot nga telefoni (jo Wi-Fi i sallës)
- [ ] video rezervë nga run-i i 16:00
- [ ] plan B: butonat ACCEPT / S'MUNDEM në ekran (pa Telegram)
