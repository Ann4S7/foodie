# TODO improve naming
# TODO add the ability to display products


import json

from database_context_manager import DatabaseContextManager
import products


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


class ProductRepository(Repository):

    def get(self, product_id):
        with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                    host="localhost", port=5432) as cursor:

            cursor.execute(f"SELECT category, name, expiry_date, quantity FROM products "
                           f"WHERE product_id = '{product_id}';")

            products_list = cursor.fetchall()

            for product_tuple in products_list:
                product_class = get_product_class(product_tuple[0])
                product = product_class(product_tuple[1],
                                        product_tuple[2],
                                        product_tuple[3])

            return product

    def search(self, product):
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

            cursor.execute(f"UPDATE products SET quantity = {product.quantity} "
                           f"WHERE name = '{product.name}' AND expiry_date = '{product.expiry_date}';")

    def remove(self, product_id):
        with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                    host="localhost", port=5432) as cursor:

            cursor.execute(f"DELETE FROM products WHERE product_id = '{product_id}';")


def get_product_class(category):
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


def add_products(args):
    with open(args.json_file_add) as file:
        products_list = file.read()
        products_list = json.loads(products_list)

        for product_dict in products_list:
            product_class = get_product_class(product_dict["category"])
            product = product_class(product_dict["name"],
                                    product_dict.get("freshness_in_days") or product_dict["expiry_date"],
                                    product_dict.get("quantity"))

            repo = ProductRepository()

            product_status = repo.search(product)

            if product_status:
                # product_status is one-element list of tuples
                # the last element of the tuple is quantity value
                product.quantity = product.quantity + product_status[0][-1]
                repo.update(product)
            else:
                repo.add(product)


def remove_products(args):
    with open(args.json_file_remove) as file:
        products_list = file.read()
        products_list = json.loads(products_list)

        for product_dict in products_list:
            quantity_used = product_dict.get("quantity", 1)
            product_id = product_dict["product_id"]

            repo = ProductRepository()

            product = repo.get(product_id)

            if product.quantity > quantity_used:
                product.quantity = product.quantity - quantity_used
                repo.update(product)
            else:
                repo.remove(product_id)
