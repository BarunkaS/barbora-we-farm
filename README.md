# barbora-we-farm

## To-Do

1. DONE - Setup venv, install pandas, gz reader, json reader, time, psycopg2
2. DONE - Load a single file, check for structure
3. DONE - Develop final schema
4. DONE - Created PostgreSQL to save to 
5. DONE - Separate file for db setup
6. Load json to the db
    - DONE - Load products to db
    - DONE - Load vendors to db
    - DONE - Change codes data with product_id
    - Load {code: list of vendors} in a dict
    - Load vendor names and ids in a dict
    - Replace items in each list of vendors with IDs from vendor dict
    - Populate code_vendor to db (for each list item, insert code and item)
7. Create reusability
8. Separate code for readability
9. DONE - Load all files
10. Consistency and integrity testing (??)
11. Solve for errors and exceptions where needed (wrong file format in folder?,...)
12. Document readme - steps for installation and/or any dependencies, instructions on running/building

**Next step:** Load {code: list of vendors} in a dict

## Setting up PostgreSQL


 
