import argparse

import product_repository


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)

add_parser = subparsers.add_parser("add")
add_parser.add_argument("json_file_add")
add_parser.set_defaults(func=product_repository.add_products)

remove_parser = subparsers.add_parser("remove")
remove_parser.add_argument("json_file_remove")
remove_parser.set_defaults(func=product_repository.remove_products)

args = parser.parse_args()

args.func(args)
