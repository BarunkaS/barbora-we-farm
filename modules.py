import gzip
import json
import glob
from datetime import date

# Reads all files and saves data in a list
def read_all_files(folder_path):
    all_voucher_rows = []
    # Read file paths
    daily_vouchers_paths = glob.glob(folder_path)
    #Read files
    for file in daily_vouchers_paths:
        try:
            with gzip.open(file, "r") as file:
                voucher_file = file.read()
                json_voucher = json.loads(voucher_file)
                voucher_rows = list(json_voucher.values())[0]
                all_voucher_rows.append(voucher_rows)
        except(gzip.BadGzipFile):
            pass
    return all_voucher_rows

# Takes dimensional data from full dataset and creates a list of them
def listing_dimensions(dataset,dimension_name):
    dimension_list = []
    for item in dataset:
        for row in item:
            dimension_list.append(row[dimension_name])
    return dimension_list

# Takes list of unique dimensions and inserts into dimensional (peripheral) table
def insert_dimension_table(postgres_connection, cursor, insert_query, dimension_list):
    unique_items = list(set(dimension_list))
    item_ids = list(range(1,len(unique_items)+1))

    for i in range(0,len(unique_items)):
        cursor.execute(insert_query,(item_ids[i],unique_items[i]))
        postgres_connection.commit()
    return None

# Retrieves data from dimensional table and creates a dictionary
# Used for mathing ids in the codes table
def table_to_dict(cursor, select_statement):
    cursor.execute(select_statement)
    query_result = cursor.fetchall()

    inverted_dict = dict(query_result)
    final_dict = { j:k for k,j in inverted_dict.items()}
    return final_dict

# Takes full dataset and populates the code_vendor table
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

# Takes full dataset and populates the codes table
def populate_codes(postgres_connection, cursor, insert_statement, dataset):
    for item in dataset:
        for row in item:
            voucher_code = row['voucher_code']
            user_id = row['user_id']
            product_id = row['product_id']
            status = row['status']
            date_added = date.today()
            id = abs(int(hash(row['voucher_code'])))

            cursor.execute(insert_statement,(id,voucher_code,user_id,product_id,status,date_added))
            postgres_connection.commit()