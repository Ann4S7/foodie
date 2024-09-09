# TODO improve naming
# TODO create database (postgreSQL) to store products


import json

import products
from database_context_manager import DatabaseContextManager


product_list = []


def add_products(json_file):
    with open(json_file) as file:
        all_products = file.read()
        all_products = json.loads(all_products)

        for product in all_products:
            match product["product"]:
                case "fruit":
                    new_product = products.Fruit(product["name"], product["freshness_in_days"])

                case "vegetable":
                    new_product = products.Vegetable(product["name"], product["freshness_in_days"])

                case "dairy":
                    new_product = products.Dairy(product["name"], product["expiry_date"])

                case "meat":
                    new_product = products.Meat(product["name"], product["expiry_date"])

                case "grain":
                    new_product = products.Grain(product["name"], product["expiry_date"])

            with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                        host="localhost", port=5432) as cursor:
                cursor.execute(f"INSERT INTO products(category, name, expiry_date)"
                               f"VALUES('{new_product.CATEGORY}', '{new_product.name}',"
                               f"'{new_product.expiry_date}');")
