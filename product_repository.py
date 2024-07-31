# TODO improve naming
# TODO create database (postgreSQL) to store products


import json

import products


product_list = []


def add_products(json_file):
    with open(json_file) as file:
        all_products = file.read()
        all_products = json.loads(all_products)

        for product in all_products:
            match product["product"]:
                case "fruit":
                    name = product["name"]
                    freshness_in_days = product["freshness_in_days"]
                    product_list.append(products.Fruit(name, freshness_in_days))
                case "vegetable":
                    name = product["name"]
                    freshness_in_days = product["freshness_in_days"]
                    product_list.append(products.Vegetable(name, freshness_in_days))
                case "dairy":
                    name = product["name"]
                    expiry_date = product["expiry_date"]
                    product_list.append(products.Dairy(name, expiry_date))
                case "meat":
                    name = product["name"]
                    expiry_date = product["expiry_date"]
                    product_list.append(products.Meat(name, expiry_date))
                case "grain":
                    name = product["name"]
                    expiry_date = product["expiry_date"]
                    product_list.append(products.Grain(name, expiry_date))

    print(product_list)
