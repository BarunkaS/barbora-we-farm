import gzip
import json
import pandas as pd
import itertools
import numpy as np
import glob

# Read file paths
daily_vouchers_paths = glob.glob("data/vouchers/*")

all_dataframes = []

for file in daily_vouchers_paths:
    with gzip.open(file, "r") as file:
        voucher_file = file.read()
        json_voucher = json.loads(voucher_file)
        voucher_rows = list(json_voucher.values())[0]
        file_df = pd.DataFrame(voucher_rows)
        all_dataframes.append(file_df)

#Open all files to dataframe
all_vouchers_df = pd.concat(all_dataframes)

# Create index
all_vouchers_df["id"] = all_vouchers_df.index

# Explore the df
print(all_vouchers_df.info())
print(all_vouchers_df.shape)
print(all_vouchers_df.head())

#Explore unique values
print(all_vouchers_df['product'].unique())
print(all_vouchers_df['status'].unique())
print(np.unique([*itertools.chain.from_iterable(all_vouchers_df.vendor)]))

# Question: Do codes historize based on status? - Answer seems to be no based on count values
voucher_cnt = all_vouchers_df.groupby('voucher_code')['id'].size()
print(voucher_cnt.sort_values(axis=0, ascending=False))

# Based on this exploration, final database schema is put together. For details, please refer to README.md