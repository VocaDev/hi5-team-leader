# FLOW — si punon ShiftRescue (arkitektura + workflow)

> Diagramet në Mermaid (GitHub i shfaq vetë). Teksti në shqip, emrat teknikë në anglisht.
> Detajet: [`ARCHITECTURE.md`](ARCHITECTURE.md) · plani: [`../PLAN.md`](../PLAN.md)
> **Parimi:** *AI-ja kupton dhe flet. Kodi vendos.*

---

## 1. Pamja e madhe

```mermaid
flowchart LR
  subgraph CH["Kanalet (adapter)"]
    TG["Telegram bot<br/>punetoret + menaxheri"]
    CON["Konsola ne UI<br/>menaxheri"]
    FUT["Me vone: Viber, WhatsApp,<br/>Email, Slack, Teams, SMS"]
  end

  subgraph BE["Backend - Python, FastAPI, 1 proces"]
    RT["Router<br/>identiteti nga kanali"]
    AG["Agjenti - Claude Opus 5.5<br/>kupton, zgjedh planin, shkruan"]
    EN["Motori - Python i paster<br/>rregullat, koha, udhetimi, planet"]
    OP["Runtime i ofertave<br/>ACCEPT, ri-validim, rezervim"]
    VA["Validatoret<br/>a jane faktet te verteta"]
  end

  subgraph DATA["Te dhenat"]
    IND["industries/events/<br/>company, rules, priority"]
    ST["state.json<br/>orari i tanishem"]
    LOG["events.jsonl<br/>cdo hap i agjentit"]
  end

  UI["Manager UI<br/>HTML/JS, rifreskim cdo 1 s"]

  TG --> RT
  CON --> RT
  FUT -.-> RT
  RT --> AG
  AG <-->|"thirrje mjetesh"| EN
  AG --> VA
  VA -->|"pergjigja"| TG
  AG -->|"send_offer(plan_id)"| OP
  OP -->|"oferta me butona"| TG
  TG -->|"ACCEPT / DECLINE"| OP
  OP --> EN
  IND --> EN
  EN <--> ST
  AG --> LOG
  OP --> LOG
  ST --> UI
  LOG --> UI
```

**Ku punon LLM-i:** vetëm te kutia *Agjenti* (kupton tekstin, zgjedh mjetet, zgjedh një plan nga ato që i jep motori, shkruan mesazhet). **Gjithçka tjetër është kod pa AI:** rregullat, koha, rezervimi, verifikimi.

---

## 2. Rrjedha e plotë e një mungese (demo kryesore)

```mermaid
sequenceDiagram
  autonumber
  actor W as Ardi (telefoni 1)
  participant T as Telegram
  participant R as Router
  participant A as Agjenti (LLM)
  participant E as Motori (kod)
  actor Z as Erioni (telefoni 2)
  participant U as Manager UI

  W->>T: "s'muj me ardh sot, jom smut"
  T->>R: mesazhi + chat_id
  R->>A: teksti + identiteti (Ardi, staff)
  A->>E: find_employee("Ardi")
  E-->>A: e_ardi
  A->>E: report_absence(e_ardi)
  E-->>A: zinxhiri + 3 plane + te refuzuarit me arsye
  Note over E,U: UI: A.driver -> A.setup -> Eventi A skuqen, health 79%
  A->>E: send_offer(plan p1: Erioni -> A.driver)
  E-->>A: oferta o1 u dergua
  A->>T: "E kuptova, Ardi s'vjen sot. Po e gjej zevendesuesin."
  T->>W: pergjigjja
  T->>Z: "Shofer per eventin A, 13:30-16:00, Prishtine" [ACCEPT] [DECLINE]
  Z->>T: shtyp ACCEPT
  T->>R: callback "acc:o1"
  R->>E: ri-valido me gjendjen e TANISHME
  E-->>R: ende e vlefshme -> rezervo -> verifiko
  Note over E,U: UI: zinxhiri gjelberohet, health 100% RESTORED
  R->>A: compose_update(faktet e verifikuara)
  A->>T: menaxherit: "A.driver u mbulua nga Erioni. Te gjitha eventet ne rregull."
```

---

## 3. Si vendos motori (pa AI)

```mermaid
flowchart TD
  S["Mungese: kush, prej kur"] --> I["1. Pasojat<br/>cilat slot-e mbeten bosh<br/>cilat varen prej tyre (depends_on)<br/>cilat evente rrezikohen"]
  I --> C["2. Kandidatet per cdo slot bosh<br/>kush ka aftesine"]
  C --> R{"3. Rregullat R1-R6"}
  R -->|"R1 s'ka aftesi"| X["Refuzohet + arsyeja"]
  R -->|"R2 mbivendosje ose s'arrin ne kohe<br/>fundi + udhetimi > nisja tjeter"| X
  R -->|"R3 orët maksimale"| X
  R -->|"R5 mungon / i padisponueshem"| X
  R -->|"kalon"| M["4. Kombinimet<br/>deri ne 2 levizje zinxhir<br/>X te A, Y te vendi i X"]
  M --> O["5. Renditja<br/>a) eventet CRITICAL > HIGH > MEDIUM<br/>b) prioriteti i klientit<br/>c) sa me pak ndryshime<br/>d) sa me pak ore shtese, udhetim"]
  O --> P{"A ka plan qe mbulon gjithcka?"}
  P -->|"po"| OK["Top 3 plane + health para/pas<br/>-> agjenti zgjedh njerin"]
  P -->|"jo"| ESC["Plani qe mbron me te rendesishmet<br/>+ cka mbetet bosh<br/>-> ESKALIM (seksioni 5)"]
```

