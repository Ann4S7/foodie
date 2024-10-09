from argparse import Namespace
import os
import pytest
import datetime

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
def test_add_products(product_repository, init_resource):
    # given
    namespace = Namespace(json_file_add="tests/test_files/products_to_add.json")
    assert product_repository.count() == 0

    # when
    add_products(namespace)

    # then
    assert product_repository.count() == 2
    assert (product_repository.search("ham", datetime.date(2024, 9, 30))
            == [(1, "meat", "ham", datetime.date(2024, 9, 30), 1)])
    assert (product_repository.search("milk", datetime.date(2024, 10, 5))
            == [(2, "dairy", "milk", datetime.date(2024, 10, 5), 2)])

    # when
    add_products(namespace)

    # then
    assert product_repository.count() == 2
    assert (product_repository.search("ham", datetime.date(2024, 9, 30))
            == [(1, "meat", "ham", datetime.date(2024, 9, 30), 2)])
    assert (product_repository.search("milk", datetime.date(2024, 10, 5))
            == [(2, "dairy", "milk", datetime.date(2024, 10, 5), 4)])


@pytest.mark.order(2)
def test_remove_products(product_repository):
    # given
    namespace = Namespace(json_file_remove="tests/test_files/products_to_remove.json")
    assert product_repository.count() == 2

    # when
    remove_products(namespace)

    # then
    assert product_repository.count() == 2
    assert (product_repository.search("ham", datetime.date(2024, 9, 30))
            == [(1, "meat", "ham", datetime.date(2024, 9, 30), 1)])
    assert (product_repository.search("milk", datetime.date(2024, 10, 5))
            == [(2, "dairy", "milk", datetime.date(2024, 10, 5), 2)])

    # when
    remove_products(namespace)

    # then
    assert product_repository.count() == 0
