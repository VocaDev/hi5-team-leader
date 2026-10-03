# Demand: operational coordination problem and proposed value

## The operational problem

Every new job or service request has to be translated into work: establish what is needed, check who and what is available, sequence the tasks, account for timing and travel, communicate the plan, and respond when a person or resource becomes unavailable. In a small operation, those steps may be coordinated through calls, messages, spreadsheets, or a manager's own working knowledge. The result can depend on whether the right details were captured and whether all dependencies were checked.

This is a plausible recurring operational problem, but its frequency and cost for the specific event business in the plan have not yet been measured. External research supports the general importance and complexity of work scheduling and workforce planning; it does not prove the local team's current process or quantify losses from errors.

The International Labour Organization (ILO) describes variable, unstable schedules as creating difficulties for workers planning and coordinating their time, while also explaining that employers use schedule flexibility to respond to demand changes. The ILO's guide to working-time arrangements treats work schedules as an operational design issue for employers, workers, and governments. For healthcare, the World Health Organization's 2026 health workforce report identifies ongoing workforce availability and distribution challenges and the need for workforce information and planning. These sources support the general coordination context, not claims about event businesses in Kosovo.

Sources: [ILO, *Unstable and On-Call Work Schedules in the United States and Canada*](https://www.ilo.org/publications/unstable-and-call-work-schedules-united-states-and-canada); [ILO, *Guide to developing balanced working time arrangements*](https://www.ilo.org/publications/guide-developing-balanced-working-time-arrangements); [WHO, *National health workforce accounts: health workforce levels and trends 2026*](https://www.who.int/publications/i/item/9789240122925).

## Proposed value

The AI Team Leader proposal keeps the human leader responsible for the customer relationship and approval. A manager describes the job in ordinary language; the agent is intended to structure it, ask about missing details, and prepare a candidate plan. Deterministic code is intended to check configured constraints before a plan can be approved. The leader reviews the plan, then workers receive task-specific information and can accept or decline. If a worker declines, the system is intended to check for another eligible assignment and notify the leader.

The intended value is:

- **Accuracy:** apply configured checks consistently to staff, vehicles, equipment, time windows, existing work, and travel. The prototype's checks and their coverage must be verified; no measured error reduction is available yet.
- **Coordination speed:** reduce the manual steps between agreement on a job and a confirmed team. The 1–2 minute target in PLAN is a goal to test, not a result.
- **Scaling:** help one leader coordinate more work by preparing plans and distributing task details. Whether this increases jobs per leader without reducing quality is unknown.
- **Operational knowledge:** store job templates, skills, resource availability, and constraints in a shared system rather than relying only on a person's memory. The completeness and maintainability of that knowledge have not been assessed.
- **Constraint checking:** show why a proposed assignment is feasible or blocked according to explicit rules. A check only covers the data and rules entered; stale or incomplete inputs remain a risk to validate.
- **Reassignment:** when a worker declines, look for another eligible worker and seek renewed acceptance. Reassignment speed and success have not been measured.

## Evidence status and measurement plan

**Pending owner interviews (Flutura):** exact current workflow; time from customer agreement to the whole team being informed; how often something is forgotten or miscommunicated; owner quotations; and whether the owners would accept a four-Saturday pilot. These claims are intentionally left open until the answers are documented in `docs/interview/notes.md`.

**Pending product evidence (Genti and the later evidence runs):** whether the system works end to end; constraint-check correctness on written cases; time from manager message to all required worker acceptances; blocked-rule behavior; and time/success of reassignment. These must come from actual runs saved under `evidence/`, not planned behavior or invented values.

**Pending pilot evidence:** compare a defined set of jobs under the current process and with the tool. Record job scope, start/end timestamps, required and available resources, omitted/conflicting details, worker acceptances, declines, reassignment, and any manual corrections. Establish the measurement definitions before the pilot and report the sample and limitations. A four-Saturday pilot is proposed in PLAN, but acceptance is pending.

No local interviews or event-business evidence are used in this document. No performance, savings, market-size, willingness-to-pay, or error-rate claim is made.

## Commercial case

PLAN identifies potential reasons to buy: fewer coordination mistakes, faster confirmation, handling more work per leader, retaining operational knowledge, and faster reassignment after a decline. These are hypotheses. A buyer and price cannot be inferred from general workforce research or competitor product pages. The evidence needed next is the owner interview and a pilot using real, consented operational data.

No financial example is included because no verified local inputs are available. If one is added later, label it exactly **“Example, with assumptions”** and state each input and assumption separately; do not present it as observed savings.
