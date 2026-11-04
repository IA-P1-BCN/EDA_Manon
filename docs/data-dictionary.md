# Data dictionary — Gender Representation in Video Games

Source: Kaggle `br33sa/gender-representation-in-video-games` (v3), dataset by **Brisa Palomar**, November 2022.
Based on the official metadata PDF (`Metadata- Gender Representation in Video Games.pdf`, 4 pages) and on what we observed in the loaded CSVs.

## 1. Overview

Video games released **2012–2022**, with their characters, to analyze how genders are represented.

**Game selection criteria**
1. The game must have a storyline with characters that have an assigned role (excludes puzzle, racing, social simulators, MMORPGs, shooters without story mode, sandbox games without plot such as Minecraft / Roblox / LoL).
2. For games with story + multiplayer, only the **story mode** is analyzed.
3. Games are top-selling or best-rated of their year.
4. At least 5 games per year.

**Sources:** Metacritic, Destructoid, IGN, GameSpot, Wikipedia, developer / publisher / game websites.

**Contributions / contact:** brisadataanalytics (at) gmail.com

## 2. Tables and relationships

| File | Rows × cols (observed) | One row = |
|---|---|---|
| `games.grivg.csv` | 64 × 28 | a game |
| `characters.grivg.csv` | 637 × 12 | a story-relevant character |
| `sexualization.grivg.csv` | 637 × 6 | the sexualization rating of one character |

```
games.Game_Id  1 ──── N  characters.Game
characters.Id  1 ──── 1  sexualization.Id
```

## 3. `games`

| Column | Type (doc) | Description |
|---|---|---|
| `Game_Id` | str, **PK** | Unique code identifying the game (e.g. `GTAV`) |
| `Title` | str | Game title |
| `Release` | date | Date of first release |
| `Series` | str | Series the game belongs to, if any |
| `Genre` | str | Main genre |
| `Sub-genre` | str | Main subgenre |
| `Developer` | str | Game developer |
| `Publisher` | str | Game publisher |
| `Country` | str | Country of the developer |
| `Platform` | str | Original platform(s) only (later ports are not noted) |
| `PEGI` | int | Pan-European Game Information rating (minimum recommended age) |
| `Customizable_main` | str | Whether the main character can be customized: `Yes`, `No`, `Non-Binary` |
| `Protagonist` | int | Number of protagonists |
| `Protagonist_Non_Male` | int | Number of non-male protagonists (female, non-binary and customizable) |
| `Relevant_males` | int | Male characters in the game |
| `Relevant_no_males` | int | Non-male characters in the game |
| `Percentage_non_male` | float (%) | Percentage of non-male characters |
| `Criteria` | str | Why the game was selected: `TR` top rated · `MS` most sold · `SR` sales and rating |
| `Director` | str | Director gender: `M` male · `F` female · `NB` non-binary · `B` both (several directors of different genders) |
| `Total_team` | int | Main people behind the game (main programmers, developers, directors, producers, artists, designers) |
| `female_team` | int | Number of women in that team |
| `Team_percentage` | float (%) | Percentage of women in the team |
| `Metacritic` | float | Score out of 10 |
| `Destructoid` | float | Score out of 10 |
| `IGN` | float | Score out of 10 |
| `GameSpot` | float | Score out of 10 |
| `Avg_Reviews` | float | Average of the four scores above (reduces single-reviewer bias) |

## 4. `characters`

