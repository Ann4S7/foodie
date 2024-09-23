class Product:
    CATEGORY = "product"
    DEFAULT_QUANTITY = 1

    def __init__(self, name, expiry_date, quantity):
        self.name = name
        self.expiry_date = expiry_date
        self.quantity = quantity or self.DEFAULT_QUANTITY

    def __repr__(self):
        return f"({self.name}, expiry date: {self.expiry_date})"


class Fruit(Product):
    CATEGORY = "fruit"


class Vegetable(Product):
    CATEGORY = "vegetable"


class Dairy(Product):
    CATEGORY = "diary"


class Meat(Product):
    CATEGORY = "meat"


class Grain(Product):
    CATEGORY = "grain"
