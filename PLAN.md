# PLAN — AI Team Leader (Team Hi5)

> Genpact × Agilyti AI Hackathon · Prishtinë · e shtunë 3 tetor 2026 · track **AI Agent for Business**
> **Ideja finale (3 tetor ~14:00): AI Agent si Team Leader dhe shpërndarës detyrash.** ShiftRescue është hequr plotësisht.
> Dokumentet e vjetra janë te `docs/archive/` vetëm si histori. **Ky skedar është burimi i vetëm i së vërtetës.**
> ✅ = i verifikuar · ⬜ = për t'u bërë · ❓ = ende i panjohur. Pa hamendje.

---

## 1. Ideja

**Njeriu flet me klientin. AI Team Leader e kthen marrëveshjen në një plan pa gabime dhe ia jep çdo punëtori detyrën e vet, në detaje.**

1. **Lideri njerëzor** flet me klientin (telefon, takim, DM). Marrëdhënia me klientin mbetet njerëzore.
2. Ia shkruan punën **AI Team Leader-it** me tekst të lirë: *"Ditëlindje, 25 fëmijë, e shtunë 16:00, Mitrovicë, bounce + maskotë."*
3. AI Team Leader-i:
   - **e kupton** dhe pyet vetëm atë që mungon;
   - **e kontrollon** kapacitetin me kod: stafin, automjetet, pajisjet, udhëtimin, montimin, punët e tjera të ditës;
   - **e ndan** punën në detyra dhe zgjedh kush e bën secilën;
   - ia tregon planin liderit për **miratim**;
   - u dërgon **4 punëtorëve detyrat në detaje** në Telegram (çka, ku, kur, çka marrin me vete, me kë punojnë, kontakti), dhe secili shtyp **ACCEPT**.
4. Kur dikush shtyp **S'MUNDEM**, ia jep detyrën personit tjetër të përshtatshëm dhe e njofton liderin.

**Parimi:** *AI-ja kupton, planifikon dhe shkruan. Kodi i kontrollon rregullat. Njeriu miraton.* Asnjë rregull s'jeton në prompt, dhe asnjë urdhër s'e anashkalon.

**Pse "më i saktë se njeriu":** njeriu harron që vani është i zënë te eventi tjetër, ose që ekipi s'arrin në kohë pas montimit. Kodi i kontrollon **të gjitha kufizimet, çdo herë**, dhe çdo vendim e shpjegon me numra.

**Përdoruesi i vërtetë:** biznesi i eventeve i Flutures (✅ leja nga të dy pronarët).

---

## 2. Demo (live, me tekst të lirë, pa përgjigje të gatshme)

| Kush | Roli |
|---|---|
| 1 person | **Lideri njerëzor**: flet me "klientin", pastaj i shkruan AI Team Leader-it |
| 4 persona | **Punëtorët**: marrin detyrat në Telegram, shtypin ACCEPT |
| Ekrani | **Paneli i liderit**: puna, plani, kush çka bën, statuset live |

**Rrjedha (~2 min):**
1. Lideri e merr kërkesën nga klienti dhe ia shkruan agjentit me fjalët e veta.
2. Ekrani tregon si mendon agjenti: kapaciteti → detyrat → kush dhe pse ("pse jo Dritoni: 16:00 + 40 min = 16:40 > 16:30").
3. Lideri e miraton planin me një buton.
4. 4 telefona marrin detyrat në detaje dhe shtypin ACCEPT. Ekrani gjelbërohet.
5. *(nëse ka kohë)* një punëtor shtyp S'MUNDEM → agjenti ia jep detyrën tjetrit dhe e njofton liderin.
6. *(kurthi)* lideri: "vendose X gjithsesi" → **BLOCKED** me arsyen.

**E përgatitur:** bota (kompania, njerëzit, pajisjet, orari). **Live:** çdo mesazh, çdo vendim, çdo detyrë, çdo ACCEPT. Skenarin e demos e shkruan ekipi.

