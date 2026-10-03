# scripts — Devlete

> Gjendja 14:40: ⬜ `numbers.py`
> Run-et live i bën Genti në laptopin e tij (aty është çelësi). Ti i nxjerr numrat nga ato.

## `numbers.py`: numrat për prezantimin, nga provat (jo me dorë)
Burimi: `runtime/events.jsonl`, një rresht JSON për çdo hap: `{"n", "t", "type", "text", "detail"}`.
- Rreshtat `type == "reply"` kanë `detail.duration_s`, `detail.model_calls`, `detail.usage` (tokenët).
- `type == "message"` = lideri shkroi · `"sent"` = detyra u dërgua · `"accepted"` = dikush pranoi · `"blocked"` = rregull i bllokuar.

Nxirr:
1. **Sekondat nga mesazhi i liderit te plani** (`detail.duration_s` te `reply`)
2. **Sekondat nga MIRATO te ACCEPT i të gjithëve** (koha `t` e rreshtit "✅ Lideri e miratoi" → koha e "🎉 ... konfirmuar")
3. **Sa kontrolle / refuzime bëri motori** (rreshtat `check` dhe `blocked`)
4. **Kostoja për plan:** nga `usage` me çmimet e Opus 5.5: input $4/MTok, output $20/MTok, cache write $5/MTok ❓, cache read $0.40/MTok ❓ (konfirmoje)

Dalja: `evidence/numbers.md`, me numrat dhe burimin e secilit. Këta janë të vetmit numra "të matur" që hyjnë në slajde.

⏰ 15:30–16:15 (pas run-it final të Gentit në 16:00).
