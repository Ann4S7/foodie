# TODO improve naming
# TODO add the ability to remove products
# TODO add the ability to display products


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

    def get(self, column, product_id=None, product=None):
        with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                    host="localhost", port=5432) as cursor:
            if product_id:
                cursor.execute(f"SELECT {column} FROM products WHERE product_id = '{product_id}';")
            else:
                cursor.execute(f"SELECT {column} FROM products "
                               f"WHERE name = '{product.name}' AND expiry_date = '{product.expiry_date}';")

            return cursor.fetchall()

    def add(self, product):
        with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                    host="localhost", port=5432) as cursor:

            cursor.execute(f"INSERT INTO products(category, name, expiry_date, quantity)"
                           f"VALUES('{product.CATEGORY}', '{product.name}',"
                           f"'{product.expiry_date}', {product.quantity});")

    def update(self, product_id=None, quantity=None, product=None):
        with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                    host="localhost", port=5432) as cursor:

            if product_id:
                cursor.execute(f"UPDATE products SET quantity = quantity + {quantity} "
                               f"WHERE product_id = '{product_id}';")
            else:
                cursor.execute(f"UPDATE products SET quantity = quantity + {product.quantity} "
                               f"WHERE name = '{product.name}' AND expiry_date = '{product.expiry_date}';")

    def remove(self, product):
        with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                    host="localhost", port=5432) as cursor:

            cursor.execute(f"DELETE FROM products WHERE product_id = '{product}';")


def add_products(args):
    with open(args.json_file_add) as file:
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

            product_status = repo.get(column="product_id", product=product)

            if product_status:
                repo.update(product=product)
            else:
                repo.add(product)


def remove_products(args):
    with open(args.json_file_remove) as file:
        products_list = file.read()
        products_list = json.loads(products_list)

        for product_dict in products_list:
            quantity_used = product_dict.get("quantity", 1)
            product = product_dict["product_id"]

            repo = ProductRepository()

            product_status = repo.get(column="quantity", product_id=product)
            product_quantity = product_status[0][0]

            if product_quantity > quantity_used:
                repo.update(product_id=product, quantity=-quantity_used)
            else:
                repo.remove(product)
