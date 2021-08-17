# WeFarm voucher codes processing

Goal of this repository is to process raw voucher codes as coming from our platform to a PostgreSQL database.

### Final output

## Repository structure

### Repo contains:
- [Folders data/vouchers](data/vouchers) -  Separate files, one file is one day worth of vouchers
- [Postgres setup file](setup-postgres.sql) - Contains queries that set up the initial structure of target PostgreSQL databas
- [Main script](main.py)
- [Requirements](requirements.txt)

## Setting up


## To-Do

1. DONE - Setup venv, install pandas, gz reader, json reader, time, psycopg2
2. DONE - Load a single file, check for structure
3. DONE - Develop final schema
4. DONE - Created PostgreSQL to save to 
5. DONE - Separate file for db setup
6. DONE - Load json to the db
    - DONE - Load products to db
    - DONE - Load vendors to db
    - DONE - Change codes data with product_id
    - DONE - Load {code: list of vendors} in a dict
    - DONE - Load vendor names and ids in a dict
    - DONE - Replace items in each list of vendors with IDs from vendor dict
    - DONE - Populate code_vendor to db (for each list item, insert code and item)
7. DONE - Create reusability
8. DONE - Separate code for readability
9. DONE - Load all files
10. Consistency and integrity testing (??)
11. Solve for errors and exceptions where needed (wrong file format in folder?,...)
12. Document readme - steps for installation and/or any dependencies, instructions on running/building

**Next step:** Code reusability & split for readability

## Setting up PostgreSQL


 
