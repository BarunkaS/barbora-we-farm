import psycopg2
from os.path import join, dirname
import os
from dotenv import load_dotenv
import modules
import gzip

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
daily_vouchers_path = "data/vouchers/*"
codes_raw = modules.read_all_files(daily_vouchers_path)

# Getting unique products and vendors
products = modules.listing_dimensions(codes_raw,'product')
vendors = modules.listing_dimensions(codes_raw,'vendor')

# Inserting products and creating IDs
modules.insert_dimension_table(postgres_connection, cursor, insert_products, products)

# Inserting vendors and creating IDs
flattened_vendors = []

for sublist in vendors:
    for item in sublist:
        flattened_vendors.append(item)

modules.insert_dimension_table(postgres_connection, cursor, insert_vendors, flattened_vendors)

# Replace product with product_id, generate ID in codes
products_dict = modules.table_to_dict(cursor, select_products)

for item in codes_raw :
    for row in item:
        product = row['product']
        row['product_id'] = products_dict[product]
        row['id'] = abs(int(hash(row['voucher_code'])))
        row.pop('product')

# Populating code_vendor
vendors_dict = products_dict = modules.table_to_dict(cursor, select_vendors)
modules.populate_code_vendor(postgres_connection, cursor, insert_vendors_codes, codes_raw, vendors_dict)

# Populating codes
modules.populate_codes(postgres_connection, cursor, insert_codes, codes_raw)