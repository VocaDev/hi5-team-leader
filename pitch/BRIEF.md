# BRIEF — prezantimi (Tringa)

> Burimet: intervista me **Magic Events** (`docs/interview/notes.md`, PR #2), `PLAN.md`, run-et në `evidence/`.
> Kohëzgjatja ❓ (pyet organizatorët). Plani më poshtë është për **~5 min**: ~2 min demo, ~3 min slajde.
> **Rregulli i artë i jurisë:** *"Score what you saw working."* Çdo slajd mbështet demon, s'e zëvendëson.

## Slajdet

| # | Slajdi | Përmbajtja | Kush flet | Koha |
|---|---|---|---|---|
| 1 | **Titulli** | **AI Team Leader** · Team Hi5 · *"Your leader keeps the client. The agent turns the yes into a plan."* | Tringa | 10s |
| 2 | **Problemi (përdoruesi real)** | **Magic Events** (Rinor & Elmonda Hyseni, ✅ leje). *"A confirmed event is not a calendar entry."* Pas "po"-së së klientit: njerëz + aftësi + van + pajisje + kohë + vend. Sot me WhatsApp, Viber, telefonata. **3 fakte nga intervista** (poshtë). | Flutura | 45s |
| 3 | → **DEMO LIVE** ← | (asnjë slajd: ekrani + telefonat) | Genti + ekipi | 2:00 |
| 4 | **Si punon** | Diagrami: **Lideri → Agjenti (kupton, planifikon, shkruan) → Kodi (rregullat) → Lideri MIRATON → Ekipi ACCEPT**. Fjalia: *"AI proposes, code decides, a human approves."* Stack-u në një rresht: Python · Claude Opus 5.5 · motor deterministik · FastAPI · Telegram | Genti | 40s |
| 5 | **Pse e përdor** | **Sot** vs **me agjentin** (numrat poshtë) + *"Çka s'bën: s'flet me klientin, s'miraton vetë, s'cakton askënd pa ACCEPT."* | Devlete | 30s |
| 6 | **Çdo industri** | Tabela: Evente · Elektrikë · Spitale · IT si Genpact. Te secila: **çka kontrollon kodi** (PLAN.md §5). *"Same Team Leader, different rulebook."* Implementimi: të dhënat → rregullat → kanali → 2 javë shadow mode → live | Devlete / Tringa | 30s |
| 7 | **Pse ne + hapi tjetër** | *"Big platforms exist for big companies (ServiceTitan, QGenda, ServiceNow). We're the team leader in the chat you already use, in Albanian, live in a day."* **Next step:** pilot me Magic Events, 4 të shtuna, matim kohën e koordinimit + gabimet. | Tringa | 25s |

## Faktet nga intervista (fjalë për fjalë, pa i zmadhuar)

1. **Koordinimi mund të zgjasë orë:** *"Në një rast të vështirë, koordinimi i plotë mori afërsisht 4 orë."* Thuaje si **rast i vështirë real, jo mesatare**.
2. **Një rregullim prish një event tjetër:** *"Për të zgjidhur një problem te një ekip u përdor një person i planifikuar për ekipin tjetër. Eventi tjetër u vonua rreth një orë."* Ndikoi te klienti, te serioziteti dhe te çmimi final. **Ky është fakti më i fortë**, sepse demoja e kap pikërisht këtë.
3. **Ndryshimet në minutën e fundit:** rregulli është 4 orë paralajmërim, por *"ka raste kur njoftimi vjen vetëm rreth 30 minuta para nisjes."*

**Rregullat e pronarëve = rregullat e kodit:** siguria nuk komprometohet · aftësia e duhur · askush (as vani, as pajisja) në dy vende njëherësh · koha e udhëtimit · premtimet ndaj klientit s'ndryshohen pa miratimin e tij.

## Numrat: 3 lloje, mos i përziej

| Lloji | Numri | Si shkruhet |
|---|---|---|
| **Nga pronarët** | 3–4 orë (rast i vështirë) · vonesë 1 orë · 30 min paralajmërim | "Magic Events" |
| **I matur nga ne** | plani në **~17 s** · kostoja **~$0.05** për plan ❓ | **vetëm numrat finalë nga `evidence/` (Devlete, 16:00)** |
| **Shembull** | çdo shumë parash | **"Shembull, me supozime"** + supozimet në slajd |

## Si mos të tingëllojë si AI slop

- Nis me momentin: *"E shtunë. Klienti thotë 'po'. Tani 4 veta duhet ta dinë çka bëjnë, me cilin van, në cilën orë."*
- Çdo pretendim pasohet nga ekrani (demoja).
- **Fjalë të ndaluara:** revolucionar, seamless, powerful, empower, cutting-edge, game-changer, "AI-powered solution".
- Thuaj kufijtë: çka s'bën agjenti, dhe që bota e demos është e simuluar ndërsa workflow-i është real.
- **NDA:** asnjë sistem, numër ose shembull nga puna e askujt në ekip.

## Afatet

Drafti **15:30** (dërgoja Gentit) · numrat finalë nga `evidence/` në **16:15** · finali **17:00** (PDF) · provë me kronometër **17:30**.
Puna në branch `tringa/pitch` → PR. Mjeti: Google Slides / PowerPoint / Canva, sipas zgjedhjes. Stili: dark navy, i njëjtë me ekranin e Erzës.
