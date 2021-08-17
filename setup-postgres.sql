-- Creating DB, role and granting read privilege
CREATE DATABASE wefarmdb;
CREATE ROLE wefarm WITH LOGIN PASSWORD 'password';
GRANT pg_read_server_files TO wefarm;

-- Creating schema (for more info refer to README.md)
-- Contains tables codes, users (only for showcase, remains empty), products, code_vendor, vendor

CREATE TABLE IF NOT EXISTS public.codes
(
    id bigint NOT NULL,
    voucher_code text,
    user_id integer,
    product_id integer,
    status text,
    date_added date,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.products
(
    product_id integer NOT NULL,
    product_name text,
    PRIMARY KEY (product_id)
);

CREATE TABLE IF NOT EXISTS public.code_vendor
(
    code_id bigint NOT NULL,
    vendor_id integer,
    PRIMARY KEY (voucher_vendor_id),
    CONSTRAINT voucher_vendor_id FOREIGN KEY (voucher_vendor_id)
        REFERENCES public.codes (code_vendor_id) MATCH SIMPLE
);

CREATE TABLE IF NOT EXISTS public.vendor
(
    vendor_id integer NOT NULL,
	vendor_name text,
    PRIMARY KEY (vendor_id)
);

