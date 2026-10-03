# TASKS — kush çka bën (e shtunë 3 tetor)

> Ideja dhe arsyet: [`PLAN.md`](PLAN.md). Ky skedar = **detyra e secilës, skedarët, teknologjia, afati.**
> Ora e nisjes: 14:05 · **FEATURE FREEZE 16:00** · **DORËZIMI 17:50**. Pas 16:00 s'shtohet asgjë.

> **✅ 14:20 — backend-i (Genti) është në `main` dhe punon.** Nisja: `python -m src.server` → http://localhost:8000. API-ja dhe hapat janë te `README.md`.
> Pa `industries/events/` përdoren të dhënat e zhvillimit te `src/dev_data/`. Flutura: kopjo formatin prej aty. Data duhet të jetë **e shtunë** (`"date": "2026-10-10"`).
> Erza: `GET /api/view` kthen edhe `job.summary`, `tasks[].note`, `existing_jobs`, `busy` (true = agjenti po mendon) përveç kontratës më poshtë. Butonat: MIRATO → `POST /api/approve {}`; telefonat e panelit → `POST /api/callback {job_id, task_id, action}`.

## ⏱️ Gjendja 15:50 + detyrat finale (deri 17:50)

**✅ Punon në `main`:** agjenti ("a mundemi?" → plani) · MIRATO · detyrat në detaje · ACCEPT / S'MUNDEM → zëvendësim · **check-in** (👍 / ⚠️) · **progresi live** (🚗 E NISA / ✅ PËRFUNDOVA) · **raporti** (orët për person, rreziku i orëve shtesë, vonesat, problemet) · **Evente pa PM / IT me PM** (4-eyes) · UI e Erzës e lidhur (`python -m src.server` → http://localhost:8000).

| Kush | Detyra finale | Afati |
|---|---|---|
| **Genti** | Bot-i në Telegram (BotFather → token te `.env` → 5 telefona `/start` → `TELEGRAM_IDENTITY_MAP`) · run-i final → `evidence/` · video rezervë | 16:15 |
| **Flutura** | PR #2 (intervista) → merge · citatet për slajdin 1 · roli në demo | 16:15 |
| **Erza** | Demo: skenari (e shkruani ju) + rolet + prova në laptopin e Gentit; vetëm ndryshime të vogla stili te `ui/` | 16:30 |
| **Devlete** | `scripts/numbers.py` → `evidence/numbers.md` (sekondat e planit, MIRATO → të gjithë ACCEPT, kostoja) · `docs/competitors.md` (Connecteam, Microsoft Planner agent, Asana, Rovo, ServiceTitan…) | 16:30 |
| **Tringa** | 3 slajde sipas `pitch/BRIEF.md` (slajdi 3 = dy kolona: pa PM / me PM) · numri [X] nga Devlete | drafti 16:30 · finali 17:00 |
| **Të gjithë** | 2 prova me kronometër (5:00) | 17:00–17:30 |
| **Genti** | **Dorëzimi** | **17:50** |

## Si punojmë

1. Secila punon **vetëm në folderin e vet**, në branch-in e vet: `flutura/data`, `erza/ui`, `devlete/tests`, `tringa/pitch`.
2. Kur mbaron një pjesë → **Pull Request te `main`** → Genti e shikon dhe e bën merge.
3. Ndryshim te një **kontratë** (`company.json`, `jobs.json`, `view.json`)? Pyete Gentin para se ta bësh.
4. AI për ndërtim lejohet. **Përgjigjet e agjentit dhe numrat s'shpiken dhe s'redaktohen me dorë.**
5. `.env`, çelësat dhe token-at kurrë në GitHub dhe kurrë në chat.

## Teknologjia

| Pjesa | Çka përdorim |
|---|---|
| Backend | Python 3.11, `anthropic` (Claude Opus 5.5), FastAPI + Uvicorn, `requests` (Telegram) |
| Të dhënat | JSON |
| Testet | pytest |
| Ekrani | HTML + CSS + JS vanilla, pa framework, pa CDN; `fetch` çdo 1 s |
| Prezantimi | Google Slides / PowerPoint / Canva, sipas zgjedhjes së Tringës → eksport PDF |

