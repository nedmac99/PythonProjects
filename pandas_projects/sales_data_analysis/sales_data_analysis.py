import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter
from pathlib import Path

#Objective
'''
-Analyze sales data to uncover trends, top-selling products, monthly revenue, and customer behavior.✅
-Load and clean the dataset✅
-Group sales by product and date✅
-Create new features like Total = Quantity * Price✅
-Filter top customers or products✅
-Handle missing values✅
'''

'''Load Data set'''

#Finds the file we want to use
file_path = Path(__file__).parent / "Sample - Superstore.csv"

#Loads database into variable called df(DataFrame)
df = pd.read_csv(file_path, encoding='ISO-8859-1')

#Information about DataFrame
print(df.info())

#Preview the top 5 entries
print(df.head())

'''Cleaning up the data'''

#Strip whitespaces from column names
df.columns = df.columns.str.strip()

#Check for missing values
print(f"Check for missing values: \n{df.isnull().sum()}")

#Drop missing values
df.dropna(inplace=True)

#Drop Duplicates
df.drop_duplicates(inplace=True)

#Convert dates to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

'''Group sales by Product and Date'''

#Group by product and order date
grouped = df.groupby(['Product Name', 'Order Date'])['Sales'].sum().reset_index()
print(grouped.head())

#Group by the Month by adding a 'Month' column
df['Month'] = df['Order Date'].dt.to_period('M')

'''Create New Features'''

#Create new column 'Total'
df['Total'] = df['Sales']

'''Grouping and Aggregation'''

#Group data by the product and month, then sum the sales
monthly_sales = df.groupby(['Product Name', 'Month'])['Sales'].sum().reset_index()

#Group data by the product name, sum the quantity sold, sort it in descending order, and finds the top 10 selling products
top_products = df.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(10)

#Group the data by customer, totals the sales per customer, Sort it in descending order, returns top 10 customers by revenue
top_customers = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10)
