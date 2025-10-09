import pandas as pd
import streamlit as st
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Data Science Perormance Dashboard", layout='wide')

#Load CSV into file
file_path = Path(__file__).parent / "model_results.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

#Sidebar Filters
st.sidebar.header("Filter Models")
selected_models = st.sidebar.multiselect("Select Models", df['Model'].unique(), df['Model'].unique())
filtered_df = df[df['Model'].isin(selected_models)]

#Dashboard title
st.title("Data Science Performance Dashboard")

#KPI metrics
st.subheader("Key Performance Metrics")
st.metric("Best Accuracy", f"{filtered_df['Accuracy'].max():.2f}")
st.metric("Best F1 Score", f"{filtered_df['F1'].max():.2f}")

#Charts
col1, col2 = st.columns(2)
with col1:
    fig1 = px.bar(df, x='Model', y=['Accuracy', 'F1'], barmode='group', title="Accuracy vs F1 Score")
    st.plotly_chart(fig1, use_container_width=True)
    
with col2:
    fig2 = px.scatter(filtered_df, x='Precision', y='Recall', color='Model', size='F1', title="Precision vs Recall")
    st.plotly_chart(fig2, use_container_width=True)
    
#Footer
st.caption("Built with Streamlit and Plotly")

