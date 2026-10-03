# Competitor landscape

**Scope.** This is a desk-research snapshot of the products named in `PLAN.md` and `TASKS.md`. Capability descriptions below are limited to vendor documentation and official product pages. The comparison describes the proposed AI Team Leader in the current plan; it is not evidence that the prototype or a pilot already delivers those outcomes. Vendor pages change over time, and feature availability may depend on edition, configuration, or region.

## Summary

| Product | Category | What it does | Relationship to the proposed AI Team Leader |
|---|---|---|---|
| ServiceTitan | Field-service management for home and commercial trades | Scheduling, dispatch, job management, technician matching, route and schedule optimization, customer communications, and AI-supported dispatch features. | **Direct competitor** for trade and field-service coordination. It already addresses dispatch, skills, capacity, and routing. The current concept differs in its intended chat-first intake, small event-business starting point, and explicit human approval plus deterministic constraint checks; those differences remain product hypotheses, not proven advantages. |
| Simpro | Field-service management for trade and service businesses | Job and project operations, scheduling and dispatch for technicians and teams, inventory and related business workflows. | **Direct competitor** for assigning field teams and resources. Do not claim it lacks relevant capabilities; the proposed concept is a narrower conversational task-planning layer for a small operation. |
| QGenda | Healthcare workforce management | Provider, nurse, and staff scheduling; on-call; time and attendance; capacity management; rules-based and AI-supported schedule optimization. | **Direct competitor in healthcare** for workforce scheduling and deployment. The event-focused prototype is not a substitute for clinical scheduling or healthcare integrations. |
| symplr | Healthcare operations and workforce software | Healthcare scheduling, timekeeping, staffing, forecasting, workforce analytics, physician/on-call scheduling, and clinical communications. | **Direct competitor in healthcare** for scheduling and coverage workflows. It is an established, healthcare-specific suite; our planned prototype has neither its scope nor sector validation. |
| ServiceNow | Enterprise workflow and service management platform | Routes work items to service agents using configured queues, conditions, availability, capacity, and optionally skills; supports AI agents in assignment configurations. | **Direct competitor for enterprise work assignment and service workflows; adjacent to event operations.** Its assignment and routing capabilities overlap with our core orchestration idea. It is not reasonable to claim superiority over it. |
| Atlassian Jira Service Management (JSM) | IT service management and service desk | Captures service requests, organizes queues, supports SLA-based prioritization, automation, AI triage, and request handling. | **Direct competitor for IT/service-ticket coordination; adjacent to physical crew dispatch.** Its ticket intake and triage overlap with parts of our idea; the prototype instead targets jobs that may require people, vehicles, equipment, travel, and timed task sequences. |
| SleekFlow | Omnichannel customer messaging and CRM | Shared inbox, messaging channels including WhatsApp, Viber and Telegram, workflow automation, AI agents for customer conversations, lead qualification and routing. | **Adjacent product.** It can handle customer conversations and pass leads to teams. The reviewed materials do not establish multi-worker job planning across travel, equipment and overlapping assignments as its focus. That is a scope distinction, not a claim that integrations or custom workflows are impossible. |
| PappaChat | AI customer communication and booking assistant | Answers across messaging and other channels, takes bookings/requests, syncs calendars, and can hand conversations to staff. | **Adjacent product.** It automates customer response and appointments. Its public product description is not a field-crew resource scheduler; we have not tested whether it can be configured or integrated for such a workflow. |

## Product notes

### ServiceTitan

ServiceTitan offers field-service management for commercial and residential service contractors. Its official materials describe scheduling and dispatch, a dispatch board, skill-based technician matching, schedule optimization, routing, and live updates. Dispatch Pro describes assignment recommendations using technician skills, location, drive time, and performance, plus configurable automation. This is close overlap with dispatch and constraint-aware assignment in our concept. ServiceTitan is therefore a direct competitor in trades, not evidence that the problem is unsolved. Our initial event-business workflow and conversational intake are proposed differences; no comparative user or performance study has been done.

