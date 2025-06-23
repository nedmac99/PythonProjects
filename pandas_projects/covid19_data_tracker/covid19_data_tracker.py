import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

file_path = Path(__file__).parent / "worldometer_data.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

#Cleaning up the data
df.columns = df.columns.str.strip()
#print(df.head())
#df.info()
#print('\n')

#Counting the null values per column
#print(df.isnull().sum())
#df.dropna(inplace=True)

print(df.sort_values('TotalCases', ascending=False).head(10))
