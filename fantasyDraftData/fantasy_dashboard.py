import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
import random
import plotly.figure_factory as ff
import plotly.graph_objects as go
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(page_title="Fantasy Football Dashboard", layout="wide")

# --- LOAD DATA ---
file_path = Path(__file__).parent / "all_players.csv"
df = pd.read_csv(file_path)

# --- VALIDATE FILE STRUCTURE ---
required_columns = {
    "Ovr",
    "Name",
    "POS",
    "Team",
    "W1",
    "W2",
    "W3",
    "W4",
    "W5",
    "W6",
    "W7",
    "W8",
    "W9",
    "W10",
    "W11",
    "W12",
    "W13",
    "W14",
    "W15",
    "W16",
    "W17",
    "W18",
}
if not required_columns.issubset(df.columns):
    st.error(
        f"Missing required columns! Your CSV must include: {', '.join(required_columns)}"
    )
    st.stop()

# --- CALCULATIONS ---
weekly_columns = [col for col in df.columns if col.startswith("W")]
df["Total_Points"] = df[weekly_columns].sum(axis=1)


def flag_sleeper_picks(
    df,
    points_col="Total_Points",
    ovr_col="Ovr",
    sleeper_percentile=0.75,
    ovr_threshold=50,
):
    """
    Flags sleeper picks: players with high fantasy points but low draft rank (high Ovr).
    Args:
        df: DataFrame with player data
        points_col: Column for total or average points
        ovr_col: Column for overall rank
        sleeper_percentile: Percentile for high points (e.g., top 25%)
        ovr_threshold: Minimum Ovr (higher = later pick) to be considered a sleeper
    Returns:
        DataFrame of sleeper picks
    """
    # Ensure numeric
    df = df.copy()
    df[points_col] = pd.to_numeric(df[points_col], errors="coerce")
    df[ovr_col] = pd.to_numeric(df[ovr_col], errors="coerce")
    # Calculate threshold for high points
    points_cutoff = df[points_col].quantile(sleeper_percentile)
    # Sleeper: high points, Ovr above threshold (i.e., not top picks)
    sleepers = df[(df[points_col] >= points_cutoff) & (df[ovr_col] >= ovr_threshold)]
    return sleepers.sort_values(by=points_col, ascending=False)


# --- SIDEBAR CONTROLS ---
st.sidebar.title("Dashboard Controls")

selected_week = st.sidebar.selectbox(
    "Select Week to View", ["Overall"] + weekly_columns
)

selected_player = st.sidebar.selectbox(
    "Select Player to View Trend", sorted(df["Name"].unique())
)


# --- MOBILE-FRIENDLY LAYOUT ---
mobile_mode = st.sidebar.checkbox("Mobile-Friendly Layout (Compact Mode)")
if mobile_mode:
    st.markdown(
        "<style>body, .main, .block-container { max-width: 100vw !important; padding: 0.5rem !important; } .kpi-card { margin-bottom: 0.5rem !important; } </style>",
        unsafe_allow_html=True,
    )

# --- CHECK IF SELECTED WEEK HAS DATA ---
no_week_data = False
if selected_week != "Overall":
    week_data = df[selected_week].dropna()
    if week_data.empty or week_data.sum() == 0:
        st.warning(
            f"No data for {selected_week}. Showing overall stats and player trends only."
        )
        no_week_data = True

# --- DETERMINE TOP PLAYER ---
if selected_week == "Overall" or no_week_data:
    top_player = df.loc[df["Total_Points"].idxmax()]
    points = round(top_player["Total_Points"], 2)
else:
    top_player = df.loc[df[selected_week].idxmax()]
    points = round(top_player[selected_week], 2)

# --- MAIN DASHBOARD ---
st.title("🏈 Fantasy Football Dashboard")

# --- KPI SECTION ---
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Overall Rank", int(top_player["Ovr"]))
col2.metric("Highlighted Player this week", top_player["Name"])
col3.metric("Total Fantasy Points", points)
col4.metric("Position", top_player["POS"])

st.divider()

