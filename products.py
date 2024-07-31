from datetime import date, timedelta


class Product:
    EXPIRY_DATE_NOT_SET = "expiry date not set"

    def __init__(self, name):
        self.name = name
        self.expiry_date = Product.EXPIRY_DATE_NOT_SET

    def __repr__(self):
        return f"({self.name}, expiry date: {self.expiry_date})"


def calculate_date(freshness_in_days):
    expiry_date = date.today() + timedelta(days=freshness_in_days)
    return expiry_date


class Fruit(Product):
    def __init__(self, name, freshness_in_days):
        super().__init__(name)
        self.freshness_in_days = freshness_in_days
        self.expiry_date = calculate_date(self.freshness_in_days)


class Vegetable(Product):
    def __init__(self, name, freshness_in_days):
        super().__init__(name)
        self.freshness_in_days = freshness_in_days
        self.expiry_date = calculate_date(self.freshness_in_days)


class Dairy(Product):
    def __init__(self, name, expiry_date):
        super().__init__(name)
        self.expiry_date = expiry_date


class Meat(Product):
    def __init__(self, name, expiry_date):
        super().__init__(name)
        self.expiry_date = expiry_date


class Grain(Product):
    def __init__(self, name, expiry_date):
        super().__init__(name)
        self.expiry_date = expiry_date
