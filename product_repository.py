# TODO improve naming
# TODO add the ability to remove products
# TODO add the ability to display products
# TODO storing many of the same products with different dates


import json

from database_context_manager import DatabaseContextManager
import products


class Repository:

    def get(self, *args, **kwargs):
        """Get the row from database."""
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


class ProductRepository(Repository):

    def get(self, product):
        with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                    host="localhost", port=5432) as cursor:

            cursor.execute(f"SELECT * FROM products "
                           f"WHERE name = '{product.name}' AND expiry_date = '{product.expiry_date}';")

            return cursor.fetchall()

    def add(self, product):
        with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                    host="localhost", port=5432) as cursor:

            cursor.execute(f"INSERT INTO products(category, name, expiry_date, quantity)"
                           f"VALUES('{product.CATEGORY}', '{product.name}',"
                           f"'{product.expiry_date}', {product.quantity});")

    def update(self, product):
        with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                    host="localhost", port=5432) as cursor:

            cursor.execute(f"UPDATE products SET quantity = quantity + {product.quantity} "
                           f"WHERE name = '{product.name}' AND expiry_date = '{product.expiry_date}';")


def add_products(json_file):
    with open(json_file) as file:
        products_list = file.read()
        products_list = json.loads(products_list)

        for product_dict in products_list:
            match product_dict["product"]:
                case "fruit":
                    product = products.Fruit(product_dict["name"], product_dict["freshness_in_days"],
                                             product_dict.get("quantity"))

                case "vegetable":
                    product = products.Vegetable(product_dict["name"], product_dict["freshness_in_days"],
                                                 product_dict.get("quantity"))

                case "dairy":
                    product = products.Dairy(product_dict["name"], product_dict["expiry_date"],
                                             product_dict.get("quantity"))

                case "meat":
                    product = products.Meat(product_dict["name"], product_dict["expiry_date"],
                                            product_dict.get("quantity"))

                case "grain":
                    product = products.Grain(product_dict["name"], product_dict["expiry_date"],
                                             product_dict.get("quantity"))

            repo = ProductRepository()

            product_status = repo.get(product)

            if product_status:
                repo.update(product)
            else:
                repo.add(product)