| Column | Type (doc) | Description |
|---|---|---|
| `Name` | str | Character name |
| `Gender` | str | `Female` (she/her) · `Male` (he/him) · `Non-binary` (ambiguous on purpose, genderless by nature such as objects/plants/animals, or self-identified; they/them) · `Custom` (player chooses) |
| `Game` | str, **FK** | `Game_Id` from `games` |
| `Age` | str | Age during the game events (number or word) |
| `Age_range` | str | Infant 0–5 · Child 6–14 · Teenager 15–17 · Young-Adult 18–24 · Adult 25–39 · Middle-Aged 40–64 · Elderly 65+ · Unknown |
| `Playable` | bool (0/1) | 1 = playable character |
| `Sexualization` | int | Score out of 4, computed from the `sexualization` table |
| `Id` | str, **PK** | Unique character id (`Game_Id` + `_` + name, e.g. `CODMW_Farah`) |
| `Species` | str | `Human` (incl. elves, dwarfs, gods…) · `Humanoid` · `Humanoid-Animal` · `Android-Robot` · `Robots` · `Animated object` · `Animated plant` · `Animal` · `Creatures` · `Unknown` |
| `Side` | str | `P` protagonist's side (supportive or neutral) · `A` antagonist · `B` can be on both |
| `Relevance` | str | `PA` protagonist · `DA` deuteragonist · `SK` sidekick · `MC` main character · `SC` secondary character · `MA` main antagonist |
| `Romantic_Interest` | str | `No` · `Yes` (unavoidably the partner of the main character) · `Opt` (player's choice) |

## 5. `sexualization`

Rating based on 4 criteria; each is 0/1 and `Total` is their sum (0–4).

| Column | Type (doc) | Criterion (1 = true) |
|---|---|---|
| `Id` | str, **PK** | Character id (same as `characters.Id`) |
| `Sexualized_clothing` | bool | Any of: clothes not age-appropriate; clothes that make no sense (high heels for fighting, revealing clothes in extreme weather, armor not covering vital organs); only the female character(s) show sexualized body areas while male counterparts don't |
| `Trophy` | bool | The character's only purpose is to be "won" as a prize for a male character (objectified) |
| `Damsel in Distress` | bool | The character exists to be rescued by the protagonist/main character. **Children and infants are always 0** (needing help is not considered sexist) |
| `Sexualized Cutscenes` | bool | Some or all cutscenes with the character portray them suggestively or focus unnecessarily on body areas such as cleavage, breasts, pubic area, buttocks |
| `Total` | int | Sum of the four criteria (0–4) |

## 6. Differences between the metadata and the real files

Found when loading the data. These feed the cleaning tasks (#2–#4, #11, #20).

| Topic | PDF says | Files show | Action |
|---|---|---|---|
| Column name | `Customization`, `Subgenre`, `Protagonist_non_male`, `Female_team`, `Avg_reviews` | `Customizable_main`, `Sub-genre`, `Protagonist_Non_Male`, `female_team`, `Avg_Reviews` | Rename to `snake_case` |
| `Release` | Date | text like `Nov-13` | Parse with `%b-%y`, extract year |
| `Percentage_non_male`, `Team_percentage` | float | text like `"11%"` | Strip `%`, cast to float |
| `Age` | age of the character | mixed numbers and words (`27`, `Teenager`) | Clean; use `Age_range` for categories |
| `Age_range` | `Young-Adult`, `Child`… | values such as `Teenager`, `Adult` seen; check the rest | Check `value_counts()` |
| `Age_range` bounds | Middle-Aged 40–64, Elderly "older than 65" | age 65 itself is not covered | Note as ambiguity |
| `Sexualization` (in `characters`) | score out of 4 | should equal `sexualization.Total` | Verify consistency |
| Extra column | — | `Unnamed: 27`, fully empty | Drop |
| Missing values | — | `Series` 27/64 · `Destructoid` 57/64 · `IGN` 62/64 · `GameSpot` 62/64 | Decide and justify |
| Size | — | 64 / 637 / 637 rows | Brief asks for ≥ 1,000 rows (own dataset): check with the teacher |

## 7. How to load

```python
import kagglehub, os, pandas as pd

path = kagglehub.dataset_download("br33sa/gender-representation-in-video-games")
games = pd.read_csv(os.path.join(path, "games.grivg.csv"))
characters = pd.read_csv(os.path.join(path, "characters.grivg.csv"))
sexualization = pd.read_csv(os.path.join(path, "sexualization.grivg.csv"))
```
