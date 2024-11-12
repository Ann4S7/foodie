import os

import pytest
from dotenv import load_dotenv

import db_utils

if os.environ.get("ENV") == "TEST":
    load_dotenv(".env_test")
else:
    load_dotenv()


@pytest.fixture(scope="module")
def init_resource():
    db_utils.create_products_table(
        database=os.environ.get("DB_NAME"),
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=int(os.environ.get("DB_PORT")),
    )
    yield
    db_utils.drop_products_table(
        database=os.environ.get("DB_NAME"),
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=int(os.environ.get("DB_PORT")),
    )