---

## 🧠 Genti (+ Claude): `src/`

- [ ] `src/engine/`: kapaciteti (punëtorët, vanët, pajisjet, udhëtimi, punët ekzistuese), rregullat, kush e merr secilën detyrë. **Kod, pa AI.**
- [ ] `src/agent/`: cikli i Claude-it; mjetet `parse_job`, `check_capacity`, `build_plan`, `propose_plan`, `write_briefings`
- [ ] `src/channels/telegram_bot.py`: detyrat me butonat **ACCEPT / S'MUNDEM**
- [ ] `src/server.py`: `GET /api/view`, `POST /api/message`, `POST /api/approve`, `POST /api/callback`, `POST /api/reset`
- ⏰ **14:45 G1:** lideri shkruan → plani del si JSON · **15:30 G2:** 4 detyra në Telegram → ACCEPT → ekrani

## 📦 Flutura: `industries/events/` + `tests/expected.md` + `docs/interview/`

- [ ] **`company.json`** (formati poshtë): punëtorët me emra **të shpikur** dhe aftësitë; 2 vanë; pajisjet (bounce, kompresori, kostumet e maskotës); 3 zona; `travel_min`; **punët që janë tashmë të caktuara atë ditë**
- [ ] **`jobs.json`**: shabllonet, p.sh. "ditëlindje me bounce" = shoferi + montimi + maskota + çmontimi, me kohët dhe pajisjet
- [ ] **Një konflikt i qëllimshëm për demon:** p.sh. Van 2 i zënë deri në 17:00, ose një punëtor që s'arrin në kohë nga eventi tjetër. Agjenti duhet ta kapë.
- [ ] `tests/expected.md`: **5 raste të shkruara me dorë, para kodit** (hyrja → çka duhet të dalë)
- [ ] `docs/interview/notes.md`: pyet pronarët, me përgjigje fjalë për fjalë: (1) sa zgjat nga "po" e klientit deri te ekipi i informuar? (2) sa shpesh harrohet/ngatërrohet diçka? (3) a pranoni pilot 4 të shtuna?
- ⏰ **`company.json` + `jobs.json` deri në 14:30.** Motori i Gentit pret për to.

## 🖥️ Erza: `ui/`

- [ ] `ui/index.html`, `style.css`, `app.js`, `sample_view.json`
- [ ] Një ekran (paneli i liderit):
  - fusha ku lideri e shkruan punën + butoni Dërgo → `POST /api/message`
  - **feed-i "si mendon agjenti"** (`feed`)
  - **plani:** detyrat sipas personit dhe orës (`tasks`)
  - butoni **MIRATO** → `POST /api/approve`
  - statusi i secilit punëtor: dërguar / ✅ accepted / ❌ declined
  - **shiriti i kuq** kur një urdhër bllokohet (`blocked`)
- [ ] Nis me `sample_view.json` statik, pa pritur backend-in. Kur backend-i të jetë gati, ndërron vetëm URL-në te `GET /api/view`.
- [ ] Pamja: dark navy glass, ngjyrat jeshile/portokalli/kuqe për statuset, pa neon.
- ⏰ **15:00** versioni statik · **15:30** i lidhur me API-në
- Zëvendëse nëse mbaron limiti i AI-së: **Tringa**

## 🧪 Devlete: `tests/`, `scripts/`, `docs/`, `evidence/`

- [ ] `tests/test_engine.py`: pytest nga `tests/expected.md` e Flutures
- [ ] `docs/competitors.md`: ServiceTitan, Simpro (elektrikë), QGenda, symplr (spitale), ServiceNow, Atlassian JSM (IT), botët e rezervimeve (SleekFlow, PappaChat). Për secilin: çka bën, për kë, ku dallojmë. **Kurrë "askush s'e bën".**
- [ ] `docs/demand.md`: pse e blen dikush (PLAN §4), me burime; shembulli i parasë shkruhet **"Shembull, me supozime"**
- [ ] **15:30–16:00:** ekzekuton run-et e plota dhe i ruan në `evidence/`; `scripts/numbers.py` nxjerr numrat (sekondat nga mesazhi i liderit deri te ACCEPT i të gjithëve, rregullat e bllokuara, kostoja për punë)

