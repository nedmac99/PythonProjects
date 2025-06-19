import pandas as pd
from pathlib import Path


#Reading data from dataset
file_path = Path(__file__).parent / "Superstore.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

#Verifying it's reading correctly
#print(f"First 5 entries to data set: \n{df.head()}\n")
#df.info()

#Cleaning the data
'''
#Already ran df.columns = df.columns.str.strip() to clean up white spaces around column names
#print(df.columns)
'''
#Need to change the order and ship date from oject types to datetime types
#print(df.dtypes)