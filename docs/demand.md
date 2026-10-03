# Demand: operational coordination problem and proposed value

## The operational problem

Every new job or service request has to be translated into work: establish what is needed, check who and what is available, sequence the tasks, account for timing and travel, communicate the plan, and respond when a person or resource becomes unavailable. In a small operation, those steps may be coordinated through calls, messages, spreadsheets, or a manager's own working knowledge. The result can depend on whether the right details were captured and whether all dependencies were checked.

The Magic Events interview notes describe this coordination work in that business and record several specific cases. They do not establish how often those cases occur or quantify the overall cost. External research supports the general importance and complexity of work scheduling and workforce planning; it does not establish the local frequency or cost.

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

## Magic Events interview evidence

The following are paraphrases of the interview notes dated 3 October 2026, not verbatim quotations. The notes identify Magic Events as an event-services business and document permission to mention its name and use the interview answers. These examples describe Magic Events only; they are not estimates for other businesses or for every Magic Events job.

- **Coordination time:** in a recent case, five workers were contacted almost simultaneously in the morning when nearly none were available; the process took about 3 hours. The notes separately describe a difficult case where full coordination took approximately 4 hours. The notes explicitly characterize 3–4 hours as an example from a difficult case, not an average.
- **Cross-team reassignment and delay:** to resolve a problem for one team, a worker planned for another team was used; a replacement was not found in time, and the second event was delayed by about 1 hour. The notes say this affected customer experience, perceived company seriousness, and the final event price, but provide no amount or quantified loss.
- **Late availability change:** workers are asked to give at least 4 hours' notice if they cannot participate, but the notes say this is not always followed and that notice can arrive about 30 minutes before departure. This is a late worker-unavailability notice; the notes do not establish that a customer cancelled an event 30 minutes before.
- **Operational dependencies:** the notes describe coordinating workers and skills, a vehicle, equipment and materials, location, departure/arrival timing, travel, and other scheduled events. They identify avoiding conflicts across existing jobs as a product requirement.

The interview notes do not establish event-wide rates for delays, cancellations, forgotten items, or conflicts; willingness to pay; ROI; market size; savings; or acceptance of a pilot. No such figures are inferred here.

## Evidence status and measurement plan

**Pending product evidence (Genti and the later evidence runs):** whether the system works end to end; constraint-check correctness on written cases; time from manager message to all required worker acceptances; blocked-rule behavior; and time/success of reassignment. These must come from actual runs saved under `evidence/`, not planned behavior or invented values.

**Pending pilot evidence:** compare a defined set of jobs under the current process and with the tool. Record job scope, start/end timestamps, required and available resources, omitted/conflicting details, worker acceptances, declines, reassignment, and any manual corrections. Establish the measurement definitions before the pilot and report the sample and limitations. A four-Saturday pilot is proposed in PLAN; the interview notes do not record whether the owners accepted it.

The Magic Events interview is used only as attributed case evidence above. No demo-performance, savings, market-size, willingness-to-pay, general-frequency, or quantified error-rate claim is made.

## Commercial case

PLAN identifies potential reasons to buy: fewer coordination mistakes, faster confirmation, handling more work per leader, retaining operational knowledge, and faster reassignment after a decline. These remain business hypotheses. The Magic Events interview gives specific examples of coordination time and a cross-team delay, but does not establish willingness to pay, realized savings, or pilot acceptance. Those require further customer validation and a pilot using consented operational data.

No financial example is included because no verified local inputs are available. If one is added later, label it exactly **“Example, with assumptions”** and state each input and assumption separately; do not present it as observed savings.
