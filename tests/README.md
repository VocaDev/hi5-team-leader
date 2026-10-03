# tests — Devlete (kodi) + Flutura (`expected.md`)

> Gjendja 14:40: ⬜ `expected.md` (Flutura, 15:15) · ⬜ `test_engine.py` (Devlete)
> Teston **motorin** (kod pa AI). Falas, i menjëhershëm, pa çelës API.

## Si e shkruan testin
Motori është te `src/engine/planner.py`. Funksionet që të duhen:
```python
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from src.config import load_pack
from src.engine.planner import expand_job, plan_job, validate_manual

company, jobs, _ = load_pack()

def new_job(template="birthday_bounce", zone="Mitrovice", start="16:00", jid="J2"):
    return {"id": jid, "title": "Test", "zone": zone, "tasks": expand_job(jobs[template], start)}

def test_full_plan():
    plan = plan_job(company, new_job(), [])
    assert plan["feasible"]
    assert next(t for t in plan["tasks"] if t["id"] == "drive")["vehicle"] == "van1"   # Van 2 është i zënë

def test_leader_cannot_override():
    reasons = validate_manual(company, new_job(), [], "drive", "w_dritoni")
    assert reasons and reasons[0].startswith("R2")                                     # s'arrin në kohë
```
Ekzekutimi: `pytest tests -q`

## Çka teston (nga `expected.md` e Flutures)
1. plan i plotë · 2. BLOCKED kur lideri kërkon dikë që s'arrin · 3. refuzimi → personi tjetër me aftësinë · 4. puna e dytë në të njëjtën orë → mungon vani/pajisja · 5. rregulli i aftësisë (R1)

Kur Flutura i fut të dhënat e saj te `industries/events/`, testet përdorin ato. Përshtat id-të (`w_...`, `van...`) sipas tyre.

Branch: `devlete/tests` → PR. ⏰ 15:30.
