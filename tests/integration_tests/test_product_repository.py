from argparse import Namespace
import pytest
import datetime

from product_repository import add_products, ProductRepository, remove_products
from utils import calculate_date


@pytest.fixture
def product_repository():
    return ProductRepository()


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
    assert (product_repository.search("banana", calculate_date(3))
            == [(2, "fruit", "banana",  calculate_date(3), 2)])

    # when
    add_products(namespace)

    # then
    assert product_repository.count() == 2
    assert (product_repository.search("ham", datetime.date(2024, 9, 30))
            == [(1, "meat", "ham", datetime.date(2024, 9, 30), 2)])
    assert (product_repository.search("banana",  calculate_date(3))
            == [(2, "fruit", "banana",  calculate_date(3), 4)])


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
    assert (product_repository.search("banana",  calculate_date(3))
            == [(2, "fruit", "banana",  calculate_date(3), 2)])

    # when
    remove_products(namespace)

    # then
    assert product_repository.count() == 0
