# TODO improve naming
# TODO add the ability to remove products
# TODO add the ability to display products
# TODO storing many of the same products with different dates


import json

import products


def add_products(json_file):
    with open(json_file) as file:
        all_products = file.read()
        all_products = json.loads(all_products)

        for product in all_products:
            match product["product"]:
                case "fruit":
                    new_product = products.Fruit(product["name"], product["freshness_in_days"], product.get("quantity"))

                case "vegetable":
                    new_product = products.Vegetable(product["name"], product["freshness_in_days"],
                                                     product.get("quantity"))

                case "dairy":
                    new_product = products.Dairy(product["name"], product["expiry_date"], product.get("quantity"))

                case "meat":
                    new_product = products.Meat(product["name"], product["expiry_date"], product.get("quantity"))

                case "grain":
                    new_product = products.Grain(product["name"], product["expiry_date"], product.get("quantity"))

            new_product.save()
