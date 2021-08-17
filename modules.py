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

def read_all_files(folder_path):
    all_voucher_rows = []
    # Read file paths
    daily_vouchers_paths = glob.glob(folder_path)
    #Read files
    for file in daily_vouchers_paths:
        with gzip.open(file, "r") as file:
            voucher_file = file.read()
            json_voucher = json.loads(voucher_file)
            voucher_rows = list(json_voucher.values())[0]
            all_voucher_rows.append(voucher_rows)
    return all_voucher_rows

def listing_dimensions(dataset,dimension_name):
    dimension_list = []
    for item in dataset:
        for row in item:
            dimension_list.append(row[dimension_name])
    return dimension_list

def insert_dimension_table(postgres_connection, cursor, insert_query, dimension_list):
    unique_items = list(set(dimension_list))
    item_ids = list(range(1,len(unique_items)+1))

    for i in range(0,len(unique_items)):
        cursor.execute(insert_query,(item_ids[i],unique_items[i]))
        postgres_connection.commit()
    return None

def table_to_dict(cursor, select_statement):
    cursor.execute(select_statement)
    query_result = cursor.fetchall()

    inverted_dict = dict(query_result)
    final_dict = { j:k for k,j in inverted_dict.items()}
    return final_dict

def populate_code_vendor(postgres_connection, cursor, insert_statement, dataset, dimension_dict):
    for item in dataset:
        for row in item:
            vendors = row['vendor']
            code = row['id']
            i = 0
            for item in vendors:
                vendor = vendors[i]
                cursor.execute(insert_statement,(code+dimension_dict[vendor],code,dimension_dict[vendor]))
                postgres_connection.commit()
                i+=1