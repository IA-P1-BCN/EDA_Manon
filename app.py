"""Interactive dashboard: gender representation in video games (board #25).

Run with:  streamlit run app.py

The cleaning below mirrors the notebook's Limpieza + Feature engineering sections
so the dashboard runs on its own. When the reusable cleaning module (#24) exists,
replace `load_data()` with a call to it.
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

RAW_DIR = Path(__file__).parent / "docs" / "raw data"
KAGGLE_DATASET = "br33sa/gender-representation-in-video-games"

ROLE_LABELS = {
    "PA": "Protagonist", "DA": "Deuteragonist", "MA": "Main antagonist",
    "MC": "Main character", "SK": "Sidekick", "SC": "Secondary character",
}
ROLE_TIERS = {"PA": "Lead", "DA": "Major", "MC": "Major", "MA": "Major", "SK": "Minor", "SC": "Minor"}
SIDE_LABELS = {"P": "Protagonist's side", "A": "Antagonist", "B": "Both sides"}
CRITERIA = {"Sexualized_clothing": "Sexualized clothing", "Trophy": "Trophy",
            "Damsel_in_distress": "Damsel in distress", "Sexualized_cutscenes": "Sexualized cutscenes"}
GENDERS = ["Female", "Male"]          # Non-binary (n=33) and Custom (n=8) are too small to compare
COLORS = {"Female": "#c0504d", "Male": "#4a6fa5"}


# ----------------------------------------------------------------------------- data
def _raw_dir() -> Path:
    """Local copy of the CSVs if present, otherwise download them with kagglehub."""
    if (RAW_DIR / "games.grivg.csv").exists():
        return RAW_DIR
    import kagglehub
    return Path(kagglehub.dataset_download(KAGGLE_DATASET))


@st.cache_data(show_spinner="Loading data...")
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (games, characters) cleaned, with sexualization criteria merged into characters."""
    raw = _raw_dir()
    games = pd.read_csv(raw / "games.grivg.csv", encoding="utf-8-sig")
    chars = pd.read_csv(raw / "characters.grivg.csv", encoding="utf-8-sig")
    sex = pd.read_csv(raw / "sexualization.grivg.csv", encoding="utf-8-sig")

    # games: drop empty / unused columns, fix names and types
    games = games.drop(columns=["Unnamed: 27", "Sub-genre", "Publisher", "Platform", "PEGI", "Criteria",
                                "Metacritic ", "Destructoid", "IGN", "GameSpot"], errors="ignore")
    games = games.rename(columns={"female_team": "Female_team"})
    games["Series"] = games["Series"].fillna("Standalone")
    for col in ["Percentage_non_male", "Team_percentage"]:
        games[col] = games[col].astype(str).str.rstrip("%").astype(float)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    games["Release_year"] = 2000 + games["Release"].str[-2:].astype(int)
    games["Release_month"] = games["Release"].str[:3].map({m: i for i, m in enumerate(months, 1)})

    # sexualization: rename, fix the PP_Son inconsistency (a Child flagged as damsel), recompute Total
    sex = sex.rename(columns={"Damsel in Distress": "Damsel_in_distress",
                              "Sexualized Cutscenes": "Sexualized_cutscenes"})
    sex.loc[sex["Id"] == "PP_Son", "Damsel_in_distress"] = 0
    sex["Total"] = sex[list(CRITERIA)].sum(axis=1)

    # characters: drop Age, take the corrected score, add the engineered variables
    chars = chars.drop(columns=["Age"]).drop(columns=["Sexualization"])
    chars = chars.merge(sex, on="Id", how="left").rename(columns={"Total": "Sexualization"})
    chars["Is_sexualized"] = chars["Sexualization"] > 0
    chars["Role"] = chars["Relevance"].map(ROLE_LABELS)
    chars["Role_tier"] = chars["Relevance"].map(ROLE_TIERS)
    chars["Side_label"] = chars["Side"].map(SIDE_LABELS)

    games["Has_female_team"] = games["Team_percentage"] > 0
    games["Team_group"] = pd.cut(games["Team_percentage"], bins=[-1, 0, 25, 100],
                                 labels=["0%", "1-25%", ">25%"]).astype(str)
    by_game = chars.groupby("Game")
    games["Share_women"] = games["Game_Id"].map((chars["Gender"] == "Female").groupby(chars["Game"]).mean() * 100)
    games["Share_sexualized"] = games["Game_Id"].map(by_game["Is_sexualized"].mean() * 100)
    return games, chars