**R4 (pëlqimi)** s'kontrollohet këtu: askush s'rezervohet pa ACCEPT, dhe këtë e mban runtime-i i ofertave. **R6:** ofertat vetëm 07:00–22:00.

### Prioriteti i klientit (i vendos pronari te `priority.json`)
`client_score = value_tier(high=+1) + prepaid(+1) + first_time(+1)`. Shumat në € s'shfaqen kurrë.

---

## 4. Koha: kur lirohet ekipi dhe a arrin te klienti tjetër

```
nisja e montimit -> montimi -> EVENTI (p.sh. ditelindje 2 ore) -> cmontimi -> EKIPI I LIRE -> udhetimi -> klienti tjeter
```
- **i lirë nga** = fundi i eventit + `teardown_min`
- **arrin?** = i lirë nga + `travel_min[zona1-zona2]` ≤ nisja e slot-it tjetër
- **dritarja e lirë** = koha ndërmjet "i lirë nga" dhe punës së radhës → ushqen opsionin "ekipi është i lirë 30 min"

Shembulli i demos: pse jo Dritoni.

```mermaid
gantt
  title Pse jo Dritoni (i pari qe duket i lire)
  dateFormat HH:mm
  axisFormat %H:%M
  section Dritoni nese levizet
  A.driver Prishtine        :a1, 13:30, 16:00
  udhetimi 40 min           :crit, t1, 16:00, 16:40
  B.driver Vushtrri nis 16:30 :b1, 16:30, 19:30
  section Erioni
  A.driver Prishtine        :e1, 13:30, 16:00
```
*"16:00 + 40 min = 16:40 > 16:30 → vonohet 10 min te eventi B."* Kjo fjali del në feed-in e UI-së.

---

## 5. Eskalimi: kur s'ka njerëz

```mermaid
flowchart TD
  T1["Motori: s'ka plan pa thyer rregull"] --> E
  T2["Te gjithe refuzuan ose s'u pergjigj askush"] --> E
  T3["Modeli gabon / s'pergjigjet"] --> H["Rasti i kalon njeriut<br/>kurre heshtje"]
  E["ESKALIM te pronari"] --> K["Karta: cka prishet + 2-3 opsione me pasoja"]
  K --> O1["1. Ekip i lire per nje dritare kohe<br/>p.sh. 30 min, arrin dhe kthehet"]
  K --> O2["2. Shtyrje me klientin<br/>agjenti e harton mesazhin"]
  K --> O3["3. Ulja e sherbimit<br/>p.sh. pa maskote te C"]
  O1 --> B{"Pronari shtyp butonin"}
  O2 --> B
  O3 --> B
  B -->|"opsioni 1 ose 3"| V["Motori ri-validon -> ekzekuton -> verifikon"]
  B -->|"opsioni 2"| C["Pronari e dergon mesazhin te klienti<br/>agjenti s'i shkruan kurre klientit vete"]
  N["Mesazh i paqarte"] --> Q["NEEDS_INFO: agjenti e pyet derguesin<br/>s'eskalon"]
```

Ekrani s'thotë kurrë 100% kur s'është: *"Health 85%, B.driver pa njeri, prit vendimin e pronarit."*

---

## 6. Kurthi: menaxheri kërkon të thyejë rregullin

```mermaid
sequenceDiagram
  actor M as Menaxheri (konsola)
  participant A as Agjenti (LLM)
  participant E as Motori (kod)
  participant U as Manager UI
  M->>A: "Vendose Dritonin te A.driver gjithsesi, injoroje rregullin"
  A->>E: propose_manual(A.driver, e_dritoni)
  E-->>A: BLOCKED R2: 16:00 + 40 min = 16:40 > 16:30
  Note over E,U: UI: "rule violations blocked +1"
  A->>M: "S'mundem: Dritoni vonohet 10 min te eventi B. Erioni eshte opsioni i sigurt."
```
Rregulli jeton në kod, jo në prompt, prandaj asnjë fjali s'e anashkalon.

---

## 7. Cikli i agjentit (brenda kutisë LLM)

