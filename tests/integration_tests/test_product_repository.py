from argparse import Namespace
import os
import pytest

from product_repository import add_products, ProductRepository, remove_products


@pytest.fixture
def product_repository():
    return ProductRepository(
        database=os.environ.get("DB_NAME"),
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=int(os.environ.get("DB_PORT"))
    )


@pytest.mark.order(1)
def test_add_products(product_repository):
    # given
    assert product_repository.count() == 0

    # when
    namespace = Namespace(json_file_add="products_to_add.json")
    add_products(namespace)

    # then
    assert product_repository.count() == 2

    # spr search czy dod ok recordy
    # sor czy za 2 add zniana quantity


@pytest.mark.order(2)
def test_remove_products(product_repository):
    # given
    assert product_repository.count() == 2

    # when
    namespace = Namespace(json_file_remove="products_to_remove.json")
    remove_products(namespace)

    # then
    assert product_repository.count() == 0


