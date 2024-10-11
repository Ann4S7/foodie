import argparse
import os

from src import product_repository

from dotenv import load_dotenv

if os.environ.get("ENV") == "TEST":
    load_dotenv(".env_test")
else:
    load_dotenv()

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)

add_parser = subparsers.add_parser("add")
add_parser.add_argument("json_file_add")
add_parser.set_defaults(func=product_repository.add_products)

remove_parser = subparsers.add_parser("remove")
remove_parser.add_argument("json_file_remove")
remove_parser.set_defaults(func=product_repository.remove_products)

display_parser = subparsers.add_parser("display")
display_parser.add_argument("json_file_display")
display_parser.set_defaults(func=product_repository.display_products)

args = parser.parse_args()

args.func(args)