Sources: [ServiceTitan field-service dispatch](https://www.servicetitan.com/features/dispatch-software), [Dispatch Pro](https://www.servicetitan.com/features/pro/dispatch), [field-service scheduling](https://www.servicetitan.com/features/service-scheduling-software).

### Simpro

Simpro Premium is field-service management software aimed at service and trade businesses. Its official product page describes scheduling from individual technicians to teams, assigning people to quotes, jobs, or activities, and connecting scheduling with wider operations such as inventory. This makes it a direct competitor for field-service scheduling and dispatch. We have not found sufficient official evidence to make a specific claim about its current AI capabilities, so none is asserted here.

Source: [Simpro Premium](https://www.simprogroup.com/solutions/simpro-premium).

### QGenda

QGenda focuses on healthcare workforce management, covering providers, nurses, and staff. Official materials describe rules-based scheduling, workforce deployment, on-call management, time and attendance, capacity management, mobile self-service, and AI-supported scheduling and workforce optimization. Its target domain and operational depth make it a direct healthcare competitor. Our event prototype is not positioned as a healthcare product and has not implemented credentialing, patient coverage, clinical-system integration, or healthcare compliance workflows.

Sources: [QGenda workforce scheduling](https://www.qgenda.com/workforce-scheduling-software/), [QGenda workforce management](https://www.qgenda.com/workforcemanagement/).

### symplr

symplr sells operations and workforce products to healthcare organizations. Its workforce materials describe staffing and scheduling, timekeeping, analytics, demand forecasting, mobile workflows, and open-shift management; its clinical communications product includes on-call scheduling and role-based communications. It is a direct competitor for healthcare scheduling and coverage. The proposed AI Team Leader has not been validated for hospitals or built to replace a healthcare workforce suite.

Sources: [symplr Workforce](https://www.symplr.com/products/symplr-workforce), [Smart Square](https://www.symplr.com/products/smart-square), [symplr Clinical Communications on-call scheduling](https://www.symplr.com/workforce-management/workforce-management-on-call-scheduling).

### ServiceNow

ServiceNow's Advanced Work Assignment (AWA) routes work items to queues and assigns them to agents using configured routing and assignment rules. Its official documentation identifies availability, capacity, and optional skills as assignment inputs, and documents including AI agents in work distribution. This overlaps materially with our broader Team Leader idea of turning work into assignments and finding eligible people. The difference in the current plan is the narrower event-company workflow, free-text job intake, detailed worker briefings, and proposed code-enforced business constraints with a human approval step. These are design choices and intended scope; we do not claim ServiceNow cannot support comparable configurations or integrations.

Sources: [ServiceNow AWA overview](https://www.servicenow.com/docs/r/xanadu/servicenow-platform/advanced-work-assignment/awa-overview.html), [support AI agents in AWA](https://www.servicenow.com/docs/r/conversational-interfaces/advanced-work-assignment/awa-support-ai-agents.html?contentId=WagrX8E9BdK_NfGGBcw4nw).

### Atlassian Jira Service Management

Jira Service Management serves IT and other service teams handling requests, incidents, and service workflows. Atlassian describes request queues, SLA-based prioritization and escalation, AI triage, and service automation. It overlaps with intake, organizing work, and assigning or routing requests. The present concept is aimed at operational jobs whose plan can include simultaneous field workers, vehicles, physical equipment, travel time, and setup/teardown. JSM is not characterized here as lacking customization or integrations; our prototype is simply not an IT service desk.

Sources: [Jira Service Management ITSM features](https://www.atlassian.com/software/jira/service-management/features/itsm), [Atlassian AI feature guide for JSM](https://wac-cdn.atlassian.com/software/jira/service-management/product-guide/tips-and-tricks/artificial-intelligence).

### SleekFlow

SleekFlow is an omnichannel customer communication platform with a shared inbox, CRM, workflow automation, messaging channel support, and AI agents for answering customer questions, qualifying leads, and handing conversations to staff. Its channel documentation lists WhatsApp, Telegram, Viber, and other channels. It is adjacent to our proposal because it operates in customer messaging and can route conversations, but the reviewed public materials describe customer engagement rather than end-to-end field-job planning with people, vehicles, equipment, and travel constraints. No assertion is made about what a custom integration could do.

Sources: [SleekFlow product overview](https://help.sleekflow.io/en_US/getting-started/welcome-to-sleekflow), [supported channels](https://help.sleekflow.io/en_US/connecting-channels), [WhatsApp chatbot and AI capabilities](https://sleekflow.io/en-us/solutions/whatsapp-chatbot-platform).

### PappaChat

PappaChat describes an AI assistant for business customer communications across messaging, email, website chat, and phone. Its public product page describes answering questions, collecting requests, creating or awaiting confirmation for bookings, calendar syncing, and handing conversations to a person. It is adjacent to our proposal because it handles customer intake and booking conversations. The reviewed description does not position it as an internal multi-worker dispatch and resource-constraint planner. We have not tested it or assessed integration options.

Source: [PappaChat product overview](https://pappachat.com/en).

## Comparison boundary

The prototype's proposed focus is to turn a manager's free-text description of a job into a plan, check configured people/time/travel/vehicle/equipment constraints in code, request human approval, and send individual briefings with accept/decline actions. That is a product hypothesis described in `PLAN.md`, not a validated moat. Several named vendors already provide important parts of workforce scheduling, dispatch, routing, or AI-supported work assignment. The current evidence does not establish comparative accuracy, speed, price, adoption, local fit, language advantage, or market share. Claims about those points should wait for product tests, owner interviews, and a pilot.
