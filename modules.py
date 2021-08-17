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