# ShiftRescue — Expected Test Cases

These expected results are defined before running the agent.
The agent output must not be manually edited to match them.

---

## Test 1 — Normal birthday with mascot

### Input
New job:
- Type: birthday_mascot
- Zone: Prishtine
- Start: 18:00

### Available relevant resources
- Drivers: Erioni, Dritoni, Naim
- Mascot workers: Arta, Leart
- Van 1 and Van 2
- Mascot costume: Kostumi Ariu

### Expected
The system must create a valid plan using:
- one available driver,
- one available mascot worker,
- one available van,
- the mascot costume.

The selected workers and resources must not conflict with existing jobs.

### Must not happen
- Assign a busy worker.
- Assign the same worker to overlapping tasks.
- Use a vehicle that is already occupied during the required time.

---

## Test 2 — Busy worker is not available

### Input
New job:
- Type: birthday_bounce
- Zone: Mitrovice
- Start: 16:00

### Existing conflict
Dritoni is assigned to existing job J1 in Vushtrri from 13:00 to 17:00.

### Expected
Dritoni must NOT be assigned to the new job during the conflicting period.

The system must search for another worker with the required skill.

### Why
Having the correct skill does not mean the worker is available.

### Must not happen
The engine must not assign Dritoni simply because he has:
- driver
- setup

---

## Test 3 — Busy vehicle/equipment cannot be reused

### Input
New job:
- Type: birthday_bounce
- Start before 17:00

### Existing conflict
J1 already uses:
- Van 2
- Bounce Kështjella (bounce1)
- Kompresori 1 (comp1)

from 13:00 to 17:00.

### Expected
The new plan must NOT use:
- van2
- bounce1
- comp1

during the conflicting period.

If possible, the engine should use:
- van1
- bounce2
- comp2

### Must not happen
The same vehicle or equipment must never be assigned to two overlapping jobs.

---

## Test 4 — Missing skill must block assignment

### Input
A birthday_bounce job requires:
- driver
- setup
- mascot

### Worker
Arta has:
- mascot

but does NOT have:
- driver
- setup

### Expected
Arta may only be assigned to the mascot task.

She must NOT be assigned as:
- driver
- bounce setup
- teardown

### Must not happen
The system must not use an available worker for a task they are not qualified to perform.

---

## Test 5 — No safe complete plan

### Input
Create a new birthday_bounce job at a time where the available combination of:
- workers,
- vehicle,
- bounce,
- compressor,
- mascot costume

cannot satisfy all required tasks without conflicts.

### Expected
The system must:
1. detect that no complete safe plan exists,
2. explain the blocking constraints,
3. return the job as blocked / requiring human decision.

### Expected explanation examples
- required worker unavailable,
- vehicle already assigned,
- required equipment already in use,
- timing or travel conflict.

### Must not happen
The system must NOT:
- invent a worker,
- invent a vehicle,
- invent equipment,
- ignore an existing assignment,
- claim the job is feasible when required resources are missing.