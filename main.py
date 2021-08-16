import gzip
import json
import psycopg2
from psycopg2 import Error
from datetime import datetime
import glob
from os.path import join, dirname
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import date

# Load DB credentials from environment
dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)
db_user = os.environ.get('WEFARM_USER')
db_pwd = os.environ.get('WEFARM_PWD')
db_host = os.environ.get('WEFARM_HOST')
db_port = os.environ.get('WEFARM_PORT')
db_db = os.environ.get('WEFARM_DB')

# Connect to PostgreSQL
postgres_connection = psycopg2.connect(user=db_user,
                              password=db_pwd,
                              host=db_host,
                              port=db_port,
                              database=db_db)

# Create cursor to perform database operations
cursor = postgres_connection.cursor()

# Read file paths
daily_vouchers_paths = glob.glob("data/vouchers/*")

# INSERT and SELECT queries
insert_codes = """INSERT INTO public.codes (id,voucher_code,user_id,product_id,status,date_added) 
                VALUES (%s,%s,%s,%s,%s,%s)"""
insert_products = """INSERT INTO public.products (product_id,product_name) 
                VALUES (%s,%s) ON CONFLICT DO NOTHING"""
insert_vendors = """INSERT INTO public.vendors (vendor_id,vendor_name) 
                VALUES (%s,%s) ON CONFLICT DO NOTHING"""
insert_vendors_codes = """INSERT INTO public.code_vendor (code_vendor_id,code_id,vendor_id) 
                VALUES (%s,%s,%s) ON CONFLICT DO NOTHING"""

select_products = """SELECT * FROM public.products"""
select_vendors = """SELECT * FROM public.vendors"""

# Read all files
all_voucher_rows = []
for file in daily_vouchers_paths:
    with gzip.open(file, "r") as file:
        voucher_file = file.read()
        json_voucher = json.loads(voucher_file)
        voucher_rows = list(json_voucher.values())[0]
        all_voucher_rows.append(voucher_rows)

# Data for modifications
codes_raw = all_voucher_rows

# Getting unique products and vendors
products = []
vendors = []

for item in all_voucher_rows:
    for row in item:
        products.append(row['product'])
        vendors.append(row['vendor'])

# Inserting products and creating IDs
unique_products = list(set(products))
product_ids = list(range(1,len(unique_products)+1))


for i in range(0,len(unique_products)):
    cursor.execute(insert_products,(product_ids[i],unique_products[i]))
    postgres_connection.commit()

# Inserting vendors and creating IDs
flattened_vendors = []

for sublist in vendors:
    for item in sublist:
        flattened_vendors.append(item)

unique_vendors = list(set(flattened_vendors))
vendor_ids = list(range(1,len(unique_vendors)+1))

for i in range(0,len(unique_vendors)):
    cursor.execute(insert_vendors,(vendor_ids[i],unique_vendors[i]))
    postgres_connection.commit()

# Replace product and vendor with IDs in codes_raw
# Products
cursor.execute(select_products)
result_products = cursor.fetchall()

products_reverted_dict = dict(result_products)
products_dict = { j:k for k,j in products_reverted_dict.items()}

for item in codes_raw:
    for row in item:
        product = row['product']
        row['product_id'] = products_dict[product]
        row['id'] = abs(int(hash(row['voucher_code'])))
        row.pop('product')

# Populating code_vendor
cursor.execute(select_vendors)
result_vendors = cursor.fetchall()

vendors_inverted_dict = dict(result_vendors)
vendors_dict = { j:k for k,j in vendors_inverted_dict.items()}

for item in codes_raw:
    for row in item:
        vendors = row['vendor']
        code = row['id']
        i = 0
        for item in vendors:
            vendor = vendors[i]
            cursor.execute(insert_vendors_codes,(code,vendors_dict[vendor]))
            postgres_connection.commit()
            i+=1

# Inserting into codes
for item in codes_raw:
    for row in item:
        voucher_code = row['voucher_code']
        user_id = row['user_id']
        product_id = row['product_id']
        status = row['status']
        date_added = date.today()
        id = abs(int(hash(row['voucher_code'])))

        cursor.execute(insert_codes,(id,voucher_code,user_id,product_id,status,date_added))
        postgres_connection.commit()
