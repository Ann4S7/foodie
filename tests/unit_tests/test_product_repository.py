import products
from product_repository import get_product_class


def test_get_product_class():
    assert get_product_class("fruit") == products.Fruit
    assert get_product_class("vegetable") == products.Vegetable
    assert get_product_class("dairy") == products.Dairy
    assert get_product_class("meat") == products.Meat
    assert get_product_class("grain") == products.Grain
    assert get_product_class("something") == products.Product
