import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from sklearn.metrics import confusion_matrix

st.set_page_config(page_title="Data Science Performance Dashboard", layout="wide")
file_path = Path(__file__).parent / "model_results.csv"

#Helper function
@st.cache_data
def load_csv(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Failed to load CSV file: {e}")
        return None
    
#---SIDEBAR---
st.sidebar.title("Dashboard Controls")

# File uploader (optional) -- user can upload a CSV to override local file
uploaded_file = st.sidebar.file_uploader("Upload model_results.csv (optional)", type=["csv"])

if uploaded_file is not None:
    df = load_csv(uploaded_file)
else:
    st.info("Please upload a CSV file to begin.")
    st.stop()

#Validate file Structure
required_columns = {"Model", "Accuracy", "Precision", "Recall", "F1", "AUC"}
if not required_columns.issubset(df.columns):
    st.error(f"Missing required columns! Your CSV must include: {', '.join(required_columns)}")
    st.stop()

#Optional date column
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])
    min_date, max_date = df["Date"].min(), df["Date"].max()
    date_range = st.sidebar.date_input("filter by Date Range", [min_date, max_date])
    start, end = date_range
    df = df[(df["Date"] >= pd.to_datetime(start)) & (df["Date"] <= pd.to_datetime(end))]

#Model filter
models = sorted(df["Model"].unique())
selected_modles = st.sidebar.multiselect("Select models to display", models, default=models)
filtered = df[df["Model"].isin(selected_modles)]

#Metrics selector
metrics = ["Accuracy", "Precision", "Recall", "F1", "AUC"]
metric_choice = st.sidebar.selectbox("Select metric to highlight", metrics, index=0)

#---MAIN DASHBOARD---
st.title("Data Science Performance Dashboard")

#KPI Section
st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Best Accuracy", f"{filtered['Accuracy'].max():.3f}")
col2.metric("Best F1 Score", f"{filtered['F1'].max():.3f}")
col3.metric("Avg train Time", f"{filtered['Train_Time'].mean():.2f}s" if "Train_Time" in filtered.columns else "N/A")

st.divider()

#---CHARTS---
colA, colB = st.columns(2)

with colA:
    st.markdown("#### Model Comparison (Bar chart)")
    fig_bar = px.bar(
        filtered,
        x='Model',
        y=metrics,
        barmode='group',
        title="Performance Comparison Across Models"
    )
    fig_bar.update_layout(xaxis_tickangle=-45, yaxis_title="Score")
    st.plotly_chart(fig_bar, use_container_width=True)
    
with colB:
    st.markdown("#### Precision vs Recall Scatter")
    fig_scatter = px.scatter(
        filtered,
        x="Precision",
        y="Recall",
        size="F1",
        color='Model',
        hover_name='Model',
        title="Precision vs Recall (bubble size = F1)"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
st.divider()

#---CONFUSION MATRIX SECTION---
st.markdown("### Confusion Matrix Visualizer")

cm_file = st.file_uploader("Upload confusion_matrix_data.csv (with y_true, y_pred columns)", type=["csv"])
if cm_file is not None:
    try:
        cm_df = pd.read_csv(cm_file)
        if {"y_true", "y_pred"}.issubset(cm_df.columns):
            labels = sorted(set(cm_df["y_true"]) | set(cm_df["y_pred"]))
            cm = confusion_matrix(cm_df["y_true"], cm_df["y_pred"], labels=labels)
            cm_fig = px.imshow(
                cm, 
                text_auto=True,
                x=labels,
                y=labels,
                color_continuous_scale="Blues",
                title="Confusion Matrix"
                )
            cm_fig.update_xaxes(title="Predicted")
            cm_fig.update_yaxes(title="Actual")
            st.plotly_chart(cm_fig, use_container_width=True)
        else:
            st.warning("Confusion matrix file must contain 'y_true' and 'y_pred' columns.")
    except Exception as e:
        st.error(f"Error reading confusion matrix file: {e}")
else:
    st.caption("You can upload a CSV with y_true, y_pred columns to view the confusion matrix.")

st.divider()

#---DATA DOWNLOAD---
st.markdown("### Download Filtered Results")
csv_export = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv_export,
    file_name="filtered_model_results.csv",
    mime="text/csv"
)

#---FOOTER---
st.caption("Built using Streamlit, pandas, Plotly, and scikit-learn.")
    
