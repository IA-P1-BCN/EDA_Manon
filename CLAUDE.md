# CLAUDE.md — EDA: Gender Representation in Video Games

Project-specific guidance. Global defaults live in `~/.claude/CLAUDE.md`; this file takes precedence where they differ.

## 🎯 What this project is

A bootcamp (Factoría F5 Madrid, IA School) **EDA project**. Framing: we are the data team of a consultancy; the client's CEO doesn't read code, so the deliverable is clean data plus a clear story and an executive report.

- **Dataset:** Kaggle `br33sa/gender-representation-in-video-games` (v3, Brisa Palomar, 2022). 3 tables: `games` (64×28), `characters` (637×12), `sexualization` (637×6). Joins: `characters.Game = games.Game_Id`, `characters.Id = sexualization.Id`.
- **Main file:** `Gender Representation in Video Games.ipynb` (the notebook the user is actively working in).
- **Deadline:** one week from the brief. Target level: all 4 levels are on the board (Esencial → Medio → Avanzado → Experto); "one level done well beats two half-done".

### Sources of truth

| What | Where |
|---|---|
| Original brief (levels, deliverables) | https://github.com/Factoria-F5-madrid/ai_project_EDA |
| This repo | https://github.com/IA-P1-BCN/EDA_Manon (`origin`, branch `main`) |
| Task board | https://github.com/orgs/IA-P1-BCN/projects/49 ("EDA_Manon") |
| Step-by-step reference exercise (Titanic) | https://github.com/Factoria-F5-madrid/AI-Workshop-EDA/blob/main/titanic_eda_ejercicio.ipynb |
| Research questions Q1–Q3 + angles A/B/C | `docs/research-questions.md` |
| Column meanings, tables, relationships | `docs/data-dictionary.md` |
| Official dataset metadata | `docs/Metadata- Gender Representation in Video Games.pdf` |
| Raw CSVs (local copy) | `docs/raw data/` |

