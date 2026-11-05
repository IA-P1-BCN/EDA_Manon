# Notes for later

Things found along the way that we want to come back to. Not final: each note says where it belongs.

---

## 1. Outliers: draft for the notebook section `## 5. Outliers` (board #12)

Status: draft from the univariate analysis (#5). To complete: IQR on every numeric variable, final decisions.

### Team_percentage (share of women in the development team)

- **Method:** IQR rule on the boxplot. A value is an outlier if it lies outside `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`.
- **Findings:**
  - Q1 = 0%, median = 0%, Q3 = 14.75%, so IQR = 14.75 and the upper fence is about 36.9%.
  - 5 of the 64 games lie above it: 43%, 50%, 60% and two at 67%.
  - The distribution is strongly right-skewed (skewness ≈ 1.9): 36 of the 64 games (56%) have exactly 0% women in the team, and the mean (10.7%) is far above the median (0%).
- **Decision (provisional):** keep the 5 outlier games.
  **Why:** they are not data errors. They are real games with unusually balanced teams, and they are the most interesting cases for the team-mix question. Removing them would also leave only 59 games in an already small dataset.
- **Caution:** because the box is squashed at 0, the IQR rule flags a lot relative to the typical value. The mean is misleading here, so use the median.

### Avg_Reviews

*(to fill in: outliers seen on the boxplot, and decision)*

### To revisit

- Check the other numeric variables (`Total_team`, `Protagonist`, `Percentage_non_male`, `Age`...).
- Confirm the decision on `Team_percentage` once angle B has been run.

---

## 2. Angle B (team mix) and the skew of `Team_percentage`

Belongs to: angle B of Q1–Q3 in `research-questions.md`.

`Team_percentage` is heavily skewed. 36 of the 64 games (56%) have exactly 0% women in the team, and the median is 0%. Correlating or averaging the raw percentage is therefore misleading.

Instead, compare two groups: games with **0%** vs games with **>0%** (n = 36 vs 28), and show `n` for both. If the >0% group is still informative, it can be split further (for example 1–25% and >25%).

---

## 3. Feature engineering idea (board #14)

Candidates for the 3 new variables required at the Medio level:

- `Has_female_team` (True/False, from `Team_percentage > 0`). It comes directly from note 2.
- `Is_sexualized` (True/False, from `Sexualization > 0`). In `characters`, 602 of 637 characters score 0 (94.5%) and only 35 score above 0, with a maximum of 3 (nobody scores 4). Means are therefore misleading, and "share of characters with a score above 0" is a more robust way to compare women and men in Q1. Always show `n`.

---

## 4. Role definitions: Protagonist (PA) vs Main character (MC)

Belongs to: Q2 and Q3 in `research-questions.md`. Definitions come from the official metadata PDF.

- **PA** = the most important person(s) in the game. **MC** = relevant throughout most of the story, but not the protagonist; this category can include antagonists.
- **Q2** asks about "lead" roles for women. If you count only PA, you get the strictest definition: protagonists. If you count PA + DA + MC, you get a broader "major characters" group. Pick one on purpose and say so in the notebook.
- **Q3** uses MA (main antagonists). Remember that antagonists can also be MC or SC. So "women who are villains" is better measured with `Side` (A), and "women who are main villains" with `Relevance` (MA).
- **Limit:** the PDF doesn't explain how the author decides between PA and MC when a game has no clear lead. Keep this in mind for the analysis.

---

## 5. Other loose ends

- `Team_percentage` is stored as text with a "%" sign (`"11%"`). Convert it to float in the cleaning section (board #3). For now the univariate cell converts it locally with `.str.rstrip("%").astype(float)`.
- `Genre` has tiny groups (Simulation n=1, Interactive Story n=4). Decide later whether to group them as "Other" or leave them out of genre comparisons.
- `Gender`: Non-binary (33) and Custom (8) are small. Decide later whether to show them separately or note them aside in Q1–Q3.
