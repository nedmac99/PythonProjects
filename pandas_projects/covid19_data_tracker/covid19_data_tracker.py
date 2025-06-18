import pandas as pd
from pathlib import Path

#Objectives
'''
-Create an analysis dashboard for confirmed cases, deaths, and recoveries across countries and time.
-Load global COVID data
-Track changes over time
-Group by country
-Calculate growth rates or moving averages
-Visualize results (optional)
'''

file_path = Path(__file__).parent / "worldometer_data.csv"

df = pd.read_csv(file_path,  encoding='ISO-8859-1')

#Provide information about data
#print(df.info())

#Print the first ten entries
#print(df.head(10))

print(df.groupby("Country/Region").get_group("USA"))
df.dropna(inplace=True)
print(df.groupby("Country/Region").get_group("USA"))