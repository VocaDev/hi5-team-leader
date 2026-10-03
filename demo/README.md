# demo — Erza + Tringa (skenarin e shkruani ju)

> Demoja është **live, me tekst të lirë**. Agjenti s'ka përgjigje të gatshme. E përgatitur është vetëm bota (kompania, njerëzit, punët e ditës).

## Rolet (6 veta)
| Kush | Roli | Pajisja |
|---|---|---|
| ? | **Lideri**: flet me "klientin", pastaj i shkruan agjentit | laptopi (ekrani) ose Telegram |
| ? × 4 | **Punëtorët**: marrin detyrat, shtypin ACCEPT / S'MUNDEM | telefonat (Telegram) |
| Genti | tregon çka po ndodh në ekran | — |

## Rrjedha (~2 min)
1. Lideri e shkruan punën me fjalët e veta (p.sh. ditëlindje, ora, vendi, shërbimet)
2. Ekrani: "si mendon agjenti", përfshirë konfliktin që e kap (dikush s'arrin në kohë / vani i zënë)
3. Plani → **MIRATO**
4. 4 telefona marrin detyrat në detaje → ACCEPT
5. Njëri shtyp **S'MUNDEM** → detyra kalon te tjetri, lideri njoftohet
6. *(opsional)* lideri: "vendose X gjithsesi" → **BLOCKED**

## Checklist para demos
- [ ] `POST /api/reset` (butoni Reset)
- [ ] 5 telefonat e kanë dërguar `/start` te bot-i dhe janë te `TELEGRAM_IDENTITY_MAP` (Genti)
- [ ] hotspot nga telefoni (jo Wi-Fi i sallës)
- [ ] video rezervë nga run-i i 16:00
- [ ] plan B: butonat ACCEPT / S'MUNDEM në ekran (pa Telegram)
