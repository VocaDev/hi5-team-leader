# industries/events — Flutura

> Gjendja 14:40: ✅ intervista (PR #2) · ⬜ `company.json` · ⬜ `jobs.json` · ⬜ `tests/expected.md`
> Backend-i punon. Sapo këto skedarë të futen në `main`, agjenti i përdor vetë në vend të `src/dev_data/`.

## Çka bën ti, me radhë

### 1. `company.json` ⏰ 15:00
**Kopjo `src/dev_data/company.json` këtu dhe ndryshoje** sipas Magic Events (forma e punës reale, emrat të shpikur):
- `company.date` = **`"2026-10-10"`** (e shtunë) + `"day_label": "e shtunë 10 tetor"`. Agjenti e kap vetë nëse dita s'përputhet.
- `zones` dhe `travel_min` (minutat ndërmjet zonave, ❓ vlera të supozuara)
- `workers`: `id` (`w_emri`), `name`, `skills` (`driver`, `setup`, `mascot`, `bubble`, … vetëm fjalë që i përdor edhe te `jobs.json`). Opsionale: `max_hours`, `unavailable: [{"from": "HH:MM", "to": "HH:MM"}]`
- `vehicles` dhe `equipment` (`type` duhet të përputhet me `equipment` te `jobs.json`)
- `existing_jobs`: punët e rezervuara atë ditë, me `assignments {worker_id: rol}`, `vehicle`, `equipment`

**Konflikti i demos (gjetja 2 e intervistës):** dikush duket i lirë por **duhet më vonë te një event tjetër**, ose **s'arrin në kohë** nga një zonë tjetër. Te dev data: Dritoni është te J1 në Vushtrri deri në 17:00. Mbaje një rast të tillë.

### 2. `jobs.json` ⏰ 15:00
Shabllonet e punëve. Minutat janë relative me nisjen e eventit (p.sh. `-60` = 1 orë para). Shembull te `src/dev_data/jobs.json`. Shto 2–3 shabllone reale të Magic Events (p.sh. bounce, bubble, maskotë), me kohët e montimit dhe çmontimit.

### 3. Kontrollo vetë
```bash
python -m src.engine.planner          # nxjerr planin e një ditëlindjeje test me të dhënat e tua
```
Nëse del `"feasible": true` dhe refuzimet kanë kuptim (p.sh. *"Dritoni ... + 20 min rrugë = 17:20 > 14:20"*), je në rregull.

### 4. `tests/expected.md` ⏰ 15:15
5 raste **me dorë, para se t'i provojë kodi**. Për secilin: hyrja (mesazhi i liderit) → çka duhet të dalë. P.sh.:
1. Ditëlindje 16:00 Mitrovicë → plan i plotë, Van 1 (Van 2 i zënë)
2. Lideri: "vendose Dritonin shofer" → **BLOCKED** (s'arrin në kohë)
3. Arta shtyp S'MUNDEM → detyra kalon te dikush tjetër me aftësinë `mascot`
4. Puna e dytë në të njëjtën orë → çka mungon (van/pajisje) + opsione, pa plan të paplotë
5. Mesazh pa orë → agjenti pyet (NEEDS_INFO)

## Rregullat e pronarëve (nga intervista) → si i mban kodi
| Rregulli | Te kodi |
|---|---|
| Aftësia e duhur | R1 |
| Askush (as vani, as pajisja) në dy vende njëherësh | R2 + R6 |
| Koha e udhëtimit | R2 |
| Premtimet ndaj klientit s'ndryshohen pa miratimin e tij | agjenti s'i shkruan klientit; lideri miraton |
| Siguria s'komprometohet | detyrat me aftësi (p.sh. `setup` për bounce) |

Branch: `flutura/data` → PR. Ndryshim te formati? Pyet Gentin.
