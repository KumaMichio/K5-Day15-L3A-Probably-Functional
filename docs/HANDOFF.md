# Handoff — state of the project for the next agent / laptop

> Written 15:05 Friday 27/11/2026 by Claude Code on Hùng's first laptop, when Hùng switched laptops.
> **Read this first, then `CLAUDE.md` (rules) and `plan/index.html` (plan).** Update the "State" section whenever you finish something big, so the next handoff stays true.

## Who you are working for

- **Phan Sỹ Hùng** — team captain of **Probably-Functional** (L3A, AI20K khoá 5), GitHub `KumaMichio`, owner of this repo. He talks to the agent in **English**; team-facing docs are in **Vietnamese**.
- He is one of the two people allowed to merge (with Tân). When he explicitly asks, merging his own PRs with the owner bypass is fine: `gh pr merge <n> --squash --admin --delete-branch`. Never merge without being asked.
- Team (all have accepted the collaborator invite):

| Person | GitHub | Branch prefix | Role |
|---|---|---|---|
| Phan Sỹ Hùng | `KumaMichio` | `hung/` | Captain, builds the prototype, runs evals, submits checkpoints, reviews + merges |
| Dương Thị Huệ | `dhuee10` | `hue/` | Interviews, pain evidence, slides, user testing |
| Dương Minh Tân | `mihtan05` | `tan/` | Data mining, lesson data + tools, impact, cost; reviews + merges |
| Nguyễn Bá Thành | `Nguyen-Ba-Thanh` | `thanh/` | Hard cases, metrics, pass standard, benchmark, eval report |

## What the project is

- **Hackathon brief:** https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon — read `README.md`, `02-guide.md`, `03-rubric.md`, `tracks/track-a-edtech.md`. Clone it next to this repo.
- **Our choice:** Track A (EdTech), direction **A1, option 1** — improve one thing the existing pre-class AI tutor does poorly.
- **Slice:** *Một học viên L3 · hỏi một câu dưới video pre-class · AI quyết định trả lời kèm mã đoạn bài hay nói "không có trong bài" · học viên tự kiểm được bằng cách mở đúng đoạn.*
- **Planned design (spec §4, not written yet):** fixed workflow, not an agent: search lesson passages → if a relevant passage exists, the model answers citing passage codes; if not, answer "không có trong bài" without calling the model. Code checks every cited code exists. User text is data, not instructions. No doing homework / leaking quiz answers.
- **Shared contract (lets Hùng and Tân work in parallel):**
  ```
  data/lessons/<bai>.json = {"lesson_id", "title", "video", "passages": [{"code": "D05-L2-P03", "text": "…"}]}
  codebase/tools.py: search_lesson(query, k=3) -> [{"code","text","score"}]  ([] if nothing)
                     get_passage(code) -> {"code","text"} | None
  ```
- **Model (not connected yet):** a small tier for building — Gemini free tier (`gemini-3.1-flash-lite`) or Claude Haiku 5.5 / gpt-5-nano with a few dollars. For the cost table: price the same measured tokens at a small and a large tier (e.g. Haiku 5.5 + Sonnet 5.5), from the brief's `further-reading/model-prices.md`. Avoid gemini-4-argon, gemini-3.8-flash at old price, gemini-2.5-*, gpt-5.6-sol (price changes / deprecated).

## Evidence so far (from `evidence/data-mining.md`, script `evidence/scripts/count_preclass.py`)

- 145/436 active learners (33.3%) ever messaged the AI; 1,090 questions under videos to the tutor (05–25/11).
- 98/1,075 (9.1%) tutor replies flagged `missing_context`; **97/98 still answered at length**.
- 231/557 (41.5%) replies cite no timestamp in the lesson (field exists from 13/11).
- 530/1,090 (48.6%) re-ask or rewind within 2–3 min — weak signal, needs interviews.
- Per-learner question counts (for cost personas): 1 q: 38 · 2–5: 46 · 6–15: 43 · ≥16: 16 (median 4).

## Repo and GitHub setup (done)

