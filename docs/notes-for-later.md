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

## 5. Draft answers to Q1–Q3 (to place in the final answers, not in the bivariate cells)

Collected from the bivariate analysis. Numbers use the cleaned data (`PP_Son` corrected). Women and men only: Non-binary (33) and Custom (8) are left out of these comparisons, and the notebook should say so. These are drafts: confirm each number against the notebook outputs before writing the final answer. Always show `n`, and remember the games are top-selling or top-rated, so the results describe successful games.

### Q1. How much more are women sexualized than men, in what ways, and does it depend on the role?

- **How much (answered so far):** 29 of 203 women (14.3%) have a score above 0, against 4 of 393 men (1.0%). That is about 14 times higher. Before the `PP_Son` fix it was 5 men (1.3%), about 11 times.
- **Context:** only 34 of the 637 characters have a score above 0 (603 score 0), and nobody scores 4. The mean is misleading, so compare the share above 0. One Non-binary character is sexualized, and no Custom one.
- **Still to do:**
  - *In what ways:* rate of each of the four criteria (clothing, trophy, damsel, cutscenes) by gender, to see which one drives the gap.
  - *Does it depend on the role:* repeat the comparison by `Relevance`, `Side`, `Age_range` and `Species`. Groups will be very small (only 33 sexualized women and men in total), so show `n` and avoid strong claims.

### Q2. What roles do women hold: lead, playable, romantic interest?

- **Roles (answered so far):** women are about 32% of characters but only 26.2% of protagonists (16 of 61) and 22.4% of main antagonists (11 of 49 women and men).
- **Where women are well represented:** main characters (39.4%, 78 of 198), deuteragonists (44.4%, 8 of 18) and sidekicks (46.2%, 6 of 13). The last two are small groups.
- **Within each gender:** 7.9% of women are protagonists against 11.5% of men; 38.4% of women are main characters against 30.5% of men; 41.4% against 44.0% are secondary characters.
- **Not yet in the notebook (computed for these notes, to confirm):**
  - *Playable:* 33 of 203 women (16.3%) against 72 of 393 men (18.3%), so the shares are close.
  - *Romantic interest:* 31 of 203 women (15.3%; 14 `Yes` and 17 `Opt`) against 16 of 393 men (4.1%; 3 `Yes` and 13 `Opt`).
- **Decision to make:** which definition of "lead" to use (see section 4): `PA` only, or `PA` + `DA` + `MC`.

### Q3. Good vs. bad: are women allies, antagonists or main villains?

- **Side (answered so far):** 75.4% of women are on the protagonist's side, against 61.3% of men.
- **Antagonists:** 9.9% of women (20) against 27.7% of men (109). Women are only 15.5% of all antagonists, although they are 32% of the characters.
- **Both sides:** 14.8% of women against 10.9% of men; women are 41.1% of this group (30 of 73). It is small, so read it with caution.
- **Main villains:** 22.4% of the female and male main antagonists are women (11 of 49). With all 53 main antagonists, it is 11 of 53 (20.8%).
- **Still to do:** sexualization by side is covered in Q1.

---

## 6. Other loose ends

- **Stale comment in the notebook:** the Findings under *Gender & Sexualization* say women are "roughly 11 times" more sexualized. That was before the `PP_Son` fix. With 4 men (1.0%) instead of 5 (1.3%), it is about 14 times.
- Done: `Team_percentage` is now converted to float in *Limpieza* (board #3), and the analysis cell uses it directly. Its leftover comment `# Convert "11%" -> 11.0` and the duplicate `games = tables["games"]` line can be deleted.
- `Genre` has tiny groups (Simulation n=1, Interactive Story n=4). Decide later whether to group them as "Other" or leave them out of genre comparisons.
- `Gender`: Non-binary (33) and Custom (8) are small. Decide later whether to show them separately or note them aside in Q1–Q3.
