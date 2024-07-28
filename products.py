from datetime import date, timedelta


class Product:
    def __init__(self, name):
        self.name = name


class Fruit(Product):
    def __init__(self, name, freshness_in_days):
        super().__init__(name)
        self.freshness_in_days = freshness_in_days
        self.expiry_date = None

    def calculate_date(self):
        self.expiry_date = date.today() + timedelta(days=self.freshness_in_days)
        return self.expiry_date


class Vegetable(Product):
    def __init__(self, name, freshness_in_days):
        super().__init__(name)
        self.freshness_in_days = freshness_in_days
        self.expiry_date = None

    def calculate_date(self):
        self.expiry_date = date.today() + timedelta(days=self.freshness_in_days)
        return self.expiry_date


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


# fruit1 = Fruit("mango", 5)
#
# print(fruit1.calculate_date())