- `main` is protected: PR required, 1 approval from a Code Owner (`.github/CODEOWNERS` = `@KumaMichio @mihtan05`), linear history, no force push. Owner can bypass.
- Squash merge only; head branches auto-deleted.
- **15 open issues = 15 tasks** (#2 #5 #8 #11 #12 #14 #24 #25 #26 #27 #32 #33 #36 #38 #41), with milestones CP1–CP4 + Hạn chót, labels `người: <tên>`, assignees. 28 smaller issues were closed as "not planned" with a "Gộp vào #x" comment. #1 and #5 are done.
- Only 5 hard "blocked by" links: #25←#8, #27←#11,#24, #32←#27, #33←#27. Everything else starts now and updates later.
- **Plan page:** `plan/index.html`, also published as a Claude artifact (Hùng's claude.ai account, shared "anyone with the link"): https://claude.ai/artifact/JotqHaozppmQnajHGJYRws . To update it from another session, edit `plan/index.html` and publish with the Artifact tool passing that `url` (read it first). The page cannot fetch GitHub live, so its "Tình trạng" box is a dated snapshot — refresh `SNAPSHOT`, `STATUS`, `MERGED`, `PRS`, `NEXT_UP` in the script.

## Schedule (internal deadlines, earlier than official)

| When | Done |
|---|---|
| 17:00 Fri | **CP1** (official 17:00) |
| 19:30 Fri | **CP2** (official 19:30): interviews, hard cases + metrics + 10 test cases + pass standard (**locked after 19:30**), spec §4 diagram, fake-mode skeleton, DATA_CARD |
| 23:30 Fri | **Submit CP3 tonight** (official 10:00 Sat): real model + guards, 20–30 cases, evidence summary, impact, run 1, 30-s video |
| 00:30 Sat | Read failures, one improvement, run 2, 50-session simulation |
| 13:45 Sat | **Submit CP4** (official 14:30): eval report, cost estimate, slides PDF, backup video, rehearsal. Enter room 14:00, demo 14:30 |
| 23:59 Sat | Final: changelog, reflections, lock repo |

Critical path: #11 → #27 → #32 → #26 → #2. Hùng owns most of it; Tân has a backup API key role.

## State at handoff (15:05 Fri 27/11)

- `main` = `1c9580e`. PRs #45, #46, #47 merged. No open PRs, no other branches.
- **CP1 not yet submitted** — everything required is on main (TEAMS.md, canvas.md, public repo). Paste-ready text: Track A; problem = canvas line 3; slice = canvas line 5; links to `canvas.md` and the repo. Submit with student ID 2A202603420, then tick it in #2.
- Not started: #8, #11, #12, #14 and everything after.
- Small loose ends: Tân to fill the `__ dòng khác` line in `evidence/data-mining.md`; canvas line 4 and `spec.md` §1–§2 still say 8.1% (should be 9.1% = 98/1,075) — part of #26.

## Setting up the new laptop

1. `git clone https://github.com/KumaMichio/K5-Day15-L3A-Probably-Functional.git` and `git clone https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon.git` side by side.
2. `git config user.name "Phan Sỹ Hùng"` (and his email) inside the repo.
3. Python ≥ 3.10; no pip install needed. Check: `python run.py check`.
4. Organizer data (not in git): copy `K5-L3-Day15-AI-Product-Hackathon/data/preclass` to `K5-Day15-L3A-Probably-Functional/data-btc/preclass`. Then `python evidence/scripts/count_preclass.py data-btc/preclass` should print the numbers above.
5. GitHub CLI: install (`winget install GitHub.cli` on Windows), then Hùng runs `gh auth login` himself (browser login). On Windows Git Bash, gh may need `export PATH="$PATH:/c/Program Files/GitHub CLI"`.
6. `.env` does not exist yet — create from `.env.example` when connecting the model (#11). Never commit it.

## Things that are only on the old laptop (not needed)

- `D:\Vin_Hackathon\drafts-trackA-A1\` — old Track A drafts, already merged into the repo.
- Scratch scripts that created/consolidated the issues and dependency links (GitHub REST via `gh auth token`). Recreate with `gh` if needed: issue dependencies are `POST /repos/{owner}/{repo}/issues/{n}/dependencies/blocked_by` with `{"issue_id": <id of blocking issue>}`.
