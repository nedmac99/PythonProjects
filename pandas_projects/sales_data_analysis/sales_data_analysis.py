import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter
from pathlib import Path

#Objective
'''
-Analyze sales data to uncover trends, top-selling products, monthly revenue, and customer behavior.
-Load and clean the dataset
-Group sales by product and date
-Create new features like Total = Quantity * Price
-Filter top customers or products
-Handle missing values
'''

file_path = Path(__file__).parent / "Sample - Superstore.csv"


df = pd.read_csv(file_path,encoding='ISO-8859-1')

#Details about dataframe
print(df.info()) 
#Preview Data
print(df.head(10))

new_df = df.dropna()

print(new_df.head(10))








#Example code

'''
df['Order Date'] = pd.to_datetime(df['Order Date'])
# Monthly sales trends
monthly_sales = df.groupby(pd.Grouper(key='Order Date', freq='M'))['Sales'].sum()

# Top 5 products
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5)

print("Monthly Sales:\n", monthly_sales)
print("\nTop 5 Products:\n", top_products)
'''