from utils import calculate_date


class Product:
    EXPIRY_DATE_NOT_SET = "expiry date not set"
    CATEGORY = "product"

    def __init__(self, name):
        self.name = name
        self.expiry_date = Product.EXPIRY_DATE_NOT_SET

    def __repr__(self):
        return f"({self.name}, expiry date: {self.expiry_date})"

    def save(self):
        pass


class Fruit(Product):
    CATEGORY = "fruit"

    def __init__(self, name, freshness_in_days):
        super().__init__(name)
        self.freshness_in_days = freshness_in_days
        self.expiry_date = calculate_date(self.freshness_in_days)


class Vegetable(Product):
    CATEGORY = "vegetable"

    def __init__(self, name, freshness_in_days):
        super().__init__(name)
        self.freshness_in_days = freshness_in_days
        self.expiry_date = calculate_date(self.freshness_in_days)


class Dairy(Product):
    CATEGORY = "diary"

    def __init__(self, name, expiry_date):
        super().__init__(name)
        self.expiry_date = expiry_date


class Meat(Product):
    CATEGORY = "meat"

    def __init__(self, name, expiry_date):
        super().__init__(name)
        self.expiry_date = expiry_date


class Grain(Product):
    CATEGORY = "grain"

    def __init__(self, name, expiry_date):
        super().__init__(name)
        self.expiry_date = expiry_date