# ----------------------------------------------------------------------------- helpers
def pct(part: int, whole: int) -> str:
    return f"{part / whole * 100:.1f}%" if whole else "n/a"


def share_by_group(df: pd.DataFrame, group: str, flag: pd.Series, order: list[str]) -> pd.DataFrame:
    """% of each gender's characters with `flag`, per value of `group`, with counts for the hover."""
    d = df.assign(_flag=flag)
    out = d.groupby([group, "Gender"], observed=True).agg(Count=("_flag", "sum"), Base=("_flag", "size")).reset_index()
    out["Percent"] = (out["Count"] / out["Base"] * 100).round(1)
    out[group] = pd.Categorical(out[group], categories=order, ordered=True)
    return out.sort_values(group)


def grouped_bar(data: pd.DataFrame, x: str, title: str, y_label: str, x_label: str):
    fig = px.bar(data, x=x, y="Percent", color="Gender", barmode="group", color_discrete_map=COLORS,
                 custom_data=["Count", "Base"], title=title, labels={"Percent": y_label, x: x_label})
    fig.update_traces(hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:.1f}% "
                                    "(%{customdata[0]} of %{customdata[1]})<extra></extra>")
    return fig


def show(fig):
    st.plotly_chart(fig, width="stretch")


# ----------------------------------------------------------------------------- page
st.set_page_config(page_title="Gender in video games", page_icon="🎮", layout="wide")
games_all, chars_all = load_data()

st.title("🎮 Gender representation in video games")
st.caption("64 top-selling or top-rated games released 2012-2022. Results describe successful games, "
           "not the whole industry.")

with st.expander("ℹ️ New here? How to use this dashboard", expanded=False):
    st.markdown(
        """
**What question does it answer?** How are women represented in successful video games, and are they
portrayed differently from men?

**How to use it**
1. **Pick a slice** with the filters on the left (years, genre, country...). Everything on the page updates.
2. **Read the four numbers** at the top: they summarise your slice.
3. **Open the tabs** for the detail. Hover over any bar or dot to see the exact counts behind a percentage.
4. **Reset** a filter by clearing it. With no filter you see all 64 games.

**Good to know**
- Percentages come from small groups. When a slice has few characters, trust the counts, not the percentage.
- Only women and men are compared. Non-binary (33) and custom (8) characters are too few to compare fairly.
- A character is called *sexualized* when it scores above 0 on a 4-point checklist (see the glossary at the bottom).
        """
    )

# --- sidebar filters (they act on games, and characters follow their game)
st.sidebar.header("Filters")
y_min, y_max = int(games_all["Release_year"].min()), int(games_all["Release_year"].max())
years = st.sidebar.slider("Release year", y_min, y_max, (y_min, y_max))
genres = st.sidebar.multiselect("Genre", sorted(games_all["Genre"].unique()), placeholder="All genres")
countries = st.sidebar.multiselect("Developer country", sorted(games_all["Country"].unique()),
                                   placeholder="All countries")
team = st.sidebar.multiselect("Women in the development team", ["0%", "1-25%", ">25%"],
                              placeholder="Any share")
tiers = st.sidebar.multiselect("Character role tier", ["Lead", "Major", "Minor"], placeholder="All roles",
                               help="Lead = protagonist. Major = deuteragonist, main character, main antagonist. "
                                    "Minor = sidekick, secondary character.")

