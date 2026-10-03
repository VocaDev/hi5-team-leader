# Competitor landscape

**Scope:** Current official product materials, checked 3 October 2026. This compares documented capabilities with the current Magic Events demo. Capabilities can depend on product plan, configuration, and rollout. “Our prototype” means the hackathon implementation; it does not imply a production-ready product or a proven advantage.

## At a glance

| Product | What it does / who it serves | Overlap with AI Team Leader | How our current prototype differs in emphasis |
|---|---|---|---|
| **Connecteam** | Mobile workforce management for small teams and larger businesses: scheduling and dispatching jobs, task completion, time tracking, team communication, and other employee operations. Its Small Business Plan is currently advertised as free for companies with **up to 10 users**. | Very high for small operational teams. Job schedules can include location and instructions; shift tasks have completion tracking; employees can confirm or reject shifts; the product describes AI-assisted scheduling and last-minute changes. | Magic Events demo starts with a leader’s unstructured customer request and demonstrates the connected flow through a proposed plan, code checks for configured event constraints, human approval, worker actions in Telegram, check-ins, progress, problem handling/reassignment, and an owner report. Connecteam already covers much of workforce scheduling and follow-through; this is a difference in the demo’s workflow/context, not a claim it cannot be configured to do similar things. |
| **Microsoft Planner Agent** | AI work and task management in Microsoft Planner/Copilot for people and teams already working with plans, tasks, goals, and Microsoft 365 content. | Creates plans and tasks from goals/files, answers questions, updates task properties, can execute assigned tasks and produce status reports. Drafts can be reviewed and approved. | Our demo interprets a customer’s event request and plans physical operations against configured people, vehicle, equipment, time, and travel rules, then dispatches work to staff and follows operational check-in/progress. Planner Agent’s documented task execution produces task output and plan/report updates; it is not the physical event operations flow shown in our demo. |
| **Asana AI Teammates** | Configurable AI teammates inside Asana, for teams coordinating work through projects, tasks, and workflows. | Can receive assigned work, use task/project context and configured skills, create or update work, and collaborate with people through review/checkpoints. Asana describes workflow agents for operations, intake, validation, routing, risk alerts, and reporting. | Our prototype’s center is an event operation with hard-coded checks against physical resources and an actual worker response/progress loop. Asana has substantial overlap in AI-supported orchestration and workflow coordination; the distinction is the operational model and current demo integration, not AI capability or general task coordination. |
| **Atlassian Rovo** | Atlassian’s AI search, chat, and configurable agents, grounded in Jira, Confluence, and connected apps; used by teams managing knowledge and work in Atlassian products. | Agents can use organizational context, follow objectives and permissions, and—with configured tools—create, edit, organize, or comment on Jira work items and Confluence content. Agents can run from chat, automation, and Atlassian editing/workflows. | Our current demo is centered on a small event business and worker-facing execution through Telegram, with configured physical-resource checks and live operational status. Rovo is deeply grounded in Jira/Confluence and connected work data; it is not accurate to say it only answers questions or cannot act. A customized Rovo workflow may overlap further. |
| **ServiceTitan** | Field-service management for residential and commercial contractors/trades, spanning booking, scheduling, dispatch, technician workflows, and service operations. | Strong overlap in operational dispatch: technician skills, schedules/capacity, routing, real-time updates, job assignment recommendations, and mobile field workflows. Dispatch Pro documents AI/algorithm-supported recommendations and automated assignment options. | The demo uses Magic Events’ event jobs and crew/resources, with a conversational request and a visible human-approval-to-worker-confirmation/check-in/progress/report loop. ServiceTitan is the more established field-service system and already has dispatch and workforce features; our prototype is not a replacement for its broader contractor operations suite. |

## Product notes and official sources

### 1. Connecteam

Connecteam presents itself as an employee/workforce management app for businesses of different sizes, including small teams. Its current help material says the Small Business Plan is free for companies with up to 10 users (including active and archived users); the company says this plan includes the platform features. Its job scheduler creates shifts or dispatch jobs with location, instructions, and attachments. Shift tasks can be tracked to completion, while scheduling settings can include employee confirm/reject options. Connecteam’s current homepage also describes AI-assisted scheduling, job/task addition, last-minute changes, and employee progress tracking.

