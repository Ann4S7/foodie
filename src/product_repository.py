import json
import os
from argparse import Namespace
from typing import Optional
from conflog import logger

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

    def __init__(self, database: Optional[str] = None, user: Optional[str] = None, host: Optional[str] = None,
                 port: Optional[int] = None, password: Optional[str] = None):
        self.database = database or os.environ.get("DB_NAME")
        self.user = user or os.environ.get("DB_USER")
        self.password = password or os.environ.get("DB_PASSWORD")
        self.host = host or os.environ.get("DB_HOST")
        self.port = port or int(os.environ.get("DB_PORT"))

    def get(self, product_id: int) -> products.Product:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            logger.info(f"Getting product (id={product_id})...",
                        extra={"extra_parameters": {"product_id": product_id}})

            cursor.execute(f"SELECT category, name, expiry_date, quantity FROM products "
                           f"WHERE product_id = '{product_id}';")

            logger.info(f"Getting product is completed.")

            products_list = cursor.fetchall()

            product_tuple = products_list[0]
            product_class = get_product_class(product_tuple[0])
            product = product_class(product_tuple[1],
                                    product_tuple[2],
                                    product_tuple[3])

            return product

    def search(self, conditions: Optional[dict] = None, columns: str = "*", limit: Optional[int] = None) -> list[tuple]:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            logger.info(f"Searching products...",
                        extra={"extra_parameters": {"conditions": conditions, "columns": columns, "limit": limit}})

            query = f"SELECT {columns} FROM products"

            if conditions:
                where_conditions = []
                for attribute_name, attribute_value in conditions.items():
                    if isinstance(attribute_value, dict):
                        where_conditions.append(f"{attribute_name} {attribute_value.get("operator")}"
                                                f" '{attribute_value.get("value")}'")
                    else:
                        where_conditions.append(f"{attribute_name} = '{attribute_value}'")

                query += " WHERE " + " AND ".join(where_conditions)

            if limit:
                query += f" LIMIT {limit}"

            cursor.execute(query)

            logger.info(f"Search completed.")

            return cursor.fetchall()

    def add(self, product: products.Product) -> None:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            logger.info(f"Adding product {product}...",
                        extra={"extra_parameters": {"category": product.CATEGORY, "name": product.name,
                                                    "expiry_date": product.expiry_date, "quantity": product.quantity}})

            cursor.execute(f"INSERT INTO products(category, name, expiry_date, quantity)"
                           f"VALUES('{product.CATEGORY}', '{product.name}',"
                           f"'{product.expiry_date}', {product.quantity});")

            logger.info(f"Adding completed.")

    def update(self, product: products.Product) -> None:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            logger.info(f"Updating quantity of the product: {product.name} - {product.expiry_date}...",
                        extra={"extra_parameters": {"category": product.CATEGORY, "name": product.name,
                                                    "expiry_date": product.expiry_date, "quantity": product.quantity}})

            cursor.execute(f"UPDATE products SET quantity = {product.quantity} "
                           f"WHERE name = '{product.name}' AND expiry_date = '{product.expiry_date}';")

            logger.info(f"Updating completed.")

    def remove(self, product_id: int) -> None:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            logger.info(f"Removing product (id={product_id})...",
                        extra={"extra_parameters": {"product_id": product_id}})

            cursor.execute(f"DELETE FROM products WHERE product_id = '{product_id}';")

            logger.info(f"Removing completed.")

    def count(self) -> int:
        with DatabaseContextManager(database=self.database, user=self.user, password=self.password,
                                    host=self.host, port=self.port) as cursor:

            logger.info("Counting all products...")

            cursor.execute(f"SELECT COUNT (*) FROM products;")

            logger.info(f"Counting completed.")

            return cursor.fetchall()[0][0]


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

            repo = ProductRepository()

            product_status = repo.search(conditions={"name": product.name, "expiry_date": product.expiry_date})

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

            repo = ProductRepository()

            product = repo.get(product_id)

            quantity_used = product_dict.get("quantity", product.DEFAULT_QUANTITY)

            if product.quantity > quantity_used:
                product.quantity = product.quantity - quantity_used
                repo.update(product)
            else:
                repo.remove(product_id)


def display_products(args: Namespace) -> list[tuple]:
    with open(args.json_file_display) as file:
        request_body = file.read()
        request_body = json.loads(request_body)

        repo = ProductRepository()

        result = repo.search(conditions=request_body.get("conditions"), columns=request_body.get("columns", "*"),
                             limit=request_body.get("limit"))

        return result