Shembull i një detyre në Telegram (formati, jo teksti final):
```
📋 Detyra jote — e shtunë 4 tetor
Eventi: Ditëlindje (25 fëmijë), Mitrovicë, rr. ..., nis 16:00
Roli: Montimi i bounce-it
Mbërritja: 15:00 (montimi 45 min)
Merr me vete: Bounce #2, kompresori, 4 kunja
Shkon me: Erioni (shofer, Van 1, niset 14:20 nga depoja)
Pas eventit: çmontimi 18:00–18:30, kthimi në depo
Kontakti i klientit: te lideri
[ACCEPT]  [S'MUNDEM]
```

---

## 3. Kriteret e jurisë (✅) dhe si i plotësojmë

| % | Kriteri | Si e plotësojmë |
|---|---|---|
| 25 | **Working demo** | Rrjedha e §2, live: lideri → agjenti → 4 telefona → ACCEPT → ekrani i gjelbër. Plan B: butonat në ekran + video rezervë (16:00). |
| 20 | **Problem proof** | Biznesi i Flutures me emër. Citate fjalë për fjalë: sa zgjat nga "po" e klientit deri te ekipi i informuar, sa shpesh harrohet ose ngatërrohet diçka. |
| 20 | **Technical depth** | **Vendimi:** AI kupton dhe shkruan, kodi kontrollon rregullat, njeriu miraton. Modeli s'mund të caktojë njeri pa kaluar motorin. **Plus stack-u (§7).** |
| 15 | **Completeness** | Pitch-ojmë vetëm atë që punon. Slajdi "What runs today". Korporata, spitalet dhe elektrikët shkruhen "next". |
| 10 | **Differentiation** | §5: platformat e mëdha ekzistojnë. Ne jemi në chat, në shqip, pa projekt implementimi, me rregulla që s'thyhen dhe vendime që shpjegohen. **Kurrë "askush s'e bën".** |
| 10 | **Next step** | Pilot me biznesin e Flutures, 4 të shtuna. Matim minutat nga "po" e klientit deri te ekipi i konfirmuar, dhe gabimet (diçka e harruar, konflikt). ❓ pronarët ende po mendojnë → *"we've asked them for a pilot"*. |

---

## 4. Pse do ta blente dikush (Demand)

