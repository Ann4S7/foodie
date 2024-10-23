from database_context_manager import DatabaseContextManager


def create_table(database, user, password, host, port):
    with DatabaseContextManager(
        database=database, user=user, password=password, host=host, port=port
    ) as cursor:

        cursor.execute(
            "CREATE TABLE products("
            "product_id SERIAL PRIMARY KEY, "
            "category VARCHAR(50) NOT NULL, "
            "name VARCHAR(50) NOT NULL, "
            "expiry_date date NOT NULL, "
            "quantity INTEGER);"
        )


def drop_table(database, user, password, host, port):
    with DatabaseContextManager(
        database=database, user=user, password=password, host=host, port=port
    ) as cursor:

        cursor.execute("DROP TABLE products;")