mask = games_all["Release_year"].between(*years)
if genres:
    mask &= games_all["Genre"].isin(genres)
if countries:
    mask &= games_all["Country"].isin(countries)
if team:
    mask &= games_all["Team_group"].isin(team)
games = games_all[mask]
chars = chars_all[chars_all["Game"].isin(games["Game_Id"])]
if tiers:
    chars = chars[chars["Role_tier"].isin(tiers)]

if games.empty or chars.empty:
    st.warning("No game or character matches these filters. Widen them in the sidebar.")
    st.stop()

fm = chars[chars["Gender"].isin(GENDERS)]
women, men = fm[fm["Gender"] == "Female"], fm[fm["Gender"] == "Male"]

# --- headline numbers
c1, c2, c3, c4 = st.columns(4)
c1.metric("Games", len(games))
c2.metric("Characters", len(chars))
c3.metric("Women among characters", pct((chars["Gender"] == "Female").sum(), len(chars)),
          help=f"{(chars['Gender'] == 'Female').sum()} of {len(chars)} characters")
c4.metric("Sexualized (score > 0)",
          f"{pct(women['Is_sexualized'].sum(), len(women))} of women",
          delta=f"{pct(men['Is_sexualized'].sum(), len(men))} of men", delta_color="off",
          help=f"Women: {women['Is_sexualized'].sum()} of {len(women)}. Men: {men['Is_sexualized'].sum()} of {len(men)}.")
if len(chars) < 60:
    st.info("Small selection: read percentages with caution and check the counts in the hover.")

tab_roles, tab_sex, tab_teams, tab_time, tab_data = st.tabs(
    ["👥 Roles & side", "⚠️ Sexualization", "🏢 Development teams", "📈 Over time", "🗂️ Data"])

with tab_roles:
    st.markdown("Do women get the important parts of the story? Left chart: what share of "
                "each gender's characters has each role. Right chart: whose side they are on. "
                "Bottom chart: who holds each role (women are about 32% of all characters, so a bar "
                "below that means women are under-represented in that role).")
    st.caption("Unit: character. Women vs men only (Non-binary and Custom characters are too few to compare).")
    role_order = list(ROLE_LABELS.values())
    left, right = st.columns(2)
    with left:
        d = fm.assign(_all=True).groupby(["Role", "Gender"]).size().rename("Count").reset_index()
        d["Base"] = d["Gender"].map(fm["Gender"].value_counts())
        d["Percent"] = (d["Count"] / d["Base"] * 100).round(1)
        d["Role"] = pd.Categorical(d["Role"], categories=role_order, ordered=True)
        show(grouped_bar(d.sort_values("Role"), "Role", "Roles held by women and men",
                         "% of the gender's characters", "Role in the story"))
    with right:
        d = fm.groupby(["Side_label", "Gender"]).size().rename("Count").reset_index()
        d["Base"] = d["Gender"].map(fm["Gender"].value_counts())
        d["Percent"] = (d["Count"] / d["Base"] * 100).round(1)
        show(grouped_bar(d, "Side_label", "Side taken by women and men",
                         "% of the gender's characters", "Side in the story"))
    st.markdown("**Share of women within each role** (the opposite reading: who holds the role)")
    d = chars.groupby("Role").agg(Women=("Gender", lambda s: (s == "Female").sum()), Total=("Gender", "size")).reindex(role_order).dropna()
    d["Percent"] = (d["Women"] / d["Total"] * 100).round(1)
    fig = px.bar(d.reset_index(), x="Percent", y="Role", orientation="h", custom_data=["Women", "Total"],
                 title="Women as a share of each role", labels={"Percent": "Women (% of the role)"})
    fig.update_traces(marker_color=COLORS["Female"],
                      hovertemplate="<b>%{y}</b><br>%{x:.1f}% (%{customdata[0]} of %{customdata[1]})<extra></extra>")
    fig.update_yaxes(categoryorder="array", categoryarray=role_order[::-1])
    show(fig)

