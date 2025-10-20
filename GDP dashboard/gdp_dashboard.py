import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import streamlit as st

# Load GDP data
file_path = Path(__file__).parent / "gdp_data.csv"
df = pd.read_csv(file_path)

#Clean column names
df.columns = df.columns.str.strip()

# Display basic information about the DataFrame
df.info()
print(df.head())
print(df.columns)

# Example: Print the list of countries
print(df['Country'])

# Example: Filter data for a specific country
print(df[df['Country'] == 'Angola'])

