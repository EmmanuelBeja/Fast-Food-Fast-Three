"""tables script"""

table1 = """CREATE TABLE IF NOT EXISTS tbl_users(
	userid  serial PRIMARY KEY,
	username varchar(25) UNIQUE NOT NULL,
    userphone varchar(25) UNIQUE NOT NULL,
    password varchar(25) NOT NULL,
    userRole varchar(25) NOT NULL DEFAULT 'client',
	createddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""

table2 = """CREATE TABLE IF NOT EXISTS tbl_orders(
	order_id serial PRIMARY KEY,
	food_id int NOT NULL,
    client_id int NOT NULL,
	client_adress varchar(25) NOT NULL,
    status varchar(25) NOT NULL,
	createddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""


table3 = """CREATE TABLE IF NOT EXISTS tbl_foods(
	food_id serial PRIMARY KEY,
	food_name varchar (25) NOT NULL,
    food_price varchar(25) NOT NULL,
    food_image varchar(25) NOT NULL,
	createddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""

table4 = """CREATE TABLE IF NOT EXISTS tbl_auth_tokens(
	token_id serial PRIMARY KEY,
	token text  NOT NULL,
    status varchar(25) NOT NULL DEFAULT 'active',
	blacklist_dy varchar(25) DEFAULT NULL,
	createddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""

data1 = """ SELECT*FROM tbl_users;"""
data2 = """ SELECT*FROM tbl_orders;"""
data3 = """ SELECT*FROM tbl_foods;"""

queries = [table1, table2, table3, table4]
foods = [data1, data2, data3]
