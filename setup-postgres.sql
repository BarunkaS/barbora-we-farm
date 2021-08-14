CREATE DATABASE wefarmdb;
CREATE ROLE wefarm WITH LOGIN PASSWORD 'password';
GRANT pg_read_server_files TO wefarm;