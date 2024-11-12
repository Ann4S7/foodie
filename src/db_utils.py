from database_context_manager import DatabaseContextManager


def create_products_table(
    database: str, user: str, password: str, host: str, port: int
) -> None:
    """Create the products table in the database.

    Args:
        database: database name.
        user: username.
        password: the user password.
        host: a server hostname that defines the location of the database server.
        port: a server port number.

    """
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


def drop_products_table(
    database: str, user: str, password: str, host: str, port: int
) -> None:
    """Remove the products table from the database.

    Args:
        database: database name.
        user: username.
        password: the user password.
        host: a server hostname that defines the location of the database server.
        port: a server port number.

    """
    with DatabaseContextManager(
        database=database, user=user, password=password, host=host, port=port
    ) as cursor:

        cursor.execute("DROP TABLE products;")
