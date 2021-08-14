import gzip
import json
import pandas as pd
import itertools
import numpy as np

# Read file path
file_path = "/Users/barboraspacilova/Documents/DATA/LEARN/Python/WeFarm/" \
            "barbora-we-farm/data/vouchers/vouchers-2019-11-01.json.gz"

# Open single json to dataframe
with gzip.open(file_path, "r") as file:
   voucher_file = file.read()
   json_voucher = json.loads(voucher_file)
   voucher_rows = list(json_voucher.values())[0]
   voucher_df = pd.DataFrame(voucher_rows)

# Explore the df
print(voucher_df.info())
print(voucher_df.shape)
print(voucher_df.head())

#Explore unique values
print(voucher_df['product'].unique())
print(voucher_df['status'].unique())
print(np.unique([*itertools.chain.from_iterable(voucher_df.vendor)]))