# --- LEADERBOARD CHART ---
if selected_week == "Overall" or no_week_data:
    chart_df = df.nlargest(10, "Total_Points")
    title = "Top 10 Players by Total Fantasy Points"
    y_col = "Total_Points"
else:
    chart_df = df.nlargest(10, selected_week)
    title = f"Top 10 Players - {selected_week}"
    y_col = selected_week

fig = px.bar(chart_df, x="Name", y=y_col, color="POS", title=title, text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# --- PLAYER COMPARISON TOOL ---
st.sidebar.markdown("---")
compare_players = st.sidebar.multiselect("Compare Players", sorted(df["Name"].unique()))
if compare_players:
    st.markdown(
        '<div class="section-title">Player Comparison</div>', unsafe_allow_html=True
    )
    comp_df = df[df["Name"].isin(compare_players)].set_index("Name")
    st.dataframe(
        comp_df[["Ovr", "POS", "Team", "Total_Points"] + weekly_columns],
        use_container_width=True,
    )

# --- TRADE VALUE ANALYZER ---
st.sidebar.markdown("---")
trade_player_1 = st.sidebar.selectbox(
    "Trade Analyzer: Player 1", ["None"] + sorted(df["Name"].unique())
)
trade_player_2 = st.sidebar.selectbox(
    "Trade Analyzer: Player 2", ["None"] + sorted(df["Name"].unique())
)
if (
    trade_player_1 != "None"
    and trade_player_2 != "None"
    and trade_player_1 != trade_player_2
):
    st.markdown(
        '<div class="section-title">Trade Value Analyzer</div>', unsafe_allow_html=True
    )
    p1 = df[df["Name"] == trade_player_1].iloc[0]
    p2 = df[df["Name"] == trade_player_2].iloc[0]
    st.write(
        f"**{trade_player_1}**: {p1['Total_Points']} pts, Ovr {p1['Ovr']}, POS {p1['POS']}"
    )
    st.write(
        f"**{trade_player_2}**: {p2['Total_Points']} pts, Ovr {p2['Ovr']}, POS {p2['POS']}"
    )
    if abs(p1["Total_Points"] - p2["Total_Points"]) < 20:
        st.success("This trade is likely fair.")
    elif p1["Total_Points"] > p2["Total_Points"]:
        st.warning(
            f"{trade_player_1} is more valuable. Consider asking for more in return."
        )
    else:
        st.warning(
            f"{trade_player_2} is more valuable. Consider asking for more in return."
        )


# --- PLAYER TREND SECTION ---
st.subheader(f"Performance Trend: {selected_player}")

player_data = df[df["Name"] == selected_player][weekly_columns].T
player_data.columns = ["Fantasy Points"]
player_data["Week"] = player_data.index

fig_line = px.line(
    player_data,
    x="Week",
    y="Fantasy Points",
    title=f"Week-by-Week Performance for {selected_player}",
    markers=True,
)
st.plotly_chart(fig_line, use_container_width=True)

# --- START/SIT RECOMMENDATIONS ---
st.sidebar.markdown("---")
start_sit_pos = st.sidebar.selectbox("Start/Sit: Position", ["QB", "RB", "WR", "TE"])
start_sit_week = st.sidebar.selectbox("Start/Sit: Week", weekly_columns)
ss_df = (
    df[df["POS"] == start_sit_pos]
    .sort_values(by=start_sit_week, ascending=False)
    .head(5)
)
st.markdown(
    f'<div class="section-title">Start/Sit Recommendations ({start_sit_pos}, {start_sit_week})</div>',
    unsafe_allow_html=True,
)
st.dataframe(ss_df[["Ovr", "Name", "Team", start_sit_week]], use_container_width=True)

# --- SLEEPER PICKS SECTION ---
st.subheader("Potential Sleeper Picks")
sleeper_df = flag_sleeper_picks(df)
if not sleeper_df.empty:
    st.dataframe(
        sleeper_df[["Ovr", "Name", "POS", "Team", "Total_Points"]],
        use_container_width=True,
    )
    st.info(
        "Sleeper picks are players with high total points but a lower draft rank (Ovr >= 50)."
    )
else:
    st.write("No sleeper picks found with current criteria.")
