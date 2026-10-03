# BRIEF — prezantimi: 3 slajde + demo live = 5 minuta (Tringa)

> Burimet: intervista me **Magic Events** (`docs/interview/notes.md`), `PLAN.md`, numrat finalë nga `evidence/`.
> **Rregulli i jurisë:** *"Score what you saw working."* Slajdet e mbështesin demon. Demoja është ylli.

## Rrjedha dhe koha

| Koha | Çka | Kush flet |
|---|---|---|
| 0:00–0:50 | **SLAJDI 1: Problemi** | Flutura |
| 0:50–3:20 | **DEMO LIVE** (pa slajd: ekrani + telefonat) | Genti, ekipi luan rolet |
| 3:20–4:10 | **SLAJDI 2: Si punon dhe pse e përdor** | Genti |
| 4:10–4:50 | **SLAJDI 3: Sot ekipet e vogla, nesër korporatat (next step)** | Tringa |
| 4:50–5:00 | Mbyllja: një fjali, mbi slajdin 3 | Tringa |

---

## SLAJDI 1: Problemi (0:50)

**Titulli:** *Një "po" nga klienti = 10 gjëra që duhet të dalin mirë*

**Majtas, përdoruesi real:**
- **Magic Events**: Rinor & Elmonda Hyseni (✅ leje)
- Pas çdo eventi të konfirmuar: **njerëz + aftësi + van + pajisje + orë + vend**
- Sot: WhatsApp, Viber, telefonata, një nga një

**Djathtas, 3 fakte nga intervista** (kuti të mëdha, fjalë për fjalë):
1. **~4 orë** koordinim në një rast të vështirë
2. **1 orë vonesë** te një event, sepse personi u mor për të rregulluar një ekip tjetër
3. Anulimi vjen ndonjëherë **30 min** para nisjes

**Fjalia e Flutures në fund:** *"Pyetja s'është 'a kemi dikë të lirë?' Është 'a mund ta kryejë kompania këtë punë pa prishur diçka tjetër?'"*

---

## DEMO LIVE (2:30): s'ka slajd
Ekrani i Erzës në projektor, 4 telefona në duar. Skenarin e shkruan ekipi (`demo/README.md`). Genti flet. Tringa s'flet këtu.

---

## SLAJDI 2: Si punon dhe pse e përdor (0:50)

**Titulli:** *AI planifikon. Kodi kontrollon. Njeriu miraton.*

> **Figura e gatshme: `pitch/architecture.png`** (3200×1800, dark navy). Vendose në gjysmën e sipërme ose në gjithë slajdin; titulli dhe stack-u janë brenda figurës. `architecture.svg` = versioni që s'humbet cilësi.

**Lart, diagram me 5 kuti dhe shigjeta:**
`Lideri (flet me klientin)` → `Agjenti AI (kupton, planifikon, shkruan detyrat)` → `Kodi (rregullat: aftësia, rruga, orari, vani, pajisjet)` → `Lideri: MIRATO` → `Ekipi: ACCEPT në Telegram`

**Poshtë majtas, "Sot → Me agjentin":**
| Sot | Me agjentin |
|---|---|
| deri në ~4 orë telefonata (rast i vështirë) | plani në **[X] sekonda** ← numri nga `evidence/` |
| konflikti zbulohet kur është vonë | konflikti kapet para se të ndodhë |
| njëri nga një | 4 veta njëherësh, me detaje |

**Poshtë djathtas, "Çka s'bën":** s'flet me klientin · s'miraton vetë · s'cakton askënd pa ACCEPT · rregullat s'i anashkalon askush

**Shiriti i fundit (i vogël):** Python · Claude Opus 5.5 · motor deterministik · FastAPI · Telegram

---

## SLAJDI 3: Hapi tjetër: nga ekipet e vogla te korporatat (0:40 + mbyllja)  ← VERSIONI FINAL (15:55)

**Titulli:** *Sot: ekipet e vogla. Nesër: asistenti i PM-it në korporata.*

**Majtas, "Sot (demo)": biznes i vogël pa PM**
- pronari shkruan punën → agjenti kontrollon njerëzit, vanin, pajisjet, rrugën
- secili merr detyrën: çka bën, ku, kur, **çka merr me vete** → ACCEPT
- gjatë punës: **check-in** ("A je gati?"), **🚗 e nisa / ✅ përfundova**
- raporti për pronarin: orët, rreziku për orë shtesë, problemet

**Djathtas, "Next: korporata me PM"** (diagram me shigjeta):
`Product Manager` → `PM i shkruan agjentit çka ndërtohet` → `Agjenti e ndan te Team Lead-ët dhe zhvilluesit` → `ndjek progresin live, kontrollon rregullat (4-eyes, aftësitë, ngarkesa), raporton te secili rol`
- Raporti sipas rolit: Product Manager (premtimi ndaj klientit) · PM (afati, rreziqet) · Team Lead (pengesat, review) · zhvilluesi (detyrat e veta)
- Shtresë mbi Jira / ServiceNow, jo mjet i ri

**Rreshti poshtë (korrigjuar sipas research-it të Devletes, 16:23):** *"Connecteam, Microsoft Planner, Asana and Jira already help teams, some with AI agents. What we show is the full handoff in one flow: client request → AI plan → rules checked in code → human approval → workers act in their chat → follow-through when something changes."*
- **"Pa thyer asnjë rregull" = parim i arkitekturës** (e tregon kurthi BLOCKED në demo), **jo pretendim** që të tjerët s'e bëjnë.
- **Kurrë mos thoni** "existing tools give apps, we give an agent": Planner, Asana dhe Rovo kanë agjentë.

**Kutia e fundit, hapi tjetër konkret:** *Pilot me Magic Events (4 të shtuna): matim kohën e koordinimit dhe gabimet.*

**Mbyllja (Tringa, 10s):** *"Lideri juaj mban klientin. Ne e kthejmë 'po'-në në një plan që s'prish asgjë dhe e ndjekim deri në fund."*

---

## Rregulla
- **Numrat:** nga intervista ose nga `evidence/`. **[X] sekonda** e plotëson Devlete pas run-it të 16:00 (testi i parë: ~17 s). Pa shuma parash.
- **Pa fjalë:** revolucionar, seamless, powerful, empower, cutting-edge, game-changer.
- **Stili:** dark navy, i njëjtë me ekranin e Erzës; tekst i madh, pak fjalë. Asnjë slajd me më shumë se ~40 fjalë (përveç tabelave).
- **NDA:** asnjë gjë nga puna e askujt në ekip.

## Afatet
Drafti **15:30** → Gentit · numri [X] **16:15** · finali **17:00** (PDF + PPT) · provë me kronometër **17:30** (5:00 saktë).
