import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

files = ["worldometer_data.csv", "time_series_covid19_confirmed_global.csv", "time_series_covid19_deaths_global.csv"]

file_path = Path(__file__).parent / files[0]
file_path2 = Path(__file__).parent / files[1]
file_path3 = Path(__file__).parent / files[2]
df = pd.read_csv(file_path, encoding='ISO-8859-1')
df2 = pd.read_csv(file_path2, encoding='ISO-8859-1')
df3 = pd.read_csv(file_path3, encoding='ISO-8859-1')

#Cleaning up the data

df.columns = df.columns.str.strip()
df2.columns = df2.columns.str.strip()
df3.columns = df3.columns.str.strip()
#print(df.head())
#df.info()

#Analysis of the data

#Counting the null values per column
#print(df.isnull().sum())
#df.dropna(inplace=True)

#Find the top 10 Countries with the highest TotalCases
#print(df.sort_values('TotalCases', ascending=False).head(10))

#Find the countries that have the highest death rate
df['DeathRate'] = df['TotalDeaths'] / df['TotalCases']
#print(df.sort_values('DeathRate', ascending=False).head())

#Find countries with high total cases but low deaths using deathrate
#print(df[(df['TotalCases'] > 100000) & (df['DeathRate'] < 0.01)])

#Find the countries with the highest death rate despite low case counts
#print(df[(df['TotalCases'] < 50000) & (df['DeathRate'] > .05)])

#Find confirmed cases per million people
df['CasesPerMillion'] = (df['TotalCases'] * 1000000) / (df['Population'])
#print(df.sort_values('CasesPerMillion', ascending=False).head())

#Find out how many deaths per million
df['DeathsPerMillion'] = (df['TotalDeaths'] * 1000000) / (df['Population']) 
#print(df.sort_values('DeathsPerMillion', ascending=False).head())

#Find percent of cases recovered
df['RecoveryRate'] = (df['TotalRecovered']) / (df['TotalCases'])
#print(df.sort_values('RecoveryRate', ascending=False).head(10))

#Visualizations

#Chart top 10 countries by cases per million in descending order
#df.sort_values('CasesPerMillion', ascending=False).head(10).plot(kind='bar', x='Country/Region', y='CasesPerMillion')
#plt.show()

#Chart top 10 countries by deaths per million
#df.sort_values('DeathsPerMillion', ascending=False).head(10).plot(kind='bar', x='Country/Region', y='DeathsPerMillion')
#plt.show()

#Chart top 10 recovery rates with horizontal bar graph
#df.sort_values('RecoveryRate', ascending=False).head(10).plot(kind='barh', x='Country/Region', y='RecoveryRate')
#plt.show()

#Chart top 10 death rates with a vertical bar chart
#df.sort_values('DeathRate', ascending=False).head(10).plot(kind='bar', x='Country/Region', y='DeathRate')
#plt.show()

#Time-Series Analysis for confirmed cases
#df2.info()
#print(df2.head())

#Reshape data so that first 4 columns('Province/State', 'Country/Region', 'Lat', 'Long') stay fixed and all the remaining date columns become rows with one column for Date and one column for Confirmed cases
df2_melted = pd.melt(df2, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Confirmed')
print(df2_melted.head(10000))