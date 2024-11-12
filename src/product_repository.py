import json
import os
from argparse import Namespace
from datetime import date
from typing import Optional

import products
from conflog import logger
from database_context_manager import DatabaseContextManager
from utils import calculate_date


class Repository:
    """The generic class defining what methods the child class should have."""

    def get(self, *args, **kwargs):
        """Get the row from database by id."""
        raise NotImplementedError

    def search(self, *args, **kwargs):
        """Get the row from database by name and expiry date."""
        raise NotImplementedError

    def add(self, *args, **kwargs):
        """Add the row to database."""
        raise NotImplementedError

    def update(self, *args, **kwargs):
        """Update the row in database."""
        raise NotImplementedError

    def remove(self, *args, **kwargs):
        """Remove the row from database."""
        raise NotImplementedError

    def count(self, *args, **kwargs):
        """Count the rows."""
        raise NotImplementedError


class ProductRepository(Repository):
    """The class has instance methods that contain database queries."""

    def __init__(
        self,
        database: Optional[str] = None,
        user: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        password: Optional[str] = None,
    ):
        self.database = database or os.environ.get("DB_NAME")
        self.user = user or os.environ.get("DB_USER")
        self.password = password or os.environ.get("DB_PASSWORD")
        self.host = host or os.environ.get("DB_HOST")
        self.port = port or int(os.environ.get("DB_PORT"))

    def get(self, product_id: int) -> Optional[products.Product]:
        """Retrieve from the table one-element list of tuples.
        The tuple contains the parameters of the product with specific id.
        These parameters are used to create the instance of the class
        that inherits from the Product class.

        Args:
            product_id: id of the product.

        Returns: the instance of the class that inherits from the Product class
            or None (if there is no product with specific id in the table).

        """
        with DatabaseContextManager(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        ) as cursor:

            logger.info(
                "Getting product...",
                extra={"extra_parameters": {"product_id": product_id}},
            )

            cursor.execute(
                f"SELECT category, name, expiry_date, quantity FROM products "
                f"WHERE product_id = '{product_id}';"
            )

            products_list = cursor.fetchall()

            if products_list:
                product_tuple = products_list[0]
                product_class = get_product_class(product_tuple[0])
                product = product_class(
                    product_tuple[1], product_tuple[2], product_tuple[3]
                )
                logger.info("Getting product is completed.")
            else:
                product = None
                logger.error(
                    "Product not found.",
                    extra={"extra_parameters": {"product_id": product_id}},
                )

            return product

    def search(
        self,
        conditions: Optional[dict] = None,
        columns: str = "*",
        limit: Optional[int] = None,
    ) -> list[tuple]:
        """Search the records in the table by specific conditions.

        Args:
            conditions: can specify parameters of the products to be retrieved from the table.
            columns: can specify columns with the product parameters to be retrieved from the table.
            limit: can specify limit of the records to be retrieved from the table.

        Returns: list of the tuples that contain product parameters (the list can be empty)

        """
        with DatabaseContextManager(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        ) as cursor:

            logger.info(
                "Searching products...",
                extra={
                    "extra_parameters": {
                        "conditions": conditions,
                        "columns": columns,
                        "limit": limit,
                    }
                },
            )

            query = f"SELECT {columns} FROM products"

            if conditions:
                where_conditions = []
                for attribute_name, attribute_value in conditions.items():
                    if isinstance(attribute_value, dict):
                        where_conditions.append(
                            f"{attribute_name} {attribute_value.get("operator")}"
                            f" '{attribute_value.get("value")}'"
                        )
                    else:
                        where_conditions.append(
                            f"{attribute_name} = '{attribute_value}'"
                        )
                query += " WHERE " + " AND ".join(where_conditions)

            if limit:
                query += f" LIMIT {limit}"

            cursor.execute(query)

            logger.info("Search completed.")

            return cursor.fetchall()

    def get_by_name_and_date(self, name: str, expiry_date: date) -> list[tuple]:
        """Retrieve a product with a specific name and expiry date from the table.

        Args:
            name: product name.
            expiry_date: product expiry date.

        Returns: list of the tuples that contain product parameters
            (the list can contain one tuple or be empty)

        """
        product = self.search(conditions={"name": name, "expiry_date": expiry_date})

        if len(product) > 1:
            logger.warning(
                "There are more than 1 rows in the database storing the same product.",
                extra={"extra_parameters": {"name": name, "expiry_date": expiry_date}},
            )

        return product

    def add(self, product: products.Product) -> None:
        """Take the instance of the class that inherits from the Product class.
        Its attributes are used to create the new record in the table.

        Args:
            product: the instance of the class that inherits from the Product class.

        """
        with DatabaseContextManager(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        ) as cursor:

            logger.info(
                "Adding product...",
                extra={
                    "extra_parameters": {
                        "category": product.CATEGORY,
                        "name": product.name,
                        "expiry_date": product.expiry_date,
                        "quantity": product.quantity,
                    }
                },
            )

            cursor.execute(
                f"INSERT INTO products(category, name, expiry_date, quantity)"
                f"VALUES('{product.CATEGORY}', '{product.name}',"
                f"'{product.expiry_date}', {product.quantity});"
            )

            logger.info("Adding completed.")

    def update(self, product: products.Product) -> None:
        """Update the quantity of the product with a specific name and expiry date.

        Args:
            product: the instance of the class that inherits from the Product class.

        """
        with DatabaseContextManager(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        ) as cursor:

            logger.info(
                "Updating quantity of the product...",
                extra={
                    "extra_parameters": {
                        "category": product.CATEGORY,
                        "name": product.name,
                        "expiry_date": product.expiry_date,
                        "quantity": product.quantity,
                    }
                },
            )

            cursor.execute(
                f"UPDATE products SET quantity = {product.quantity} "
                f"WHERE name = '{product.name}' AND expiry_date = '{product.expiry_date}';"
            )

            logger.info("Updating completed.")

    def remove(self, product_id: int) -> None:
        """Remove the product with a specific id from the table.

        Args:
            product_id: id of the product.

        """
        with DatabaseContextManager(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        ) as cursor:

            logger.info(
                "Removing product...",
                extra={"extra_parameters": {"product_id": product_id}},
            )

            cursor.execute(f"DELETE FROM products WHERE product_id = '{product_id}';")

            logger.info("Removing completed.")

    def count(self) -> int:
        """Count all records in the table.

        Returns: number of records in the table.

        """
        with DatabaseContextManager(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        ) as cursor:

            logger.info("Counting all products...")

            cursor.execute("SELECT COUNT (*) FROM products;")

            logger.info("Counting completed.")

            return cursor.fetchall()[0][0]


