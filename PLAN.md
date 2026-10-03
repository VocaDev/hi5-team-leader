# PLAN — ShiftRescue (Team Hi5)

> Genpact × Agilyti AI Hackathon · Icon Tower, Prishtinë · e shtunë 3 tetor 2026 · track **AI Agent for Business**
> **Kjo repo është burimi i së vërtetës.** Detajet teknike: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). Repo e vjetër (`hi5-inbox-agent/weekend/`) mbetet vetëm si histori.
> ✅ = i verifikuar · ⬜ = për t'u bërë · ❓ = ende i panjohur. Pa hamendje.

---

## 1. Ideja

**"One person goes missing. Your operation doesn't have to."**

Kur dikush mungon papritur, menaxheri sot fillon telefonatat dhe shpesh e zgjidh një problem duke krijuar tjetrin. ShiftRescue nuk pyet vetëm *"kush është i lirë?"*, por **"nëse e lëviz këtë person, çka prishet më pas?"** Gjen ndryshimin më të vogël të sigurt, ia ofron punën zëvendësuesit në Telegram, e rezervon vetëm pas **ACCEPT** dhe verifikon që eventet kritike janë mbuluar prapë. Kur s'ka zgjidhje të sigurt, **eskalon te pronari me opsione**, s'improvizon.

**Parimi:** *AI-ja kupton dhe flet. Kodi vendos.* Rregullat e forta s'jetojnë në prompt, dhe asnjë urdhër, as i menaxherit, s'i anashkalon.

**Përdoruesi i vërtetë:** biznesi i eventeve i Flutures. ✅ Të dy pronarët kanë dhënë leje që ta përmendim.

---

## 2. Kriteret e jurisë (✅ slajdi i organizatorëve) dhe si i plotësojmë

