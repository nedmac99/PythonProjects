#Customized
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(page_title="Fantasy Football Dashboard", layout='wide')

# --- LOAD DATA ---
file_path = Path(__file__).parent / "all_players.csv"
df = pd.read_csv(file_path)

# --- VALIDATE FILE STRUCTURE ---
required_columns = {"Ovr", "Name", "POS", "Team", 
                    "W1","W2","W3","W4","W5","W6","W7","W8","W9",
                    "W10","W11","W12","W13","W14","W15","W16","W17","W18"}
if not required_columns.issubset(df.columns):
    st.error(f"Missing required columns! Your CSV must include: {', '.join(required_columns)}")
    st.stop()

# --- CALCULATIONS ---
weekly_columns = [col for col in df.columns if col.startswith("W")]
df["Total_Points"] = df[weekly_columns].sum(axis=1)

def flag_sleeper_picks(df, points_col='Total_Points', ovr_col='Ovr', sleeper_percentile=0.75, ovr_threshold=50):
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
    df[points_col] = pd.to_numeric(df[points_col], errors='coerce')
    df[ovr_col] = pd.to_numeric(df[ovr_col], errors='coerce')
    # Calculate threshold for high points
    points_cutoff = df[points_col].quantile(sleeper_percentile)
    # Sleeper: high points, Ovr above threshold (i.e., not top picks)
    sleepers = df[(df[points_col] >= points_cutoff) & (df[ovr_col] >= ovr_threshold)]
    return sleepers.sort_values(by=points_col, ascending=False)

# --- SIDEBAR CONTROLS ---
st.sidebar.title("Dashboard Controls")

selected_week = st.sidebar.selectbox(
    "Select Week to View", 
    ["Overall"] + weekly_columns
)

selected_player = st.sidebar.selectbox(
    "Select Player to View Trend",
    sorted(df["Name"].unique())
)

# --- CHECK IF SELECTED WEEK HAS DATA ---

# --- CHECK IF SELECTED WEEK HAS DATA ---
no_week_data = False
if selected_week != "Overall":
    week_data = df[selected_week].dropna()
    if week_data.empty or week_data.sum() == 0:
        st.warning(f"No data for {selected_week}. Showing overall stats and player trends only.")
        no_week_data = True

# --- DETERMINE TOP PLAYER ---
if selected_week == "Overall" or no_week_data:
    top_player = df.loc[df["Total_Points"].idxmax()]
    points = round(top_player["Total_Points"], 2)
else:
    top_player = df.loc[df[selected_week].idxmax()]
    points = round(top_player[selected_week], 2)


# --- CUSTOM STYLES ---
kpi_style = """
<style>
.kpi-card {
    background: linear-gradient(135deg, #83c9ff 0%, #83c9ff 100%);
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(30,144,255,0.08);
    padding: 1.5rem 1rem;
    margin-bottom: 1rem;
    text-align: center;
    border: 1.5px solid #c2e0ff;
}
.kpi-title {
    color: #1E90FF;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #222;
}
.section-title {
    font-size: 1.5rem;
    color: #1E90FF;
    font-weight: 700;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
}
</style>
"""
st.markdown(kpi_style, unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
st.markdown('<div class="section-title">🏈 Fantasy Football Dashboard</div>', unsafe_allow_html=True)

# --- KPI SECTION ---
st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Overall Rank</div><div class="kpi-value">{int(top_player["Ovr"])} </div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Name</div><div class="kpi-value">{top_player["Name"]} </div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Fantasy Points</div><div class="kpi-value">{points} </div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Position</div><div class="kpi-value">{top_player["POS"]} </div></div>', unsafe_allow_html=True)

st.markdown("---")

# --- LEADERBOARD CHART ---
st.markdown('<div class="section-title">Leaderboard</div>', unsafe_allow_html=True)
if selected_week == "Overall" or no_week_data:
    chart_df = df.nlargest(10, "Total_Points")
    title = "Top 10 Players by Total Fantasy Points"
    y_col = "Total_Points"
else:
    chart_df = df.nlargest(10, selected_week)
    title = f"Top 10 Players - {selected_week}"
    y_col = selected_week

fig = px.bar(
    chart_df,
    x="Name",
    y=y_col,
    color="POS",
    title=title,
    text_auto=True
)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#222222'),
    title_font=dict(size=22, color='#1E90FF'),
    legend=dict(bgcolor='rgba(0,0,0,0)')
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# --- PLAYER TREND SECTION ---
st.markdown(f'<div class="section-title">Performance Trend: {selected_player}</div>', unsafe_allow_html=True)
player_data = df[df["Name"] == selected_player][weekly_columns].T
player_data.columns = ["Fantasy Points"]
player_data["Week"] = player_data.index
fig_line = px.line(
    player_data,
    x="Week",
    y="Fantasy Points",
    title=f"Week-by-Week Performance for {selected_player}",
    markers=True
)
fig_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#222222'),
    title_font=dict(size=20, color='#1E90FF'),
    legend=dict(bgcolor='rgba(0,0,0,0)')
)
st.plotly_chart(fig_line, use_container_width=True)
st.markdown("---")

# --- SLEEPER PICKS SECTION ---
st.markdown('<div class="section-title">Potential Sleeper Picks</div>', unsafe_allow_html=True)
sleeper_df = flag_sleeper_picks(df)
if not sleeper_df.empty:
    st.dataframe(sleeper_df[["Ovr", "Name", "POS", "Team", "Total_Points"]], use_container_width=True, height=350)
    st.info("Sleeper picks are players with high total points but a lower draft rank (Ovr >= 50).")
else:
    st.write("No sleeper picks found with current criteria.")