def get_product_class(category: str) -> type(products.Product):
    """Match a product class based on category name.

    Args:
        category: name of the product category.

    Returns:
        Product class or class that inherits from the Product class.

    """
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
            logger.warning(
                "Invalid product category.",
                extra={"extra_parameters": {"category": category}},
            )

    return product_class


def add_products(args: Namespace) -> None:
    """Add products that have been purchased.
    Update the quantity of the stored product or create new record.

    Args:
        args: an object holding the json_file_add attribute.
            This attribute allows to pass the file containing
            parameters of the products that have been purchased.

    """
    with open(args.json_file_add, encoding="utf-8") as file:
        products_list = file.read()
        products_list = json.loads(products_list)

        repo = ProductRepository()

        for product_dict in products_list:
            product_class = get_product_class(product_dict["category"])
            if product_class != products.Product:
                product = product_class(
                    product_dict["name"],
                    product_dict.get("expiry_date")
                    or calculate_date(product_dict["freshness_in_days"]),
                    product_dict.get("quantity"),
                )

                found_product = repo.get_by_name_and_date(
                    product.name, product.expiry_date
                )

                if found_product:
                    # product_status is one-element list of tuples
                    # the last element of the tuple is quantity value
                    product.quantity = product.quantity + found_product[0][-1]
                    repo.update(product)
                else:
                    repo.add(product)


def remove_products(args: Namespace) -> None:
    """Check the availability of the product with a given id. Remove used product.

    Args:
        args: an object holding the json_file_remove attribute.
            This attribute allows to pass the file containing
            product_id and the quantity of the products that have been used.

    """
    with open(args.json_file_remove, encoding="utf-8") as file:
        products_list = file.read()
        products_list = json.loads(products_list)

        repo = ProductRepository()

        for product_dict in products_list:
            product_id = product_dict["product_id"]

            product = repo.get(product_id)

            if product:
                quantity_used = product_dict.get("quantity", product.DEFAULT_QUANTITY)
                if product.quantity > quantity_used:
                    product.quantity = product.quantity - quantity_used
                    repo.update(product)
                else:
                    repo.remove(product_id)


def display_products(args: Namespace) -> list[tuple]:
    """Display products that meet the search criteria.

    Args:
        args: an object holding the json_file_display attribute.
            This attribute allows to pass the file containing
            parameters used in the search method.

    Returns:
        List of the tuples which contain product's parameters. The list can be empty.

    """
    with open(args.json_file_display, encoding="utf-8") as file:
        request_body = file.read()
        request_body = json.loads(request_body)

        repo = ProductRepository()
        result = repo.search(
            conditions=request_body.get("conditions"),
            columns=request_body.get("columns", "*"),
            limit=request_body.get("limit"),
        )

        return result
