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

    def get(self, cursor, new_product):
        cursor.execute(f"SELECT * FROM products "
                       f"WHERE name = '{new_product.name}' AND expiry_date = '{new_product.expiry_date}';")

    def add(self, cursor, new_product):
        cursor.execute(f"INSERT INTO products(category, name, expiry_date, quantity)"
                       f"VALUES('{new_product.CATEGORY}', '{new_product.name}',"
                       f"'{new_product.expiry_date}', {new_product.quantity});")

    def update(self, cursor, new_product):
        cursor.execute(f"UPDATE products SET quantity = quantity + {new_product.quantity} "
                       f"WHERE name = '{new_product.name}' AND expiry_date = '{new_product.expiry_date}';")


def add_products(json_file):
    with open(json_file) as file:
        all_products = file.read()
        all_products = json.loads(all_products)

        for product in all_products:
            match product["product"]:
                case "fruit":
                    new_product = products.Fruit(product["name"], product["freshness_in_days"],
                                                 product.get("quantity"))

                case "vegetable":
                    new_product = products.Vegetable(product["name"], product["freshness_in_days"],
                                                     product.get("quantity"))

                case "dairy":
                    new_product = products.Dairy(product["name"], product["expiry_date"], product.get("quantity"))

                case "meat":
                    new_product = products.Meat(product["name"], product["expiry_date"], product.get("quantity"))

                case "grain":
                    new_product = products.Grain(product["name"], product["expiry_date"], product.get("quantity"))

            with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                        host="localhost", port=5432) as cursor:

                ProductRepository().get(cursor, new_product)

                product_status = cursor.fetchall()

                if not product_status:
                    ProductRepository().add(cursor, new_product)
                else:
                    ProductRepository().update(cursor, new_product)
