# ui — Erza

> Gjendja 14:40: ✅ `sample_view.json` (nga një run i vërtetë) · ⬜ `index.html` · ⬜ `style.css` · ⬜ `app.js`
> **S'të duhet çelës dhe s'të duhet server.** Ti e ndërton faqen me `sample_view.json`; Genti dhe Claude e lidhin me agjentin.

## Hapat
```bash
git clone https://github.com/VocaDev/hi5-team-leader.git
cd hi5-team-leader
git checkout erza/ui
```
Puno vetëm këtu: `ui/index.html`, `ui/style.css`, `ui/app.js`. Te `app.js` lexo: `fetch("sample_view.json")`.

## Çka shfaq faqja (një ekran, dark navy glass, pa neon, pa CDN)
| Pjesa | Nga `sample_view.json` |
|---|---|
| Kutia ku lideri shkruan + **Dërgo** | → `sendMessage(text)` |
| "Agjenti po mendon…" | kur `busy == true` |
| **Plani**: titulli, zona, ora, statusi, përmbledhja | `job.title`, `job.zone`, `job.start`, `job.status`, `job.summary` |
| **Detyrat**: roli, kush, ora, çka merr me vete, shënimi, statusi | `tasks[]`: `role`, `worker`, `from`–`to`, `bring[]`, `note`, `status` (`planned` / `sent` / `accepted` ✅ / `declined` ❌) |
| Butoni i madh **MIRATO** | vetëm kur `job.status == "awaiting_approval"` → `approve()` |
| Te çdo detyrë `sent`: **ACCEPT** / **S'MUNDEM** | → `answer(task.id, "accept" \| "decline")` |
| **Si mendon agjenti** (feed live, më i riu poshtë) | `feed[]`: `t`, `type`, `text`. Ngjyrat: `blocked` e kuqe · `accepted` jeshile · `check` gri · `tool` blu · `message`/`reply` e bardhë |
| Shiriti i kuq | `blocked[].text` |
| Punëtorët | `workers[]`: `name`, `skills`, `status` (`free` / `busy` / `assigned`) |
| Punët ekzistuese të ditës | `existing_jobs[]`: `title`, `zone`, `from`–`to`, `workers` |
| Butoni **Reset** (i vogël) | → `reset()` |

## Funksionet: lëri bosh, Claude i lidh
```js
function sendMessage(text) {}
function approve() {}
function answer(taskId, action) {}   // "accept" | "decline"
function reset() {}
```
Rifreskimi: një funksion `render(view)` që e vizaton gjithë faqen nga JSON-i. Kështu lidhja live bëhet duke e thirrur `render` çdo 1 sekondë.

## Afatet
Versioni i parë **15:00** → `git add ui/` → `git commit -m "ui"` → `git push` → Pull Request. Finali **15:45**. Freeze **16:00**.
