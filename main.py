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

# Read all files
for file in daily_vouchers_paths:
    with gzip.open(file, "r") as file:
        voucher_file = file.read()
        json_voucher = json.loads(voucher_file)
        voucher_rows = list(json_voucher.values())[0]
        file_df = pd.DataFrame(voucher_rows)

        df_lenght = file_df.shape[0]
        print(df_lenght)




# Writing into the DB
"""postgres_insert_query = 'INSERT INTO public.vendors (vendor_id,vendor_name) VALUES (1,'kn')'

cursor.execute(postgres_insert_query)
postgres_connection.commit()"""