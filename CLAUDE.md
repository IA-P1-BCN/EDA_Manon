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
- Don't edit the notebook with tools unless explicitly asked. If they ask for a code block, put it in the chat for them to paste.
- Writing docs/config (like this file) is fine when asked.

Notebook conventions already established (match them when suggesting code):
- Language: **English** in the notebook and `docs/`; board issues are in Spanish.
- Sections, in this order: `📥 Carga de datos` → `🔍 Exploración` (find problems only: missing, duplicates, outliers detection, dubious data) → `🧹 Limpieza` → `📊 Análisis` (univariate, bivariate, Q1–Q3 on **clean** data) → Conclusiones (to come). Same order as the Titanic guide. Each section opens with 🎯 Goal / 📥 Input / 🛠️ What we do.
- Every cleaning choice is written as `⚖️ **Decision:** … **Why:** …` in a markdown cell, followed by the code.
- Raw tables stay untouched; cleaned versions go through the `tables` dict (`games`, `characters`, `sexualization`).
- Column naming: `Capitalized_with_underscores` (e.g. `Female_team`, `Damsel_in_distress`). Note the raw `"Metacritic "` column has a **trailing space**.
- Plot defaults: `sns.set_style("whitegrid")`, `figsize=(10, 6)`. Charts need a title, named axes, legend when needed.
- Always show `n` next to percentages (small dataset, small groups).

## 📋 GitHub Project board — keep it in sync

The user asked me to **move tasks as we progress, and to say so every time I do**.

- Board: project **#49**, owner `IA-P1-BCN`. 30 items = issues #1–#30 in `IA-P1-BCN/EDA_Manon`, labeled by level (`Esencial`, `Medio`, `Avanzado`, `Experto`). A `Fase` field (1 Configuración … 6 Conclusiones) also exists.
- Status flow: `Todo` → `In Progress` → `Done`.
- **When to move:** when the user starts a task → In Progress; when they say it's finished or the notebook clearly shows it complete → Done (close the issue too if it isn't auto-closed; Done items on the board are closed issues). If unsure whether a task is truly done, ask rather than assume.
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

- Needs `gh` logged in as `ManonChab` with `project` scope (already the case).
- Task ↔ notebook mapping to watch: #1 load/structure · #2 missing+duplicates · #3 types · #4 drop/rename columns · #11 justify cleaning · #20 dubious data · #5–#7 uni/bi/visuals · #8 answer Q1–Q3 · #9 notebook runs top-to-bottom · #10 README + requirements.

## 🧱 Project facts worth remembering

- Games are top-selling/top-rated 2012–2022 → results describe **successful games**, not the industry.
- Angles B (team mix) and C (country) compare games, so group characters by game first.
- Known data findings so far (see notebook for evidence): `Unnamed: 27` empty column; `Avg_Reviews` reliable (0.1 rounding diffs only); one inconsistent row (character `Son`, game `PP`, a Child flagged `Damsel in Distress`); `Series` NaN means "no series" (→ `"Standalone"`).
- Deliverables outstanding from the brief: executive report (1–2 pages, non-technical), `README.md` (data source, install, how to run), `requirements.txt`.

## ⚙️ Environment

- Python venv in `.venv/` (git-ignored); install with `pip install -r requirements.txt`. Key libs: pandas 3, numpy, matplotlib, seaborn, plotly, missingno, kagglehub, scipy.
- pandas 3 note: convert ints/strings to dates explicitly (`astype(str)` before `pd.to_datetime`).
- Windows + PowerShell/Git Bash. When printing notebook content with emoji from Python, set `PYTHONIOENCODING=utf8`.
- `data/` is empty (raw files moved to `docs/raw data/`); the notebook downloads via `kagglehub`.

## 📝 Git

- Conventional Commits (matches existing history: `feat:`, `chore:`, `docs:`).
- Don't commit or push unless asked. `docs/Markdown_template.md` is intentionally git-ignored.
- Keep commit messages clear and branches ordered — the brief grades Git hygiene.