This is the toughest direct comparison for the small-business positioning. The pitch should acknowledge the overlap. We can show our Magic Events workflow and the specific deterministic constraints encoded in our demo, but must not suggest Connecteam lacks small-team scheduling, tasks, mobile operations, confirmation/rejection, or AI scheduling.

Sources: [Small Business Plan FAQ](https://help.connecteam.com/en/articles/6393056-small-business-plan-frequently-asked-questions), [user limit for Small Business Plan](https://help.connecteam.com/en/articles/9448683-is-there-a-limit-to-the-number-of-users-i-can-add-to-a-plan), [job scheduler guide](https://help.connecteam.com/en/articles/4100339-starting-guide-to-the-job-scheduler), [shift task completion tracking](https://help.connecteam.com/en/articles/6618394-shift-tasks), [schedule rules and alerts](https://help.connecteam.com/en/articles/6400563-job-scheduling-must-have-capabilities), [Connecteam homepage and AI scheduling description](https://connecteam.com/).

### 2. Microsoft Planner Agent

Microsoft documents Planner Agent capabilities including creating plans and tasks, generating proposed task lists from goals and files, answering questions about work, editing supported task fields, executing assigned tasks, and generating status reports from plan progress and activity. AI-generated plans, tasks, and updates can be reviewed and approved. Microsoft’s documentation notes that capability and plan support varies by Planner Agent experience and is subject to rollout; for example, its FAQ describes limits on which plan types and task properties the Copilot experience supports.

The strongest distinction for our demo is that a Planner task is a work-management object, while our example task represents a physical event operation with configured equipment, vehicle, travel, and timed work constraints, followed by worker confirmation and operational progress. Do not claim that Microsoft’s agent cannot create tasks, execute assigned work, use organizational context, or report status.

Sources: [What Planner Agent can do](https://support.microsoft.com/en-us/planner/what-can-you-do-with-planner-agent-in-copilot), [Planner Agent FAQ and current limitations](https://support.microsoft.com/en-us/planner/planner-agent-limitation), [execute tasks and generate status reports](https://support.microsoft.com/en-us/planner/copilot/generate-automatic-status-reports-with-planner-agent), [Planner Agent FAQ on execution and plan creation](https://support.microsoft.com/lt-LT/Planner/copilot/frequently-asked-questions-about-planner-agent).

### 3. Asana AI Teammates

Asana AI Teammates are configurable agents intended to work inside Asana projects and workflows. Asana documents assigning a Teammate work like a team member, giving it context, guidance, skills, and permissions, and reviewing its work. Its AI Studio materials cover intake, validation, classification, routing, alerts for risks/blockers, and reporting. That is meaningful overlap with orchestration, human checkpoints, contextual communication, and follow-through in the broad sense.

Our current prototype is narrower: a small event-business demo with a leader’s free-text request, deterministic checks for its configured operational rules, explicit leader approval, worker actions in Telegram, and a follow-up status/report loop. Asana’s broad workflow-agent capability means the pitch cannot claim that “AI creating and coordinating tasks” is itself our differentiation.

Sources: [Asana AI Teammates](https://asana.com/product/ai/ai-teammates), [Asana AI Teammates overview and workflow examples](https://asana.com/resources/ai-teammates-overview), [AI Studio workflow automation](https://asana.com/product/ai/ai-studio), [Asana Help: getting started with AI](https://help.asana.com/s/article/get-started-with-asana-ai).

### 4. Atlassian Rovo

Rovo combines AI search/chat and configurable agents. Atlassian says agents can use Jira, Confluence, and connected-app context; agents can be invoked in chat, automation, and while editing Jira/Confluence content. With permission and configured tools, they can create, organize, or edit Jira work items and Confluence pages. Rovo therefore overlaps with contextual agents that act inside workflows, not just chatbots that answer questions.

Our demo differs by the operational target and interface: a Magic Events leader initiates a real event plan, and the runtime follows assignments and worker status in Telegram. Rovo’s documented strength is Atlassian work context and extensible in-product actions. A customized Rovo agent and integrations could be adapted to more workflows, so we do not claim Rovo is incapable of operational orchestration.

Sources: [What is Rovo?](https://support.atlassian.com/rovo/docs/what-is-rovo/), [Rovo agents](https://support.atlassian.com/rovo/docs/agents/), [configure tools for Rovo agents](https://support.atlassian.com/rovo/docs/configure-tools-for-rovo-agents/), [Rovo Studio and Teamwork Graph](https://www.atlassian.com/software/rovo/studio).

### 5. ServiceTitan

ServiceTitan is an end-to-end field-service platform for trade contractors. Its official materials document scheduling and dispatch, technician availability and skills, schedule optimization, routing, job notifications, field/mobile workflows, and assignment recommendations based on factors such as skills and location. Dispatch Pro describes AI/algorithm-supported recommendations, centralized task prioritization, and configurable automation. These features directly overlap with parts of our intended operational coordination flow.

Our current demo is for Magic Events, not a trade-contractor business, and demonstrates event-specific job decomposition, configured hard-rule checks, approval, task distribution, worker response, check-in/progress, problem handling, and a report. ServiceTitan already has mature field-service scheduling and dispatch. We have not established that our prototype is easier, cheaper, more accurate, or better suited to any customer segment.

Sources: [ServiceTitan dispatch](https://www.servicetitan.com/features/dispatch-software), [Dispatch Pro](https://www.servicetitan.com/features/pro/dispatch), [ServiceTitan scheduling](https://www.servicetitan.com/features/service-scheduling-software), [ServiceTitan product features](https://www.servicetitan.com/features).

## What we can honestly claim in the pitch

1. **Show the connected demo flow:** a leader’s unstructured event request becomes a proposed plan, is checked by code, requires human approval, reaches workers in Telegram, and is followed through worker status and a report. This describes what the demo does; it does not claim the sequence is unique in the market.
2. **Explain the responsibility boundary:** AI interprets and communicates; deterministic code enforces the constraints encoded in this prototype; a human approves; workers confirm and report status. This is our architecture and safety design, not a claim that competitors have no rules or human oversight.
3. **Name the specific starting context:** the current example is Magic Events, with event tasks and configured staff, vehicle, equipment, timing, and travel constraints. The prototype demonstrates this particular operational model; customer fit and comparative value still need validation.

## Hard mentor questions

### 1. “Why isn’t this just Connecteam?”

Connecteam is a real alternative for small teams: it already offers job scheduling, dispatch, shift tasks, worker status, workforce tools, and an AI scheduler; its Small Business Plan is advertised as free up to 10 users. Our demo is a different workflow emphasis: begin with a customer’s unstructured event request, build a plan using our configured event rules, require leader approval, then follow individual workers’ accept/check-in/progress and issue handling in Telegram. We have not proven that a Magic Events customer needs a separate product or prefers this flow over configuring Connecteam.

### 2. “Why isn’t this just Microsoft Planner / Asana / Rovo?”

Those products already use AI to create or manage tasks and act within work-management systems. Our present demo is centered on physical event execution: people, timed task sequences, vehicle/equipment availability and travel rules, followed by worker responses and operational status. That is a difference in the domain model and integrated demo path, not a claim that those products cannot be extended or integrated for similar workflows.

### 3. “Why do you need an AI agent instead of a normal scheduling application?”

**Deterministic code should handle constraints, availability, and hard rules.** We should not ask a language model to decide whether a van, worker, or time slot is truly available. AI is justified for interpreting an unstructured customer request, asking for missing details, orchestrating the planning tools, communicating role-specific context, and reacting to changing workflow state such as a worker reporting a problem. If requests and exceptions are already structured, a conventional scheduling application may be sufficient.

### 4. “Why would a small business pay for this?”

Our business hypothesis is that it could reduce coordination overhead and operational mistakes, make essential planning knowledge less dependent on one manager’s memory, and let that manager handle more work. We have not established willingness to pay, savings, or a productivity gain. Those require customer interviews and a pilot with Magic Events or another target customer.

### 5. “What is actually new here if these competitors already use AI?”

We are not claiming a new kind of AI or that AI task planning is novel. The proposition is to connect conversational intake to a domain-specific, code-validated operational plan, human approval, real worker actions, and follow-through in one demo workflow for a small event operation. Competitors overlap with parts of that sequence, and some offer substantial agentic workflows already. Whether this integrated experience is useful enough to adopt is the hypothesis to validate.
