from pathlib import Path
import pandas as pd

df = pd.read_csv(Path(__file__).parent / "movies.csv")

#Remove leading and trailing spaces from column names
df.columns = df.columns.str.strip()

#df.info()
#print("----------------------------------------------------------------------------------------")
#print(df.head())
#print("----------------------------------------------------------------------------------------")
#print(df.columns)
#print("----------------------------------------------------------------------------------------")


#Print top 10 movies ordered by score
sorted_score = df.sort_values('score', ascending=False)[['name', 'year', 'score']]
if not sorted_score.empty:
    print("Top 10 movies:")
    print(sorted_score.head(10))  
print("----------------------------------------------------------------------------------------")

