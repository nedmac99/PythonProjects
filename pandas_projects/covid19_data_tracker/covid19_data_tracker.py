import pandas as pd
from pathlib import Path

#Objectives
'''
-Create an analysis dashboard for confirmed cases, deaths, and recoveries across countries and time.
-Load global COVID data
-Track changes over time
-Group by country
-Calculate growth rates or moving averages
-Visualize results (optional)(plot)
'''

file_path = Path(__file__).parent / "worldometer_data.csv"

df = pd.read_csv(file_path,  encoding='ISO-8859-1')

#Provide information about data
print(f"{df.info()}\n")

#Print the first five entries
print(f"{df.head()}\n")

#Clean data
df.columns = df.columns.str.strip()

#Before dropna
print(f"Missing Values: \n{df.isnull().sum()}\n")

#Drop duplicate rows. No duplicates found
#df.drop_duplicates(inplace=True)


#Dropping rows with null values
#Dropping rows with null values only leaves 3 rows left
#df.dropna(inplace=True)

#After dropna
#print(f"Missing Values after dropna: \n{df.isnull().sum()}\n")

#Print first 5 entries after dropping rows with null values
#print(f"{df.head()}\n")
