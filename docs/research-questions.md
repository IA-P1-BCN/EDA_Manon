# EDA — Women in video games: questions to answer

Questions we set ourselves **before** looking at the data (project task #8). Each one is mapped to the columns that can answer it. Column meanings: see [`data-dictionary.md`](data-dictionary.md).

**Tables:** `games` (G), `characters` (C), `sexualization` (S).
Joins: `C.Game = G.Game_Id` · `C.Id = S.Id`.

## Selected questions to lead the EDA

| # | Question | Why it works |
|---|---|---|
| **Q1** | How many women are sexualized? | The core of the project. 637 characters, a 0–4 score and 4 separate criteria. We can compare women and men directly and see which criterion (clothing, cutscenes, trophy, damsel) drives the gap. |
| **Q2** | What roles do women hold: lead, playable, romantic interest? | A clear comparison: Gender × Playable × Relevance × Romantic_Interest. Large enough sample, and easy for a non-technical CEO to read. |
| **Q3** | Good vs. bad: are women allies, antagonists or main villains? | Gender × Side (and Relevance) is a clean 637-row comparison. Also: does sexualization differ by side? |

### Angles that can be added to each question

Each of Q1–Q3 can be re-read through these three lenses:

| Angle | Question | Columns |
|---|---|---|
| **A. Time** | Has it changed over time (2012–2022)? | `G.Release` (year) |
| **B. Team mix** | Does the team's gender mix change what is shown? | `G.Team_percentage`, `G.female_team`, `G.Total_team` against the characters' results (merge on `Id`, group by game) |
| **C. Country** | Does the developer's country have an influence? | `G.Country` (group into regions if countries have very few games) |

---

## Q1. How many women are sexualized?

- **Columns:** `C.Gender`, `C.Sexualization` (0–4), `S.Total`, and the four criteria in `S` (`Sexualized_clothing`, `Trophy`, `Damsel in Distress`, `Sexualized Cutscenes`).
- **Approach:** share of characters with a score above 0, by gender; which criterion is the most frequent; check that `C.Sexualization` equals `S.Total`.
- **Chart:** bar chart of mean score by `Gender`; bars per criterion.
- **Add-on angles:** A (score by release year) · B (`Team_percentage` vs mean score per game) · C (mean score by country).
- **Answer:** *(to fill in)*

## Q2. What roles do women hold: lead, playable, romantic interest?

- **Columns:** `C.Gender`, `C.Playable`, `C.Relevance` (`PA` protagonist, `DA`, `SK`, `MC`, `SC`, `MA`), `C.Romantic_Interest` (`No` / `Yes` / `Opt`); `G.Protagonist`, `G.Protagonist_Non_Male`.
- **Approach:** share of women among playable characters and among protagonists; distribution of `Relevance` by gender (main or secondary?); share with `No` vs `Yes`/`Opt` romantic interest. Always compare with men. `Protagonist_Non_Male` also counts non-binary and customizable characters.
- **Chart:** bar chart of gender share among protagonists / playable; stacked bar of `Relevance` and of `Romantic_Interest` by `Gender`.
- **Add-on angles:** A (female protagonists per year) · B (`Team_percentage` vs `Protagonist_Non_Male`) · C (by country).
- **Answer:** *(to fill in)*

## Q3. Good vs. bad: are women allies, antagonists or main villains?

- **Columns:** `C.Side` (`P` protagonist's side / `A` antagonist / `B` both), `C.Relevance` (`MA` main antagonist), `C.Gender`, `S.Total`.
- **Approach:** share of women among protagonists' allies vs antagonists; share of main antagonists who are women; compare sexualization between sides.
- **Chart:** stacked bar of `Gender` by `Side`; bar of mean sexualization by `Side` and `Gender`.
- **Add-on angles:** A (women villains per year) · B (`Team_percentage` vs share of female antagonists) · C (by country).
- **Answer:** *(to fill in)*

---

## Also considered (not selected)

Kept as optional side notes if time allows.

| Question | Why it was not selected |
|---|---|
| Does the developer's country have an influence? | Now an add-on angle (C) of Q1–Q3. 64 games across many countries: group by region and show `n`. |
| Women developers vs. male developers (+ % of women in the team) | Team percentage is now add-on angle B. The director's gender is dropped: possibly very few female directors. |
| Do games with female leads get better scores? (`Metacritic`, `Avg_Reviews`) | Scores depend on many other factors, and 64 games give noisy results. |
| Custom gender: when, who, which country, which score? | Probably only a handful of games: more descriptive than analytical. |
| Does species or age influence sexualization? (`Species`, `Age_range` vs `S.Total`) | Interesting, but several groups are small. Good candidate to add to Q1 as a breakdown. |

---

## Notes and limits

- The dataset is small (64 games, 637 characters): report counts (`n`) next to every percentage, and avoid strong claims on small groups.
- Games were selected as top-selling or top-rated, so results describe **successful games**, not the whole industry.
- Angles B and C compare games, so characters must be grouped by game first (otherwise games with many characters weigh more).
