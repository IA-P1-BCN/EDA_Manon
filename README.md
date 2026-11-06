# 🎮 Gender Representation in Video Games: an EDA

Exploratory data analysis of how women and men are portrayed in 64 top-selling or top-rated video games (2012–2022). Bootcamp project (Factoría F5 Madrid, IA School). We play the data team of a consultancy; the deliverables are a clean dataset, a documented notebook and a short executive report for a non-technical reader.

📄 **Executive report (3 pages):** [`docs/Women in Video Games What the Data Shows.pdf`](docs/Women%20in%20Video%20Games%20What%20the%20Data%20Shows.pdf)

🎤 **5-minute presentation (8 slides):** [`docs/Women in video games what the data shows.pptx`](docs/Women%20in%20video%20games%20what%20the%20data%20shows.pptx)

🌐 **Live dashboard:** [women-representation-in-videogames-eda.streamlit.app](https://women-representation-in-videogames-eda.streamlit.app/) (the app may need a click to wake up if nobody visited recently)

## 🎯 Questions

1. **Q1.** Are women more sexualized than men, in what ways, and does it depend on the role?
2. **Q2.** What roles do women hold: lead, playable, romantic interest?
3. **Q3.** Good vs. bad: are women allies, antagonists or main villains?

## 🔎 Main findings

All comparisons are women (203) against men (393). Non-binary and custom characters (41) are too few to compare.

- Women are sexualized about **14 times as often as men** (14.3% against 1.0%), in every role tier.
- Women are **34% of characters but 26% of protagonists**; among major characters they reach 37%.
- **75% of women are on the hero's side** and 10% are antagonists (men: 61% and 28%). Women are two thirds of romantic interests.
- Games with women on the team have **more female characters**: 27% with no woman on the team, 41% when women are over a quarter of it (an association, not proof of cause).

⚠️ The games are top-selling or top-rated, so the results describe successful games, not the whole industry. Several groups are small; every percentage is shown with its count.

## 📦 Data

Kaggle dataset [`br33sa/gender-representation-in-video-games`](https://www.kaggle.com/datasets/br33sa/gender-representation-in-video-games) (v3, Brisa Palomar, 2022). The notebook downloads it with `kagglehub`, so an internet connection is needed.

| Table | Shape | Join |
|---|---|---|
| `games` | 64 × 28 | `characters.Game = games.Game_Id` |
| `characters` | 637 × 12 | `characters.Id = sexualization.Id` |
| `sexualization` | 637 × 6 | |

Column meanings: [`docs/data-dictionary.md`](docs/data-dictionary.md).

## 🚀 How to run

```bash
git clone https://github.com/IA-P1-BCN/EDA_Manon.git
cd EDA_Manon
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
```

Open `Gender Representation in Video Games.ipynb` in Jupyter or VS Code, pick the `.venv` kernel and use **Run All**. It was developed with Python 3.14.

**Interactive dashboard**, also [online](https://women-representation-in-videogames-eda.streamlit.app/) (filters by year, genre, country, team and role; every chart shows the counts on hover):

```bash
streamlit run app.py
```

It opens at `http://localhost:8501`. It reads the CSVs in `docs/raw data/` (or downloads them with `kagglehub`) and applies the same cleaning as the notebook (both use `src/cleaning.py`).

**Tests** (32 tests of the cleaning functions, about a second):

```bash
pytest
```

They were written after the functions, except for `validate_tables`, which was built test-first. To check a test can fail, break the function on purpose and run `pytest` again.

**On Google Colab:** the first code cell installs the plotly version pinned in `requirements.txt` (Colab's own plotly draws charts blank). Restart the runtime after it runs.

## 🗂️ Repository

```
├── Gender Representation in Video Games.ipynb   # the analysis, top to bottom
├── app.py                                        # interactive Streamlit dashboard
├── src/cleaning.py                               # reusable cleaning functions (notebook and dashboard)
├── tests/test_cleaning.py                        # pytest tests of src/cleaning.py
├── requirements.txt                              # pinned dependencies
├── CLAUDE.md                                     # working notes for the AI assistant
└── docs/
    ├── Women in Video Games What the Data Shows.pdf   # executive report
    ├── Women in video games what the data shows.pptx  # 5-minute presentation
    ├── data-dictionary.md                        # tables and columns
    ├── data-quality.md                           # what was missing, corrected, still open
    ├── research-questions.md                     # Q1–Q3 and the angles
    ├── notes-for-later.md                        # drafts and loose ends
    ├── Metadata- Gender Representation in Video Games.pdf
    └── raw data/                                 # local copy of the CSVs
```

## 📓 What the notebook does

1. **📥 Data loading:** download, structure and descriptive statistics of the three tables.
2. **🔍 Exploración:** missing values, duplicates, outliers and dubious data (problems are found here and treated in Limpieza).
3. **🧹 Limpieza:** each cleaning choice is written as a `⚖️ Decision / Why`: drop or rename columns, fix types, correct one inconsistent row, and create six new variables (`Is_sexualized`, `Has_female_team`, `Team_group`, `Role_tier`, `Share_women`, `Share_sexualized`).
4. **📊 Análisis:** univariate and bivariate analysis, group summaries, a time trend and a game-level correlation heatmap.
5. **📝 Conclusiones:** the answers to Q1–Q3.

Charts use seaborn by default and plotly where hover helps to read the counts.

## 👤 Author

Manon ([@ManonChab](https://github.com/ManonChab)).
