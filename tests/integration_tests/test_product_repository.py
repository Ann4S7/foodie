import datetime
from argparse import Namespace

import pytest

from product_repository import (
    ProductRepository,
    add_products,
    display_products,
    remove_products,
)
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
    assert product_repository.search(
        conditions={"name": "ham", "expiry_date": datetime.date(2024, 9, 30)}
    ) == [(1, "meat", "ham", datetime.date(2024, 9, 30), 1)]
    assert product_repository.search(
        conditions={"name": "banana", "expiry_date": calculate_date(3)}
    ) == [(2, "fruit", "banana", calculate_date(3), 2)]

    # when
    add_products(namespace)

    # then
    assert product_repository.count() == 2
    assert product_repository.search(
        conditions={"name": "ham", "expiry_date": datetime.date(2024, 9, 30)}
    ) == [(1, "meat", "ham", datetime.date(2024, 9, 30), 2)]
    assert product_repository.search(
        conditions={"name": "banana", "expiry_date": calculate_date(3)}
    ) == [(2, "fruit", "banana", calculate_date(3), 4)]


@pytest.mark.order(2)
@pytest.mark.parametrize(
    "file_version, expected_result",
    [
        ("1", [("banana", calculate_date(3), 4)]),
        ("2", [(1, "meat", "ham", datetime.date(2024, 9, 30), 2)]),
        (
            "3",
            [
                (1, "meat", "ham", datetime.date(2024, 9, 30), 2),
                (2, "fruit", "banana", calculate_date(3), 4),
            ],
        ),
    ],
)
def test_display_products(product_repository, file_version, expected_result):
    # given
    namespace = Namespace(
        json_file_display=f"tests/test_files/products_to_display_{file_version}.json"
    )

    # when
    feedback = display_products(namespace)

    # then
    assert feedback == expected_result


@pytest.mark.order(3)
def test_remove_products(product_repository):
    # given
    namespace = Namespace(json_file_remove="tests/test_files/products_to_remove.json")
    assert product_repository.count() == 2

    # when
    remove_products(namespace)

    # then
    assert product_repository.count() == 2
    assert product_repository.search(
        conditions={"name": "ham", "expiry_date": datetime.date(2024, 9, 30)}
    ) == [(1, "meat", "ham", datetime.date(2024, 9, 30), 1)]
    assert product_repository.search(
        conditions={"name": "banana", "expiry_date": calculate_date(3)}
    ) == [(2, "fruit", "banana", calculate_date(3), 2)]

    # when
    remove_products(namespace)

    # then
    assert product_repository.count() == 0
