import argparse

import product_repository


parser = argparse.ArgumentParser()

parser.add_argument("json_file")

args = parser.parse_args()

product_repository.add_products(args.json_file)