with tab_sex:
    st.markdown("Out of 100 women and 100 men in these games, how many are portrayed in a "
                "sexualized way? Left chart: the overall gap. Right chart: which of the four checklist items "
                "causes it. Bottom chart: whether the gap changes with the importance of the role.")
    st.caption("Unit: character. A character is 'sexualized' when its score is above 0. "
               "Only a few characters score above 0, so compare shares, not averages.")
    left, right = st.columns(2)
    with left:
        d = fm.groupby("Gender").agg(Count=("Is_sexualized", "sum"), Base=("Is_sexualized", "size")).reset_index()
        d["Percent"] = (d["Count"] / d["Base"] * 100).round(1)
        fig = px.bar(d, x="Gender", y="Percent", color="Gender", color_discrete_map=COLORS,
                     custom_data=["Count", "Base"], title="Sexualized characters, women vs men",
                     labels={"Percent": "Characters with a score above 0 (%)"})
        fig.update_traces(hovertemplate="<b>%{x}</b><br>%{y:.1f}% (%{customdata[0]} of %{customdata[1]})<extra></extra>")
        fig.update_layout(showlegend=False)
        show(fig)
    with right:
        rows = []
        for gender, group in fm.groupby("Gender"):
            for col, label in CRITERIA.items():
                rows.append({"Gender": gender, "Criterion": label, "Count": int(group[col].sum()),
                             "Base": len(group), "Percent": round(group[col].mean() * 100, 1)})
        show(grouped_bar(pd.DataFrame(rows), "Criterion", "Which criteria drive the gap?",
                         "% of the gender's characters", "Sexualization criterion"))
    tier_order = ["Lead", "Major", "Minor"]
    show(grouped_bar(share_by_group(fm, "Role_tier", fm["Is_sexualized"], tier_order), "Role_tier",
                     "Does it depend on the role? Sexualized share by role tier",
                     "% sexualized within the gender", "Role tier"))
    st.caption("Groups are very small once split by role: use the hover to see the counts.")

with tab_teams:
    st.markdown("Do studios with more women on the team make games with more female "
                "characters? Left chart: games grouped by the share of women in their team. "
                "Right chart: every game as a dot (hover for its name). Dots higher up have more female characters; "
                "dots further right have more women in the team.")
    st.caption("Unit: game. 36 of 64 games have no woman in the team, so games are grouped by team share "
               "instead of averaging the percentage.")
    left, right = st.columns(2)
    with left:
        d = games.groupby("Team_group").agg(Games=("Game_Id", "size"), Median=("Share_women", "median")).reindex(["0%", "1-25%", ">25%"]).dropna().reset_index()
        fig = px.bar(d, x="Team_group", y="Median", custom_data=["Games"],
                     title="Women among characters, by women in the dev team (median per game)",
                     labels={"Team_group": "Women in the development team", "Median": "Women among characters (%)"})
        fig.update_traces(marker_color=COLORS["Female"],
                          hovertemplate="<b>Team %{x}</b><br>Median %{y:.1f}% across %{customdata[0]} games<extra></extra>")
        show(fig)
    with right:
        fig = px.scatter(games, x="Team_percentage", y="Share_women", hover_name="Title",
                         hover_data={"Release_year": True, "Team_percentage": ":.0f", "Share_women": ":.1f"},
                         title="Each dot is a game",
                         labels={"Team_percentage": "Women in the development team (%)",
                                 "Share_women": "Women among characters (%)", "Release_year": "Year"})
        fig.update_traces(marker=dict(size=10, color=COLORS["Female"], opacity=0.75))
        show(fig)
    st.markdown("**Games in the current selection**")
    st.dataframe(games[["Title", "Release_year", "Genre", "Country", "Team_percentage", "Share_women", "Share_sexualized", "Avg_Reviews"]]
                 .sort_values("Release_year").round(1), hide_index=True, width="stretch")

