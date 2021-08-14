import gzip
import json
import psycopg2
from psycopg2 import Error
from datetime import datetime
import glob
from os.path import join, dirname
import os
from dotenv import load_dotenv

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

# Create a cursor to perform database operations
cursor = postgres_connection.cursor()

postgres_insert_query = """ INSERT INTO public.vendors (vendor_id,vendor_name) VALUES (1,'kn')"""

cursor.execute(postgres_insert_query)
postgres_connection.commit() 

# Read file paths
#daily_vouchers_paths = glob.glob("data/vouchers/*")

