import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Data Science Performance Dashboard", layout="wide")
file_path = Path(__file__).parent / "model_results.csv"


@st.cache_data
def load_data_from_file(path):
    return pd.read_csv(path)


# File uploader (optional) -- user can upload a CSV to override local file
uploaded = st.sidebar.file_uploader("Upload model_results.csv (optional)", type=["csv"])


if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    df = load_data_from_file(file_path)

# Sidebar controls
st.sidebar.header("Filters")
models = list(df["Model"].unique())
selected_models = st.sidebar.multiselect("Selected models", models, default=models)

# Filtered DataFrame
filtered = df[df["Model"].isin(selected_models)]

# Top KPIs
st.subheader("Key metrics")
k1, k2, k3 = st.columns(3)
k1.metric("Best Accuracy", f"{filtered['Accuracy'].max():.2f}")
k2.metric("Best F1", f"{filtered['F1'].max():.2f}")
k3.metric("Average train time (s)", f"{filtered['Train_Time'].mean():.2f}")

st.markdown("---")

# Layout charts in two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### Accuracy vs F1 (grouped)")
    # Use wide-form bar: pass list for y
    fig1 = px.bar(
        filtered,
        x="Model",
        y=["Accuracy", "F1"],
        barmode="group",
        title="Accuracy and F1 by Model",
    )
    fig1.update_layout(xaxis_tickangle=-45, yaxis_title="Score")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("#### Precision vs Recall")
    fig2 = px.scatter(
        filtered,
        x="Precision",
        y="Recall",
        size="F1",
        hover_name="Model",
        title="Precision vs Recall (size = F1)",
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("#### Correlation matrix")
    metrics = ["Accuracy", "Precision", "Recall", "F1", "AUC", "Train_Time"]
    corr = filtered[metrics].corr()
    fig3 = px.imshow(corr, text_auto=True, title="Correlation matirx")
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.subheader("Model results table")
st.dataframe(filtered.reset_index(drop=True))