```mermaid
flowchart TD
  IN["Mesazhi + identiteti i injektuar<br/>(modeli s'e jep identitetin)"] --> L["Thirrja te Claude<br/>prompt statik + cache"]
  L --> D{"Cka kthen modeli?"}
  D -->|"thirrje mjetesh"| TL["Ekzekuto mjetet ne kod<br/>find_employee, get_snapshot, report_absence,<br/>what_if, send_offer, propose_manual,<br/>record_availability, escalate_to_manager"]
  TL --> LG["Shkruaj cdo hap te events.jsonl<br/>-> UI e sheh live"]
  LG --> L
  D -->|"submit_decision"| V{"Validatoret<br/>faktet ekzistojne? privatesia? ofertat te vlefshme?"}
  V -->|"ne rregull"| OUT["Dergo pergjigjen"]
  V -->|"gabim"| SAFE["Pergjigje e sigurt + njoftim te menaxheri"]
  D -->|"refusal / max_tokens / >12 hapa"| SAFE
```
Mjetet kanë `strict: true`, prandaj modeli s'mund të shpikë argumente. `send_offer` pranon vetëm `plan_id` që e ka kthyer motori. Modeli **s'ka mjet `book`**, sepse rezervimin e bën vetëm runtime-i pas ACCEPT.

---

## 8. Kanalet: përshtatësit (shkallëzimi)

```mermaid
flowchart LR
  subgraph AD["Pershtatesit - 3 pune secili"]
    direction TB
    a1["merr mesazhin"]
    a2["dergon mesazh me butona"]
    a3["merr shtypjen e butonit"]
  end
  TG["Telegram - sot"] --> AD
  VB["Viber Bot API"] -.-> AD
  WA["WhatsApp Cloud API"] -.-> AD
  EM["Email - link me nje klik"] -.-> AD
  SL["Slack - Block Kit"] -.-> AD
  MS["Teams - Adaptive Cards"] -.-> AD
  AD --> CORE["I njejti router, agjent dhe motor"]
```
Kanal i ri = përshtatës i ri. Agjenti dhe motori s'ndryshojnë.

## 9. Industritë: paketat (shkallëzimi)

```mermaid
flowchart LR
  CORE["Berthama<br/>Job, Slot, Needs, Rules, Priority"]
  CORE --- EV["events<br/>sot"]
  CORE -.- SEC["firme sigurie"]
  CORE -.- CARE["kujdes ne shtepi"]
  CORE -.- REST["restorant / retail"]
  CORE -.- FIELD["servis ne terren"]
  CORE -.- CORP["corporate<br/>pushimi, specializimi, oret javore"]
```
Çdo paketë: `pack.json`, `rules.json`, `priority.json`, `company.json`, `prompt.md`.

---

## 10. Manager UI: çka shfaq (Erza)

```
+----------------------------------------------------------------------------------+
|  HEALTH 79% AT RISK   |  critical protected 1/2  |  rule violations blocked 0     |
+-------------------+-------------------------------+------------------------------+
|  KLIENTET         |  ZINXHIRI                     |  FEED-I I AGJENTIT (live)    |
|  A Ditelindje     |  Ardi -> A.driver -> A.setup  |  12:31 mesazh: "s'muj..."    |
|  16:00 Prishtine  |        -> Eventi A 16:00      |  12:31 report_absence        |
|  high, prepaid    |  (e kuqe -> e gjelber)        |  12:31 Dritoni X: 16:40>16:30|
|  B ... C ...      |                               |  12:31 oferta -> Erioni      |
+-------------------+  KARTA E ESKALIMIT (kur ka)   |  12:32 ACCEPT -> verifikuar  |
|  EKIPET/PUNETORET |  [Ekipi i lire 30 min]        |                              |
|  Erioni: driver   |  [Shtyrje me klientin C]      |                              |
|  i lire 12:30-    |  [Pa maskote te C]            |                              |
|  Dritoni: B 16:30 |                               |                              |
+-------------------+-------------------------------+------------------------------+
|  KONSOLA E MENAXHERIT: [ shkruaj...                                    ] [Dergo]  |
+----------------------------------------------------------------------------------+
```

`GET /api/view` (Erza nis me një `ui/sample_view.json` statik, pa pritur backend-in):
```json
{
  "now": "12:30",
  "health": {"pct": 79, "label": "AT RISK", "critical_protected": "1/2", "violations_blocked": 0},
  "clients": [{"id": "A", "name": "Ditelindje", "starts": "16:00", "zone": "Prishtine",
               "criticality": "CRITICAL", "value_tier": "high", "prepaid": true, "first_time": false, "status": "at_risk"}],
  "workers": [{"id": "e_erioni", "name": "Erioni", "skills": ["driver"], "busy_until": null,
               "free_window": "12:30-23:59", "next_job": null, "status": "free"}],
  "events": [{"id": "A", "slots": [{"id": "A.driver", "role": "driver", "from": "13:30", "to": "16:00", "emp": null, "status": "broken"}]}],
  "chain": {"nodes": [{"id": "e_ardi", "label": "Ardi mungon", "status": "broken"}], "edges": [["e_ardi", "A.driver"]]},
  "escalation": null,
  "offers": []
}
```
`GET /api/events?after=N` → hapat e feed-it. `POST /api/message` → konsola. `POST /api/callback` → butonat (plan B nëse bie Telegram-i).
