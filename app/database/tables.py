"""tables script"""

table1 = """CREATE TABLE IF NOT EXISTS tbl_users(
	userid  serial PRIMARY KEY,
	username varchar(25) NOT NULL,
    userphone varchar(25) NOT NULL,
    password text NOT NULL,
    userRole varchar(25) NOT NULL DEFAULT 'client',
	createddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""

table2 = """CREATE TABLE IF NOT EXISTS tbl_orders(
	order_id serial PRIMARY KEY,
	food_id int NOT NULL,
    client_id int NOT NULL,
	client_adress varchar(25) NOT NULL,
	quantity varchar(25) NOT NULL DEFAULT '1',
    status varchar(25) NOT NULL,
	createddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""

table3 = """CREATE TABLE IF NOT EXISTS tbl_order_cache(
	id serial PRIMARY KEY,
	food_id int NOT NULL,
	food_name varchar(25) NOT NULL,
    client_id int NOT NULL,
	price varchar(25) NOT NULL,
	quantity varchar(25) NOT NULL DEFAULT '1',
    total varchar(25) NOT NULL,
	createddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""

table4 = """CREATE TABLE IF NOT EXISTS tbl_foods(
	food_id serial PRIMARY KEY,
	food_name varchar (25) NOT NULL,
    food_price varchar(25) NOT NULL,
    food_image varchar(25) NOT NULL,
	createddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""

table5 = """CREATE TABLE IF NOT EXISTS tbl_auth_tokens(
	token_id serial PRIMARY KEY,
	token text  NOT NULL,
    status varchar(25) NOT NULL DEFAULT 'active',
	blacklist_dy varchar(25) DEFAULT NULL,
	createddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""

queries = [table1, table2, table3, table4, table5]
