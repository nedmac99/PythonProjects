import pandas as pd
from pathlib import Path

file_path = Path(__file__).parent / "gaming_mental_health_data.csv"

df = pd.read_csv(file_path)

#print(df.head())
#df.info()

#Goals (Also check Kaggle for more info)
'''
Predict depression_score using gaming behavior features
Detect high addiction_level individuals
Model causal pathways: gaming → sleep → mental health → productivity
Cluster gamer behavioral profiles
Large-scale distributed training benchmarking
'''


#Convert gender to int from str. check pandas projects for how to convert
#Clean dataset
'''
-Remove null values
-Remove duplicates
-Confirm useable data types
-Column name cleaning(str.strip() str.lower())
-Spot potential wrong data(incorrect entries)
-Feature engineering(create new columns based on exsisting data)
'''