Each board issue (#1–#30) already has a "🧭 Guía paso a paso" section that maps to a Titanic-notebook step (Pasos 0–10). Read the issue before helping with its task.

## 🤝 How we work (important)

**The user does the work themselves.** They are learning; this is their project.

- Default to **guiding, not doing**. Do not write or edit notebook cells, run analyses, or "just finish" a step unprompted.
- Give a **code block, hint, or analysis help only when asked**. Keep it minimal and aimed at the step they're on; explain *why*, not just *what*.
- When asked to help analyse a result, read their output and discuss it; let them write the conclusion in their own words.
- Don't jump ahead to later sections or levels. Don't refactor or "improve" their notebook cells uninvited.
- **Never edit the notebook file by default.** "Do X", "let's do #14" or "add these variables" means: give the code (and the markdown wording) in the chat, tested on the data, for them to paste and build around. Only edit the file when they say so in so many words ("edit the notebook", "write it in the file"); if unsure, ask. Then follow "Editing the notebook file" below.
- Test any code I hand over on the data first (see Environment), and give a short "how to read it" with the numbers and `n`.
- Writing docs/config (like this file) is fine when asked.
- `docs/notes-for-later.md` is where drafts, loose ends and draft answers to Q1–Q3 are kept. Read it at the start of a session.

### Editing the notebook file

The user's editor overwrote my edits three times (it saves its own stale copy over the file). So:
1. Ask them to **save and close the notebook tab** first, and wait for "it's closed".
2. Copy the file to the scratchpad as a backup, then re-read it (they edit it between turns).
3. Edit the JSON with a script (find cells by content, not by index), clear the outputs of the cells I changed, keep the other cells and the formatting (`indent=1`, `ensure_ascii=False`).
4. Run the notebook's code from a script on `.venv` to check it (all cells must run), without modifying their file.
5. Tell them to reopen it and run Restart & Run All, then save. If their editor shows a conflict dialog, **Revert** keeps my changes and **Overwrite** loses them.

Notebook conventions already established (match them when suggesting code):
- Language: **English** in the notebook and `docs/`; board issues are in Spanish.
- Sections, in this order: `📥 Carga de datos` → `🔍 Exploración` (find problems only: missing, duplicates, outliers detection, dubious data) → `🧹 Limpieza` → `📊 Análisis` (univariate, bivariate, Q1–Q3 on **clean** data) → Conclusiones (to come). Same order as the Titanic guide. Each section opens with 🎯 Goal / 📥 Input / 🛠️ What we do.
- Every cleaning choice is written as `⚖️ **Decision:** … **Why:** …` in a markdown cell, followed by the code.
- Raw tables stay untouched; cleaned versions go through the `tables` dict (`games`, `characters`, `sexualization`).
- Column naming: `Capitalized_with_underscores` (e.g. `Female_team`, `Damsel_in_distress`). Note the raw `"Metacritic "` column has a **trailing space**.
- Plot defaults: `sns.set_style("whitegrid")`, `figsize=(10, 6)`. Charts need a title, named axes, legend when needed.
- **Seaborn is the base; plotly only where hover helps** (e.g. showing `n` on small groups). Seaborn renders everywhere (GitHub preview, report export); plotly charts can show blank in GitHub's viewer and need `kaleido` to export. Plotly charts also need a title and named axes.
- Always show `n` next to percentages (small dataset, small groups).
- Put a heading above every table: `display(Markdown("**…**"))` before `display(df)`, so the reader knows what each table is. Compact tables for reading use "x / n (p%)" text; keep a numeric version for charts.
- Gender comparisons use Female vs Male only (Non-binary n=33 and Custom n=8 are too small); say so in the notebook.
- Say whether the unit is the **character** or the **game** (angles A/B/C compare games, so group by game first; sexualization counts are per character).
- Cleaning cells read and write `tables["games"]` / `tables["characters"]` (never the old `games` variable), so dropped columns stay dropped.

## 📋 GitHub Project board — keep it in sync

The user asked me to **move tasks as we progress, and to say so every time I do**.

- Board: project **#49**, owner `IA-P1-BCN`. 30 items = issues #1–#30 in `IA-P1-BCN/EDA_Manon`, labeled by level (`Esencial`, `Medio`, `Avanzado`, `Experto`). A `Fase` field (1 Configuración … 6 Conclusiones) also exists.
- Status flow: `Todo` → `In Progress` → `Done`.
- **When to move:** when the user starts a task → In Progress; when they say it's finished or the notebook clearly shows it complete → Done (the issue closes by itself when the card goes to Done). If unsure whether a task is truly done, ask rather than assume.
- **Always announce it**, e.g. "Moved #3 *Corregir tipos de datos* → In Progress."
- Check the current state first (statuses change between sessions):

```bash
gh project item-list 49 --owner IA-P1-BCN --limit 50 --format json
```

- Move an item (need the item's project ID from the list above):

```bash
gh project item-edit --project-id PVT_kwDOE6KzAs4BqIn4 --id <ITEM_ID> \
  --field-id PVTSSF_lADOE6KzAs4BqIn4zhohDto --single-select-option-id <OPTION_ID>
```

| Status | Option ID |
|---|---|
| Todo | `f75ad846` |
| In Progress | `47fc9ee4` |
| Done | `98236657` |

- Needs `gh` logged in as `ManonChab` with the `project` scope. If `gh auth status` says the token is invalid (it happened once), ask the user to run `! gh auth login --scopes project,read:org,repo,workflow` (interactive, I can't do it).
- On Windows, `python` can't read bash `/tmp` paths: save the item list in the scratchpad and pass that path.
- Task ↔ notebook mapping to watch: #1 load/structure · #2 missing+duplicates · #3 types · #4 drop/rename columns · #11 justify cleaning · #12 outliers · #13 groupby/agg/pivot_table · #16 trends over time · #20 dubious data · #5–#7 uni/bi/visuals · #8 answer Q1–Q3 · #9 notebook runs top-to-bottom · #10 README + requirements.
- The issues' "🧭 Guía paso a paso" texts mix Titanic steps, brief requirements and suggestions; I corrected the ones that contradicted the project. Treat them as hints, not rules.

## 🧱 Project facts worth remembering

- Games are top-selling/top-rated 2012–2022 → results describe **successful games**, not the industry.
- Angles B (team mix) and C (country) compare games, so group characters by game first.
- Known data findings so far (see notebook for evidence): `Unnamed: 27` empty column; `Avg_Reviews` reliable (0.1 rounding diffs only); one inconsistent row (character `PP_Son`, a Child flagged `Damsel_in_distress`, corrected in Limpieza); `Series` NaN means "no series" (→ `"Standalone"`); `Age` is dropped (words equal `Age_range`, numbers fall in the right range); `Team_percentage` is 0% in 36 of 64 games (skewed, compare 0% vs >0%); only 34 of 637 characters have a sexualization score above 0, so compare shares, not means; outliers are kept (real values, IQR is 0 for `Protagonist` and `Sexualization`).
- **`README.md` is a living document.** Whenever a task changes the results, the setup, the file structure or the deliverables, update `README.md` (and `requirements.txt` if a library was added) in the same work session, and say so. Same for the notebook: boards #9 (notebook runs top to bottom) and #10 (README + requirements) stay **In Progress** on purpose, because they must hold true as the project grows. Before each commit, run the notebook's code from a script and check it has no errors.
- Deliverables: the executive report is done (`docs/Women in Video Games What the Data Shows.pdf`, 3 pages, 4 findings + recommendations for studios, written in Claude Docs and exported; audience = an advocacy organisation like Women in Games, no screenshots of game characters). `README.md` has a first version (data source, install, how to run, findings, structure); keep it current as above.

## ⚙️ Environment

- Python venv in `.venv/` (git-ignored); install with `pip install -r requirements.txt`. Key libs: pandas 3, numpy, matplotlib, seaborn, plotly, missingno, kagglehub, scipy.
- pandas 3 note: convert ints/strings to dates explicitly (`astype(str)` before `pd.to_datetime`).
- Windows + PowerShell/Git Bash. When printing notebook content with emoji from Python, set `PYTHONIOENCODING=utf8`.
- `data/` is empty (raw files moved to `docs/raw data/`); the notebook downloads via `kagglehub`.
- Kernel: the user sometimes runs the notebook on Colab, which drops sessions or runs out of free quota ("notebook controller is DISPOSED" = dead kernel, not a code bug). The local `.venv` kernel is the reliable one.
- **Colab ships plotly 5.24.1, which draws plotly charts blank** (frame and hover work, nothing drawn, even a minimal `px.bar`). Fix: `%pip install -q plotly==7.1.0` (the `requirements.txt` pin) before any import, then restart the runtime. It does not persist between Colab sessions.
- To check the notebook without their kernel: run its code cells in a script with `.venv/Scripts/python.exe` (matplotlib `Agg` backend); keep the script in the scratchpad.

## 📝 Git

- Conventional Commits (matches existing history: `feat:`, `chore:`, `docs:`).
- Don't commit or push unless asked. `docs/Markdown_template.md` is intentionally git-ignored.
- Keep commit messages clear and branches ordered — the brief grades Git hygiene.
