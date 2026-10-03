# Industry pack template
Copy this folder to `industries/<name>/` and fill in:
- `pack.json` — vocabulary (job = "event" / "post" / "visit"), roles and skills, criticality levels, allowed escalation options
- `rules.json` — which hard rules are on + parameters (rest hours, max hours, travel)
- `priority.json` — weights for ranking jobs when not everything can be covered
- `company.json` — the demo world, invented only
- `prompt.md` — domain words and dialect for the model
New industry = config only, if its rules use existing rule types. A new rule type = one small Python function + a test. See PLAN.md §4.
