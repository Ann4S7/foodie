from database_context_manager import DatabaseContextManager


def create_table(database, user, password, host, port):
    with DatabaseContextManager(database=database, user=user, password=password,
                                host=host, port=port) as cursor:

        cursor.execute(f"CREATE TABLE products("
                       f"product_id SERIAL PRIMARY KEY, "
                       f"category VARCHAR(50) NOT NULL, "
                       f"name VARCHAR(50) NOT NULL, "
                       f"expiry_date date NOT NULL, "
                       f"quantity INTEGER);")


def drop_table(database, user, password, host, port):
    with DatabaseContextManager(database=database, user=user, password=password,
                                host=host, port=port) as cursor:

        cursor.execute(f"DROP TABLE products;")
