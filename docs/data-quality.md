# Data quality report — Gender Representation in Video Games

What was missing, what we corrected, and what is still open and why. Evidence lives in the notebook (sections *Exploración* and *Limpieza*); numbers below come from its outputs.

**Scope:** 3 tables, `games` (64 rows), `characters` (637) and `sexualization` (637). Raw tables are never modified; cleaned versions go through the `tables` dict.

**Overall verdict:** the dataset is in good shape. The tables are complete and consistent, with one wrong row. The real limits are not errors but **coverage and subjectivity** (see section 3).

---

## 1. What was missing

| Table | Column | Missing | Meaning |
|---|---|---|---|
| `games` | `Unnamed: 27` | 64 (100%) | Empty column created by a trailing comma at the end of every CSV row. No information. |
| `games` | `Series` | 37 (57.8%) | Not "unknown": the game belongs to no series. |
| `games` | `Destructoid` | 7 (10.9%) | Review score not available for those games. |
| `games` | `IGN`, `GameSpot` | 2 each (3.1%) | Same. |
| `characters` | none | 0 | |
| `sexualization` | none | 0 | |

Other checks that found **nothing**:
- **Duplicates:** 0 duplicated rows in the three tables.
- **Join keys:** every `Id` of `characters` exists in `sexualization` and the reverse (0 orphans).
- **Sexualization score:** the four criteria only take 0 or 1; `Total` equals their sum; `characters.Sexualization` equals `sexualization.Total` for all 637 rows.
- **`Age` vs `Age_range`:** every numeric age falls inside its category (0 mismatches).
- **`Team_percentage`:** matches `Female_team / Total_team` (0 rows off by more than 1 point).

## 2. What was corrected

| Problem | Fix | Why |
|---|---|---|
| `Unnamed: 27` empty | Dropped | No information. |
| `Series` missing (37 games) | Filled with `"Standalone"` | Keeps 58% of games in `groupby` and charts, which ignore NaN. |
| 4 review scores with gaps | Dropped; kept `Avg_Reviews` | `Avg_Reviews` has no gaps and is reliable: 8 games differ by 0.1 from the recomputed mean, always a rounding of a value ending in 5 (the source rounds up, Python rounds down). |
| `Age` mixes numbers (150) and words (487) | Dropped; kept `Age_range` | The words equal `Age_range` and the numbers fall in the right range, so `Age_range` holds the same information for all 637 characters. |
| `Sub-genre`, `Publisher`, `Platform`, `PEGI`, `Criteria` | Dropped | No question or angle (time, team mix, country) uses them. |
| `Release` as text (`"Nov-13"`) | Converted to a date; created `Release_year` | Needed for the time angle. Months mapped with an explicit English dictionary, so it does not depend on the computer's language. |
| `Team_percentage`, `Percentage_non_male` as text (`"11%"`) | Converted to numbers 0–100 | Text cannot be averaged or plotted. |
| Inconsistent names (spaces, hyphens, lowercase start) | Renamed to `Capitalized_with_underscores` | One naming style. Note the raw `"Metacritic "` has a trailing space. |
| **One wrong row:** character `Son` (game PP, a Child) flagged `Damsel_in_distress = 1` | Set to 0; `Total` and `Sexualization` updated | Contradicts the author's own rule (children are not "damsels"). It was one of only 5 men with a score above 0, so it touched the main Q1 comparison (men: 5 → 4 of 393). |
| Outliers flagged by the IQR rule | **Kept, nothing removed or capped** | They are real values (large casts, very balanced teams), not errors. For `Protagonist` and `Sexualization` the IQR is 0, so the flags are a false alarm. |

Variables created to compensate for data shape: `Is_sexualized`, `Has_female_team`, `Team_group`, `Role_tier`, `Share_women`, `Share_sexualized`, `Region`. Each is justified in the notebook as a `⚖️ Decision / Why`.

## 3. What is still open, and why

These are limits of the data or choices that stay open. None can be fixed by cleaning.

| Open point | Why it stays open | What we do about it |
|---|---|---|
| **Selection bias:** games are top-selling or top-rated, 2012–2022 | We have no data on other games. | Every conclusion says "successful games", not "the industry". |
| **Small groups** | 64 games; only 34 of 637 characters have a sexualization score above 0; Non-binary (33) and Custom (8) are too few. | Compare Female vs Male only, compare shares not means, always show `n`, avoid strong claims on subgroups. |
| **Skewed variables** | `Team_percentage` is 0% in 36 of 64 games; 45 of 64 games have no sexualized character. | Compare 0% vs >0%, use medians and Spearman instead of means and Pearson. |
| **Sexualization is a human judgement** | The four criteria were coded by one author. The metadata does not describe how doubtful cases were decided, and we cannot check inter-rater agreement. One error (`Son`) was found among 637 rows, so others are possible. | Treat scores as the author's coding, not an objective measure. |
| **`PA` vs `MC` boundary** | The metadata does not explain how the author separates a protagonist from a main character when a game has no clear lead. | `Role_tier` reports both the strict reading (Lead = `PA`) and the broad one (Major). |
| **`Team_group` cut at 25%** | A choice, not a rule from the data; the last group has only 8 games. | Stated in the notebook; results read as a direction. |
| **`Share_women` / `Share_sexualized` on small casts** | Games have 2 to 27 characters (median 9), so one character moves the share by many points. | Shares shown with `n`. |
| **Yearly trend** | Each year rests on 12 to 38 women and 0 to 8 sexualized women. | 3-year pooled rolling window, raw line shown beside it; it shows a direction only. |
| **`Team_percentage` outliers: kept** (5 games above the 36.9% fence: 43%, 50%, 60%, 67%, 67%) | They are real games with unusually balanced teams, not errors, and the most informative cases for angle B. Removing them would leave 59 games. The IQR rule over-flags here because the box is squashed at 0% (Q1 = median = 0%, Q3 = 14.75%). | Kept in all analyses; we report the median and the 0% vs >0% split instead of the mean. The notebook's *Exploración* cell still says "provisional"; the decision is now confirmed and that word should be removed. |
| **What `Total_team` counts is not defined** | The metadata does not say whether it counts credits, core team or studio. | Not used alone; only as a share (`Team_percentage`). |
