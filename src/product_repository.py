# TODO improve naming
# TODO add the ability to display products


import json
import os
from argparse import Namespace
from datetime import date

from database_context_manager import DatabaseContextManager
import products
from utils import calculate_date


class Repository:

    def get(self, *args, **kwargs):
        """Get the row from database by id."""
        raise NotImplemented

    def search(self, *args, **kwargs):
        """Get the row from database by name and expiry date."""
        raise NotImplemented

    def add(self, *args, **kwargs):
        """Add the row to database."""
        raise NotImplemented

    def update(self, *args, **kwargs):
        """Update the row in database."""
        raise NotImplemented

    def remove(self, *args, **kwargs):
        """Remove the row from database."""
        raise NotImplemented

    def count(self, *args, **kwargs):
        """Count the rows."""
        raise NotImplemented


class ProductRepository(Repository):

    def __init__(self, database, user="postgres", host="localhost", port=5432, password=None):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get(self, product_id: int) -> products.Product:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            cursor.execute(f"SELECT category, name, expiry_date, quantity FROM products "
                           f"WHERE product_id = '{product_id}';")

            products_list = cursor.fetchall()

            product_tuple = products_list[0]
            product_class = get_product_class(product_tuple[0])
            product = product_class(product_tuple[1],
                                    product_tuple[2],
                                    product_tuple[3])

            return product

    def search(self, name: str, expiry_date: date) -> list[tuple]:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            cursor.execute(f"SELECT * FROM products "
                           f"WHERE name = '{name}' AND expiry_date = '{expiry_date}';")

            return cursor.fetchall()

    def add(self, product: products.Product) -> None:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            cursor.execute(f"INSERT INTO products(category, name, expiry_date, quantity)"
                           f"VALUES('{product.CATEGORY}', '{product.name}',"
                           f"'{product.expiry_date}', {product.quantity});")

    def update(self, product: products.Product) -> None:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            cursor.execute(f"UPDATE products SET quantity = {product.quantity} "
                           f"WHERE name = '{product.name}' AND expiry_date = '{product.expiry_date}';")

    def remove(self, product_id: int) -> None:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            cursor.execute(f"DELETE FROM products WHERE product_id = '{product_id}';")

    def count(self) -> int:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            cursor.execute(f"SELECT COUNT (*) FROM products;")

            return cursor.fetchall()[0][0]


def set_repository():
    return ProductRepository(
        database=os.environ.get("DB_NAME"),
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=int(os.environ.get("DB_PORT"))
    )


def get_product_class(category: str) -> type(products.Product):
    match category:
        case "fruit":
            product_class = products.Fruit
        case "vegetable":
            product_class = products.Vegetable
        case "dairy":
            product_class = products.Dairy
        case "meat":
            product_class = products.Meat
        case "grain":
            product_class = products.Grain
        case _:
            product_class = products.Product

    return product_class


def add_products(args: Namespace) -> None:
    with open(args.json_file_add) as file:
        products_list = file.read()
        products_list = json.loads(products_list)

        for product_dict in products_list:
            product_class = get_product_class(product_dict["category"])
            product = product_class(product_dict["name"],
                                    product_dict.get("expiry_date")
                                    or calculate_date(product_dict["freshness_in_days"]),
                                    product_dict.get("quantity"))

            repo = set_repository()

            product_status = repo.search(product.name, product.expiry_date)

            if product_status:
                # product_status is one-element list of tuples
                # the last element of the tuple is quantity value
                product.quantity = product.quantity + product_status[0][-1]
                repo.update(product)
            else:
                repo.add(product)


def remove_products(args: Namespace) -> None:
    with open(args.json_file_remove) as file:
        products_list = file.read()
        products_list = json.loads(products_list)

        for product_dict in products_list:
            product_id = product_dict["product_id"]

            repo = set_repository()

            product = repo.get(product_id)

            quantity_used = product_dict.get("quantity", product.DEFAULT_QUANTITY)

            if product.quantity > quantity_used:
                product.quantity = product.quantity - quantity_used
                repo.update(product)
            else:
                repo.remove(product_id)
