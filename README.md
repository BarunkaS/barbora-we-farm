# WeFarm voucher codes processing

Goal of this repository is to process raw voucher codes as coming from our platform to a PostgreSQL database.

The main scripting is using Python3.

### Final output

## Repository structure

### Repo contains:
- [Folders data/vouchers](data/vouchers) -  Separate files, one file is one day worth of vouchers. Includes a testing .txt file for exception handling
- [Postgres setup file](setup-postgres.sql) - Queries to set up the initial structure of target PostgreSQL databas
- [Main script](main.py)
- [Modules script](modules.py) - Contains all functions used in the main script
- [Requirements](requirements.txt)
- [Data exploration script](data-explore.py) - Not a functionality, butserves for user to be able to understand the underlying data structures.

## Setting up

### Set up environment

To install all needed modules use the requirements.txt file.
Install Python3 if needed.

Recommended: To avoid version and dependency issues, virtualize for installation.

### Set up PostgreSQL
1. Please set up an instance of PostgreSQL on a desired machine/service
2. Create run the setup-postgres.sql file to create a db schema
3. Create/update your .env file with credentials. Keep the following structure:

```
export WEFARM_USER =
export WEFARM_PWD =
export WEFARM_HOST =
export WEFARM_PORT = 5432
export WEFARM_DB =
```

## Running the application

To start script, run the main.py module.

That's it!