## 🎤 Tringa: `pitch/`

- [ ] **3 slajde + demo:**
  1. **Problemi + përdoruesi real** (biznesi i Flutures, citatet e pronarëve)
  2. → **DEMO LIVE** ←
  3. **Si punon:** lideri → agjenti → kodi → ekipi, plus stack-u
  4. **Industritë** (tabela te PLAN §5), pse e blejnë (PLAN §4), **next step** (piloti)
- [ ] Numrat vetëm nga `evidence/` dhe nga pronarët
- [ ] Pa sisteme ose numra nga puna e askujt; pa shuma të shpikura si fakt
- ⏰ **Drafti 15:30 · final 17:00 · provë me kronometër 17:30**
- **Tani:** dërgoja Gentit username-in e GitHub-it

---

## Kontratat

### `industries/events/company.json` (Flutura plotëson, emrat të shpikur)
```json
{
  "company": {"name": "Festa Events (fictional)", "date": "2026-10-04", "depot_zone": "Prishtine"},
  "zones": ["Prishtine", "Mitrovice", "Vushtrri"],
  "travel_min": {"Prishtine-Mitrovice": 45, "Prishtine-Vushtrri": 35, "Mitrovice-Vushtrri": 20},
  "workers": [
    {"id": "w_erioni", "name": "Erioni", "skills": ["driver", "setup"]},
    {"id": "w_arta", "name": "Arta", "skills": ["mascot"]}
  ],
  "vehicles": [{"id": "van1", "name": "Van 1"}, {"id": "van2", "name": "Van 2"}],
  "equipment": [
    {"id": "bounce1", "type": "bounce", "name": "Bounce Kështjella"},
    {"id": "comp1", "type": "compressor", "name": "Kompresori 1"},
    {"id": "mascot_bear", "type": "mascot_costume", "name": "Kostumi Ariu"}
  ],
  "existing_jobs": [
    {"id": "J1", "title": "Ditëlindje (ekzistuese)", "zone": "Vushtrri", "from": "13:00", "to": "17:00",
     "assignments": {"w_erioni": "driver"}, "vehicle": "van2", "equipment": ["bounce1"]}
  ]
}
```

### `industries/events/jobs.json` (Flutura plotëson; minutat relativisht me nisjen e eventit)
```json
{
  "birthday_bounce": {
    "label": "Ditëlindje me bounce",
    "tasks": [
      {"id": "drive",    "role": "Shofer",          "skills": ["driver"], "start_offset_min": -100, "end_offset_min": 150, "vehicle": true},
      {"id": "setup",    "role": "Montimi i bounce", "skills": ["setup"],  "start_offset_min": -60,  "end_offset_min": 0,   "equipment": ["bounce", "compressor"]},
      {"id": "mascot",   "role": "Maskota",          "skills": ["mascot"], "start_offset_min": 0,    "end_offset_min": 90,  "equipment": ["mascot_costume"]},
      {"id": "teardown", "role": "Çmontimi",         "skills": ["setup"],  "start_offset_min": 120,  "end_offset_min": 150}
    ]
  }
}
```

### `view.json` (Genti e prodhon te `GET /api/view`, Erza e lexon)
```json
{
  "job": {"title": "Ditëlindje, 25 fëmijë", "zone": "Mitrovice", "start": "16:00", "status": "draft|awaiting_approval|sent|confirmed"},
  "tasks": [{"id": "t1", "role": "Shofer", "worker": "Erioni", "from": "14:20", "to": "18:30", "bring": ["Van 1"], "status": "planned|sent|accepted|declined"}],
  "workers": [{"id": "w_erioni", "name": "Erioni", "skills": ["driver"], "status": "free|busy|assigned"}],
  "feed": [{"t": "14:31:02", "type": "thinking|tool|check|blocked|sent|accepted", "text": "Van 2 i zënë deri 17:00 → përdor Van 1"}],
  "blocked": [{"text": "Dritoni s'arrin: 16:00 + 45 min = 16:45 > 16:30"}]
}
```
