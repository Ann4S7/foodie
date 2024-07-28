# TODO switchcase python 3.10 instead if-else
# TODO improve naming
# TODO add repr/str to classes
# TODO create database (postgreSQL) to store products


import json

import products


product_list = []


def add_products(json_file):
    with open(json_file) as file:
        all_products = file.read()
        all_products = json.loads(all_products)

        for product in all_products:
            if product["product"] == "fruit":
                name = product["name"]
                freshness_in_days = product["freshness_in_days"]
                product_list.append(products.Fruit(name, freshness_in_days))
            elif product["product"] == "vegetable":
                name = product["name"]
                freshness_in_days = product["freshness_in_days"]
                product_list.append(products.Vegetable(name, freshness_in_days))
            elif product["product"] == "dairy":
                name = product["name"]
                expiry_date = product["expiry_date"]
                product_list.append(products.Dairy(name, expiry_date))
            elif product["product"] == "meat":
                name = product["name"]
                expiry_date = product["expiry_date"]
                product_list.append(products.Meat(name, expiry_date))
            elif product["product"] == "grain":
                name = product["name"]
                expiry_date = product["expiry_date"]
                product_list.append(products.Grain(name, expiry_date))

    print(product_list)
