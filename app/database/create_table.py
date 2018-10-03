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

queries = [table1, table2, table3]