**Problemi që përsëritet:** çdo punë e re duhet kthyer në plan dhe çdo person duhet informuar. Sot kjo bëhet me telefonata, Viber dhe kokën e liderit. Gabimet (vani i zënë, pajisja e harruar, ekipi që s'arrin) kushtojnë një klient.

| Pse e blen | Si e masim |
|---|---|
| **Saktësia:** asnjë konflikt, asnjë gjë e harruar, sepse kodi i kontrollon të gjitha kufizimet | gabimet para/pas në pilot |
| **Shpejtësia:** nga "po" e klientit te ekipi i konfirmuar për 1–2 minuta, jo me një orë telefonatash | minutat, nga `evidence/` + intervista |
| **Rritja pa koordinator të ri:** një lider menaxhon më shumë punë | punët në javë për një lider |
| **Dija s'rri në një kokë:** kur lideri mungon, rregullat dhe plani janë në sistem | — |
| **Kur dikush refuzon:** detyra kalon te personi tjetër i përshtatshëm brenda sekondave | koha deri te ACCEPT |

**Tregu (✅):** kompanitë paguajnë tashmë për këtë: ServiceTitan (elektrikë dhe zanate), QGenda (spitale), ServiceNow dhe Atlassian (IT). Kjo dëshmon kërkesën. Por këto janë platforma të mëdha, në anglisht, të shtrenjta, me implementim të gjatë. **Bizneset e vogla dhe të mesme në rajon s'kanë asgjë dhe punojnë me Viber.**

**Paraja:** asnjë numër i shpikur si fakt. Nëse përdoret shembull, shkruhet **"Shembull, me supozime"** dhe supozimet duken hapur. Numrat e vërtetë vijnë nga pronarët e Flutures.

**Përgjigjja për "kemi tashmë team leader / plan / bench":**
> *"Your team leader keeps the client. We take the part where they turn a yes into a plan for ten people at once, and that's where mistakes happen. The agent checks every constraint every time, and your leader just approves."*

---

## 5. Shkallëzimi: industritë, konkurrentët, si dallojmë

Bërthama njeh vetëm **Punën → Detyrat → Aftësitë → Rregullat → Prioritetin**. Industria është paketë konfigurimi (`industries/<emri>/`).

| Industria | Puna | Rregullat që kontrollon kodi | Kush e bën sot (✅ ekzistojnë) | Si dallojmë |
|---|---|---|---|---|
| **Evente** (demo) | eventi i klientit | staf + van + pajisje, udhëtimi, montimi, punët e tjera të ditës | DM, Viber, Excel; mjetet e qirasë (❓ s'janë kontrolluar në detaje) | në chat, në shqip, kontrollon disa burime njëherësh |
| **Kompani elektrike / zanate** | intervenim, instalim | licenca/certifikata e elektricistit, pajisjet në van, udhëtimi, urgjenca para planifikimit | **ServiceTitan** ("agentic OS for the trades"), **Simpro** | punën e merr nga biseda; për firmat e vogla që s'i përballojnë platformat e mëdha |
| **Spitale** | turne, mbulimi i repartit | certifikimi, raporti infermier/pacient, pushimi mes turneve, pa turne nate rresht | **QGenda**, **symplr**, **UKG** | rregullat shpjegohen me numra; shtresë mbi sistemin ekzistues. ❓ spitalet publike në Kosovë |
| **IT / shërbime si Genpact** | rasti, tiketa, kërkesa e klientit | **SLA-ja**, aftësitë/gjuha, ngarkesa maksimale, **4-eyes** (kush e bën s'e miraton), qasja në të dhënat e klientit | **ServiceNow** (Advanced Work Assignment + AI agents), **Atlassian JSM** (intelligent routing) | për ekipet pa ServiceNow; puna nga biseda me klientin → detyra në detaje; rregullat s'thyhen as me urdhër |

**E ndershme për Q&A:** te korporatat s'e mundim ServiceNow-in dhe s'e themi. Hyrja jonë janë bizneset e vogla dhe të mesme në rajon, që sot s'kanë asgjë. Korporata është vizioni: *"Same Team Leader, different rulebook."*
**NDA:** shembujt korporativë janë IT, sigurimet dhe kujdesi ndaj klientit. Kurrë fatura, prokurim, financa ose karburant.

---

## 6. Arkitektura (e re)

```
Lideri (Telegram/konsola) ──► AI TEAM LEADER (Claude)
                                 │  1. intake: teksti → punë e strukturuar (strict tool)
                                 │  2. check_capacity ──► MOTORI (kod): burimet, koha, udhëtimi, rregullat R1–R6
                                 │  3. build_plan ──────► MOTORI: detyrat nga shablloni i punës + kush i bën
                                 │  4. propose → Lideri [MIRATO]
                                 │  5. write_briefings: një mesazh i detajuar për secilin (LLM)
                                 ▼
                     Runtime ──► 4 punëtorët në Telegram [ACCEPT] [S'MUNDEM]
                                 │  ACCEPT → ri-validim → rezervim → ekrani
                                 │  S'MUNDEM → detyra te personi tjetër → Lideri
```
- **LLM-i:** kupton kërkesën, pyet çka mungon, zgjedh planin nga ato që i jep motori, shkruan detyrat dhe shpjegimet.
- **Kodi:** kapaciteti, rregullat, caktimi, rezervimi, verifikimi. **Modeli s'ka mjet për rezervim.**
- **Shabllonet e punës** (`industries/events/jobs.json`): p.sh. "ditëlindje me bounce" = ngarkimi → udhëtimi → montimi 45 min → eventi → çmontimi 30 min, me rolet dhe pajisjet.

## 7. Stack-u (pjesë e Technical depth)

| Shtresa | Zgjedhja | Pse |
|---|---|---|
| Gjuha | **Python 3.11+**, UI me **HTML/CSS/JS vanilla** | SDK-ja zyrtare e Claude-it; motori dhe agjenti në një gjuhë; UI pa build, offline |
| Modeli | **Claude `claude-opus-5-5`** (SDK `anthropic`) | shqip/gegërisht, arsyetim me shumë hapa, adaptive thinking |
| Mjetet | `strict: true` + `additionalProperties: false` | modeli s'mund të shpikë argumente; identiteti vjen nga kanali |
| Motori | **Python deterministik**: kapaciteti, rregullat R1–R6, udhëtimi, kërkimi i caktimeve | rregullat e garantuara dhe të shpjeguara me numra; milisekonda |
| Serveri | **FastAPI + Uvicorn**, një proces, një lock | Telegram, UI dhe konsola bashkë, pa gara në gjendje |
| Kanali | **Telegram Bot API** (inline keyboard, callback_query) | falas, butona ACCEPT; Viber, WhatsApp, Slack, Teams = përshtatës më vonë |
| Gjendja | JSON me shkrim atomik + `events.jsonl` | çdo hap ruhet si provë; DB te piloti |
| Testet | **pytest** për motorin + skenarë e2e | rezultatet e pritura shkruhen me dorë para kodit |

---

## 8. Çka ndërtojmë sot dhe çka jo

**Po:** lideri → agjenti → kapaciteti → plani → miratimi → 4 detyra në Telegram → ACCEPT → ekrani · kurthi (BLOCKED) · *(nëse ka kohë)* S'MUNDEM → detyra te tjetri.
**Slajd, jo kod:** korporata/IT, spitalet, elektrikët, raporti javor, kanalet e tjera.
**Jo:** pagesa, fatura, GPS, login, databazë, çmime nga puna e askujt.

## 9. Ndarja e punës

**Te [`TASKS.md`](TASKS.md):** kush çka bën, skedarët, teknologjia, afatet dhe kontratat JSON.

## 10. Orari (i shtunë)

| Ora | Çka |
|---|---|
| 14:00 | ndarja e punës + kontratat (`company.json`, `jobs.json`, formati i ekranit) |
| **14:45 G1** | lideri shkruan → agjenti → plani në ekran (pa Telegram) |
| **15:30 G2** | 4 detyra në Telegram → ACCEPT → ekrani i gjelbër |
| **16:00** | **FEATURE FREEZE.** Run-i final → `evidence/`, video rezervë |
| 16:00–17:30 | prezantimi, provat |
| **17:50** | **DORËZIMI** |

## 11. Rregullat e ekipit

1. Tregojmë vetëm atë që punon.
2. Çdo numër vjen nga `evidence/` ose nga pronarët. Përgjigjet e agjentit s'redaktohen me dorë.
3. **Bota është e simuluar, workflow-i është real.**
4. `.env`, çelësat dhe token-at kurrë në GitHub dhe kurrë në chat.
5. Branch `<emri>/<tema>` → PR te `main`.

## 12. ❓ Të hapura

| Çka | Kush |
|---|---|
| Pronarët: sa zgjat nga "po" e klientit te ekipi i informuar? Sa shpesh harrohet/ngatërrohet diçka? | Flutura, **tani** |
| A pranojnë pilotin? | Flutura |
| Emri i produktit (punues: "AI Team Leader") | Genti |
| Username-i GitHub i Tringës | Tringa |
| Çka dorëzohet saktësisht, gjuha e pitch-it, repo publike? | organizatorët |
