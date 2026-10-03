# BRIEF — prezantimi: 3 slajde + demo live = 5 minuta (Tringa)

> Burimet: intervista me **Magic Events** (`docs/interview/notes.md`), `PLAN.md`, numrat finalë nga `evidence/`.
> **Rregulli i jurisë:** *"Score what you saw working."* Slajdet e mbështesin demon. Demoja është ylli.

## Rrjedha dhe koha

| Koha | Çka | Kush flet |
|---|---|---|
| 0:00–0:50 | **SLAJDI 1: Problemi** | Flutura |
| 0:50–3:20 | **DEMO LIVE** (pa slajd: ekrani + telefonat) | Genti, ekipi luan rolet |
| 3:20–4:10 | **SLAJDI 2: Si punon dhe pse e përdor** | Genti |
| 4:10–4:50 | **SLAJDI 3: Çdo industri + hapi tjetër** | Tringa |
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

## SLAJDI 3: Çdo industri + hapi tjetër (0:40 + mbyllja)

**Titulli:** *I njëjti Team Leader, rregulla të tjera*

**Tabela me 4 rreshta:**
| Industria | Çka kontrollon kodi |
|---|---|
| Evente (sot) | njerëz, van, pajisje, rruga |
| Elektrikë / servis | licenca, pajisjet në van, urgjenca |
| Spitale | certifikimi, pushimi mes turneve |
| IT, si Genpact | SLA, aftësitë, 4-eyes (kush e bën s'e miraton) |

**Rreshti nën tabelë:** *Platforma të mëdha ekzistojnë për kompanitë e mëdha. Ne jemi team leader-i në chat-in që e keni, në shqip, i gatshëm brenda një dite.*

**Hapi tjetër (kutia në fund):** *Pilot me Magic Events, 4 të shtuna: matim kohën e koordinimit dhe gabimet.*

**Mbyllja (Tringa, 10s):** *"Lideri juaj mban klientin. Ne e kthejmë 'po'-në në një plan që s'prish asgjë."*

---

## Rregulla
- **Numrat:** nga intervista ose nga `evidence/`. **[X] sekonda** e plotëson Devlete pas run-it të 16:00 (testi i parë: ~17 s). Pa shuma parash.
- **Pa fjalë:** revolucionar, seamless, powerful, empower, cutting-edge, game-changer.
- **Stili:** dark navy, i njëjtë me ekranin e Erzës; tekst i madh, pak fjalë. Asnjë slajd me më shumë se ~40 fjalë (përveç tabelave).
- **NDA:** asnjë gjë nga puna e askujt në ekip.

## Afatet
Drafti **15:30** → Gentit · numri [X] **16:15** · finali **17:00** (PDF + PPT) · provë me kronometër **17:30** (5:00 saktë).
