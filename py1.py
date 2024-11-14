import pandas
import sqlalchemy
import  urllib

orders = pandas.read_csv("C:\\Users\\chowvij\\Downloads\\orders.csv",na_values=[ 'Not Available', 'unknown'])
# print(orders["Ship Mode"].unique())
orders = orders.rename(columns = {"Ship Mode" : "ship_mode", "City": "city"}) ## chnage col from upper to lower

## change the spaces with underscore (_)
orders.columns = orders.columns.str.replace(" ", "_")

## craete a new col discount with list price * discount percent * 0.1
orders["discount"] = orders["List_Price"] * orders["Discount_Percent"] * 0.1
# print(orders)

## noe craete a new col sale price using the list price - discount

orders["sale_price"] = orders["List_Price"] - orders["discount"]

# ## find the profit cost_price - cost_price

# orders["profit"] =  orders("sale_price") - orders["cost_price"]

orders["profit"] = orders["cost_price"] - orders["sale_price"]

## drop list_price, cost_price and discount percent columns
orders = orders.drop(columns = ["cost_price", "List_Price","Discount_Percent" ])



## convert the order date as date

orders["Order_Date"] = pandas.to_datetime(orders["Order_Date"], format = "%Y-%m-%d")
# print(orders.dtypes)
print(orders.columns)

## load the data to SQL Server
import sqlalchemy as sal
import urllib

# Correcting the connection string format
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=BHXNRULPWCCRIMB;"
    "DATABASE=TEST;"
    "Trusted_Connection=yes;"
)

# Creating the engine
engine = sal.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Establishing the connection
conn = engine.connect()


## loda data into sql server
orders.to_sql ("to_orders", con = conn, index = False, if_exists= "replace")
## it will create the table in SQL SERVER