| % | Kriteri | Çka kërkojnë | Si e plotësojmë | Pronari |
|---|---|---|---|---|
| 25 | **Working demo** | Run it live. Show input, show output. | Telefon i vërtetë me tekst të lirë ("sot s'vij") → zinxhiri skuqet → oferta → ACCEPT → 100% e gjelbër. Pastaj **kurthi** (menaxheri "vendose gjithsesi" → BLOCKED) dhe **eskalimi** (s'ka njerëz → karta me opsione). Rreth gjysma e kohës. Plan B: butonat në ekran + video rezervë (16:00). | Genti · Erza · Tringa |
| 20 | **Problem proof** | Name a real user who has this problem today. | Biznesi i Flutures **me emër** (✅ leja). 1–2 citate fjalë për fjalë: sa shpesh mungon dikush, sa zgjat rregullimi, çka prishet. | Flutura |
| 20 | **Technical depth** | Explain one real decision under the hood. | **Vendimi:** *"AI kupton, kodi vendos."* Modeli zgjedh vetëm `plan_id` nga motori, rezervimi bëhet vetëm pas ACCEPT + ri-validimit, urdhri i menaxherit kalon nëpër të njëjtat rregulla. **Plus stack-u (§5):** gjuha, teknologjitë, mjetet dhe pse u zgjodh secila. Feed-i live e tregon. | Genti |
| 15 | **Completeness** | What you pitched vs. what actually runs. | Pitch-ojmë vetëm atë që punon. Slajdi "What runs today" = skenat e demos. Pjesa tjetër shënohet "next". Numrat nga `evidence/`. Feature freeze 16:00. | Tringa · Devlete |
| 10 | **Differentiation** | Why not just use an existing tool? | "Deputy/Skedulo e mbushin turnin. Ne shohim çka prishet pas lëvizjes, rregullat s'thyhen as me urdhër, eskalimi e njeh klientin, verifikojmë rikthimin. Në shqip, në Telegram." **Kurrë "askush s'e bën".** | Devlete |
| 10 | **Next step** | One concrete next milestone. | **Pilot në shadow mode me biznesin e Flutures, 4 të shtunat e ardhshme.** Matim minutat nga "s'vij" te "u mbulua" + sa herë rregullimi me dorë prishi një event tjetër. ❓ pronarët ende po mendojnë për pilotin → deri atëherë: *"we've asked them for a pilot"*. | Tringa |

Barazimi zgjidhet me **working demo**, pastaj me **problem proof**, prandaj këto dyja janë prioriteti.

---

## 3. Eskalimi: kur s'ka njerëz (pyetja e mentorit)

Agjenti **s'shpik njerëz dhe s'thyen rregulla**. Mbron eventet më të rëndësishme, i tregon pronarit saktë çka prishet, dhe i jep **2–3 opsione me pasoja**, një buton për secilin. Pa shtypje s'ndodh asgjë. Ekrani s'thotë kurrë 100% kur s'është.

| # | Opsioni | Si e llogarit motori | Kush miraton | Sot? |
|---|---|---|---|---|
| 1 | **Ekip i lirë për një dritare kohe** ("ekipi X është i lirë 30 min, arrin te klienti Y dhe kthehet") | ora kur mbaron ekipi + `travel_min` te klienti tjetër → dritarja e lirë | **Pronari** e konfirmon me mesazh/buton | ✅ |
| 2 | **Shtyrje me klientin** | `can_delay_min` i eventit + fleksibiliteti | Pronari. Agjenti e shkruan mesazhin, **pronari e dërgon**; agjenti s'i shkruan kurrë klientit vetë | ✅ |
| 3 | **Ulja e shërbimit** (p.sh. pa maskotë te C) | slot-et jo kritike të eventit | Pronari | ✅ |
| 4 | Orë shtesë me pëlqim brenda kufirit | orët javore të punonjësit | Punonjësi (ACCEPT) | ⛔ slajd |

### Prioriteti i klientëve (i vendos pronari, jo AI-ja)
Kur s'mbulohet gjithçka, renditja është **(criticality i eventit, pastaj client score)**. ❓ Flutura e konfirmon me pronarët a duhet të jetë kjo renditje apo shumë.

| Fusha te klienti | Vlera | Efekti |
|---|---|---|
| `value_tier` | `high` / `normal` (klient që paguan më shumë; **pa shuma në €**) | +1 |
| `prepaid` | `true` / `false` (ka paguar paraprakisht) | +1 |
| `first_time` | `true` / `false` (klient i ri, përshtypja e parë) | +1 |

Peshat jetojnë në `industries/events/priority.json`, prandaj pronari i ndryshon pa kod.

### Fleksibiliteti (llogaritet, s'shkruhet me dorë)
- **Kur mbaron secili ekip** → nga orari (`roster` + `to` i slot-it të fundit).
- **Sa shpejt arrin te klienti tjetër** → `travel_min` ndërmjet zonave (❓ vlera të supozuara, shënohen si të tilla).
Nga këto të dyja motori nxjerr **dritaret e lira**, që ushqejnë opsionin 1.

---

## 4. Shkallëzimi: si përshtatet për çdo industri

**Bërthama s'e di çka është "event".** Ajo njeh vetëm 5 koncepte; industria është paketë konfigurimi.

| Koncepti i bërthamës | Events (sot) | Firmë sigurie | Kujdes në shtëpi | Restorant / retail | Servis në terren |
|---|---|---|---|---|---|
| **Job** | eventi | posti | vizita | turni | intervenimi |
| **Slot** (roli + dritarja) | shofer, montim, maskotë | roja 06–18 | kujdestare 09–10 | kuzhinë, arkë | teknik |
| **Needs** (aftësi/certifikata) | patentë, bounce | licencë sigurie | certifikatë kujdesi | higjienë ushqimi | certifikatë elektrike |
| **Hard rules** | pa mbivendosje + udhëtim, orë maksimale | 12 orë pushim pas turnit, posti s'mbetet bosh | vazhdimësia e kujdestares | orët javore, rregullat e të miturve | udhëtimi, certifikata |
| **Priority** | criticality + klienti (vlera, parapagim, i ri) | rëndësia e postit | nevoja e pacientit | orët e pikut | niveli i SLA-së |
| **Escalation** | ekip i lirë, shtyrje, ulje e shërbimit | zgjatje me pëlqim, mbikëqyrësi | shtyrje e vizitës jo urgjente | mbyllje e një seksioni | ri-planifikim me klientin |

**Paketa e një industrie** (`industries/<emri>/`):
| Skedari | Çka mban |
|---|---|
| `pack.json` | fjalori (job = "event"), rolet dhe aftësitë, nivelet e criticality, opsionet e lejuara të eskalimit |
| `rules.json` | cilat rregulla të forta janë aktive + parametrat (pushimi, orët maksimale, udhëtimi) |
| `priority.json` | peshat për renditjen kur s'mbulohet gjithçka |
| `company.json` | bota e demos (njerëz, evente, orar), **vetëm e shpikur** |
| `prompt.md` | fjalët e domenit dhe dialekti për modelin |

**Niveli korporativ** (`industries/corporate/`, vetëm slajd sot): turni i fundit (12 orë pushim), specializimi, orët javore + kufiri i orëve shtesë, drejtësia (s'thirret gjithmonë i njëjti).

**E ndershme për Q&A:** industri e re = **vetëm konfigurim**, kur rregullat e saj përdorin llojet ekzistuese. Lloj i ri rregulli = **një funksion i vogël Python + test**. *"Change the rules, not the code"* vlen për shumicën, jo për të gjitha.

**Implementimi në një kompani të vërtetë:** (1) të dhënat nga Excel/Sheets që përdorin sot → (2) rregullat dhe prioritetet i vendos pronari → (3) secili punonjës e shtyp `/start` në Telegram, me pëlqim → (4) **2 javë shadow mode** (agjenti propozon, menaxheri vendos) → (5) live me oferta.

---

## 5. Stack-u teknik (pjesë e Technical depth)

| Shtresa | Zgjedhja | Pse |
|---|---|---|
| Gjuha | **Python 3.11+** (backend) · **HTML/CSS/JS vanilla** (UI) | e njëjta gjuhë si skeleti i shtatorit; UI pa build, punon offline |
| Modeli | **Claude `claude-opus-5-5`** përmes SDK-së zyrtare `anthropic` | arsyetim i fortë në shqip/gegërisht; adaptive thinking; `effort` i vendosur me dorë |
| Tool use | mjete me **`strict: true`** + `additionalProperties: false`; `submit_decision` i fundit | modeli s'mund të dërgojë argumente të shpikura; identiteti injektohet nga runtime |
| Prompt caching | `cache_control` në nivelin e lartë; gjendja **s'hyn** në prompt | prompt-i statik mbetet i cache-uar, gjendja vjen nga `get_snapshot` |
| Motori | **Python i pastër, deterministik**: graf varësish, rregulla R1–R6, kërkim brute-force (deri në 2 lëvizje), objektiv leksikografik | për ~10 njerëz × ~10 slot-e mjaftojnë mikrosekonda; s'ka nevojë për OR-Tools; çdo refuzim vjen me aritmetikë ("16:00 + 40 min = 16:40 > 16:30") |
| Serveri | **FastAPI + Uvicorn**, një proces, `ThreadPoolExecutor(4)` + një `STATE_LOCK` | Telegram, UI dhe konsola në të njëjtin proces; s'ka gara në gjendje |
| Kanali | **Telegram Bot API** (long polling, inline keyboard, `callback_query`, `answerCallbackQuery`, `editMessageText`) përmes `requests` | falas, i menjëhershëm, butona ACCEPT/DECLINE; WhatsApp Business kërkon verifikim |
| Gjendja | **JSON** me shkrim atomik (temp + `os.replace`) + **`events.jsonl`** (trace) | mjafton për demo; çdo hap ruhet si provë; DB vjen në pilot |
| Konfigurimi | `python-dotenv`, `.env` (kurrë në git) | çelësat s'dalin kurrë jashtë |
| Testet | **pytest** për motorin (T1–T6, pa LLM, falas) + `run_scenarios.py` për e2e me LLM (T7–T9) + `check_outputs.py` | rezultatet e pritura i shkruan Flutura **para kodit** |
| Mjetet e punës | Git + GitHub (PR, `main` i mbrojtur), Claude Code për ndërtim | çdo ndryshim kalon nga review |

---

## 6. Çka ndërtojmë sot dhe çka jo

**Po:** mungesë → pasojat → plani → ofertë në Telegram → ACCEPT → rezervim → verifikim → "100% restored" · kurthi (BLOCKED) · eskalimi me opsionet 1–3 · prioriteti i klientëve · paketa `industries/events/`.
**Slajd, jo kod:** orë shtesë, niveli korporativ, industritë e tjera, pilot.
**Jo:** payroll, rekrutim, GPS/rrugë reale, login, databazë, **asnjë shumë parash**.
**NDA:** asgjë nga puna e Gentit (sisteme, numra, karburant, furnitorë). Të dhënat janë vetëm të shpikura.

---

## 7. Ndarja

| Kush | Çka | Ku në repo | Zëvendës |
|---|---|---|---|
| **Genti** (+ Claude) | motori, agjenti, Telegram, serveri | `src/` | Flutura |
| **Flutura** | `company.json`, `rules.json`, `priority.json`, rezultatet e pritura T1–T9 (me dorë, para kodit), intervista | `industries/events/`, `tests/expected.md`, `docs/interview/` | Devlete |
| **Erza** | ekrani i menaxhmentit: health %, eventet, zinxhiri, feed-i live, karta e eskalimit, konsola | `ui/` | Tringa |
| **Devlete** | ekzekutimi i testeve, `evidence/`, numrat nga JSON, konkurrentët për Q&A | `evidence/`, `scripts/` | Genti |
| **Tringa** | prezantimi, teksti, provat; slajdet "What runs today", "Scale", "Next step" | `pitch/` | Erza |
| **Erza + Tringa** | skenari i demos (e shkruani ju), telefonat, video rezervë, hotspot | `demo/` | Flutura |

Një pronar për një skedë. Pas 16:00 s'shtohet asgjë.

---

## 8. Ora për orë (e shtunë)

| Ora | Çka |
|---|---|
| **12:00 G1** | mesazh nga konsola → agjenti → zinxhiri skuqet në ekran |
| **13:00 G2** | vendosim çka presim |
| **14:00 G3** | rast i plotë me telefon: ofertë → ACCEPT → verifikim → ekrani gjelbërohet |
| 14:00–16:00 | kurthi, eskalimi, prioriteti i klientëve, lustrim |
| 15:30 | mentor #2 |
| **16:00** | **FEATURE FREEZE.** Run-i final → `evidence/`, video rezervë |
| 16:00–17:30 | prezantimi, Q&A |
| 17:30 | provë e plotë me kronometër |
| **17:50** | **DORËZIMI** (jo 17:59) |

Prerja nëse jemi vonë (hiqet e para → e fundit): drejtësia · broadcast · afati i ofertës · disa mungesa në një mesazh · "vetëm prej 15:00" · `what_if`. **Kurrë s'priten:** rregullat në kod, shpjegimi pse jo i pari që duket i lirë, pëlqimi, verifikimi, refuzimi i urdhrit të menaxherit, eskalimi.

---

## 9. Rregullat e ekipit

1. Tregojmë vetëm atë që punon.
2. Çdo numër në prezantim vjen nga `evidence/`. Përgjigjet e agjentit s'redaktohen me dorë.
3. **Bota është e simuluar, workflow-i është real.** S'pretendojmë që incidenti i demos ka ndodhur.
4. `.env`, çelësat dhe token-at kurrë në GitHub dhe kurrë në chat.
5. Punohet në branch `<emri>/<tema>`, pastaj PR te `main`.
6. Shuma parash nuk ka. Orët shtesë maten në orë.

---

## 10. ❓ Të hapura

| Çka | Kush | Kur |
|---|---|---|
| A pranojnë pronarët pilotin? (✅ leja për emrin është dhënë) | Flutura | para 16:00 |
| Renditja: criticality pastaj klienti, apo shumë? | Flutura me pronarët | para G2 |
| Çka përdorin sot për orarin (Excel / Sheets / letër)? | Flutura | sot |
| Username-i GitHub i Tringës (ftesa) | Tringa | tani |
| Çka dorëzohet saktësisht · gjuha e pitch-it · pronësia e kodit · repo publike? | organizatorët | sot |