with tab_time:
    st.markdown("Is the situation improving? Each line follows one measure year by year. "
                "A rising 'female characters' line means more women on screen; a falling "
                "'sexualized women' line means fewer of them portrayed that way.")
    st.caption("Unit: character, grouped by the release year of its game. Some years have few characters: check the hover.")
    c = chars.merge(games[["Game_Id", "Release_year"]], left_on="Game", right_on="Game_Id")
    c["Is_female"] = c["Gender"] == "Female"
    t = c.groupby("Release_year").agg(Characters=("Id", "size"), Women=("Is_female", "sum")).reset_index()
    t["Women_sexualized"] = t["Release_year"].map(c[c["Is_female"]].groupby("Release_year")["Is_sexualized"].sum()).fillna(0)
    rows = pd.concat([
        pd.DataFrame({"Year": t["Release_year"], "Measure": "Female characters (% of characters)",
                      "Percent": (t["Women"] / t["Characters"] * 100).round(1), "Count": t["Women"], "Base": t["Characters"]}),
        pd.DataFrame({"Year": t["Release_year"], "Measure": "Sexualized women (% of women)",
                      "Percent": (t["Women_sexualized"] / t["Women"].where(t["Women"] > 0) * 100).round(1),
                      "Count": t["Women_sexualized"], "Base": t["Women"]}),
    ])
    fig = px.line(rows, x="Year", y="Percent", color="Measure", markers=True, custom_data=["Count", "Base"],
                  title="Women in video games over time", labels={"Percent": "Percentage (%)", "Year": "Release year"})
    fig.update_traces(hovertemplate="<b>%{x}</b><br>%{y:.1f}% (%{customdata[0]:.0f} of %{customdata[1]})<extra>%{fullData.name}</extra>")
    fig.update_xaxes(dtick=1)
    fig.update_layout(hovermode="x unified", legend=dict(orientation="h", y=-0.2))
    show(fig)

with tab_data:
    st.markdown("The raw numbers behind every chart, for your current filters. "
                "Click a column header to sort; use the buttons to download the table.")
    st.markdown(f"**Characters ({len(chars)})**")
    st.dataframe(chars.drop(columns=["Role", "Side_label"]), hide_index=True, width="stretch")
    st.download_button("⬇️ Download characters (CSV)", chars.to_csv(index=False).encode("utf-8"),
                       "characters_filtered.csv", "text/csv")
    st.markdown(f"**Games ({len(games)})**")
    st.dataframe(games, hide_index=True, width="stretch")
    st.download_button("⬇️ Download games (CSV)", games.to_csv(index=False).encode("utf-8"),
                       "games_filtered.csv", "text/csv")

# ----------------------------------------------------------------------------- glossary
with st.expander("📖 Glossary: what the terms mean"):
    st.markdown(
        """
| Term | Meaning |
|---|---|
| **Sexualized** | The character scores above 0 on a 4-point checklist: sexualized clothing, treated as a trophy, damsel in distress, sexualized cutscenes (1 point each). |
| **Protagonist (Lead)** | The most important character(s) of the game. |
| **Major roles** | Deuteragonist (second lead), main character (important throughout the story) and main antagonist (main villain). |
| **Minor roles** | Sidekick and secondary characters. |
| **Side** | Whether the character helps the protagonist, opposes them (antagonist) or switches between both. |
| **Women in the development team** | Share of the studio's team made up of women, as credited for the game. 36 of 64 games have none. |
| **Median** | The middle value: half of the games are above it, half below. Better than the average when a few games are very different from the rest. |
        """
    )
    st.caption("Source: Kaggle dataset *Gender Representation in Video Games* (Brisa Palomar, 2022). "
               "The games are top-selling or top-rated titles of 2012-2022.")
