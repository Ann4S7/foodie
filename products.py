from utils import calculate_date

from database_context_manager import DatabaseContextManager


class Product:
    EXPIRY_DATE_NOT_SET = "expiry date not set"
    CATEGORY = "product"
    DEFAULT_QUANTITY = 1

    def __init__(self, name):
        self.name = name
        self.expiry_date = Product.EXPIRY_DATE_NOT_SET
        self.quantity = Product.DEFAULT_QUANTITY

    def __repr__(self):
        return f"({self.name}, expiry date: {self.expiry_date})"

    def save(self):
        with DatabaseContextManager(database="foodie_db", user="postgres", password="new_password",
                                    host="localhost", port=5432) as cursor:

            cursor.execute(f"SELECT * FROM products "
                           f"WHERE name = '{self.name}' AND expiry_date = '{self.expiry_date}';")

            product_status = cursor.fetchall()

            if not product_status:
                cursor.execute(f"INSERT INTO products(category, name, expiry_date, quantity)"
                               f"VALUES('{self.CATEGORY}', '{self.name}',"
                               f"'{self.expiry_date}', {self.quantity});")
            else:
                cursor.execute(f"UPDATE products SET quantity = quantity + {self.quantity} "
                               f"WHERE name = '{self.name}' AND expiry_date = '{self.expiry_date}';")


class Fruit(Product):
    CATEGORY = "fruit"

    def __init__(self, name, freshness_in_days, quantity):
        super().__init__(name)
        self.freshness_in_days = freshness_in_days
        self.expiry_date = calculate_date(self.freshness_in_days)
        self.quantity = quantity or self.DEFAULT_QUANTITY


class Vegetable(Product):
    CATEGORY = "vegetable"

    def __init__(self, name, freshness_in_days, quantity):
        super().__init__(name)
        self.freshness_in_days = freshness_in_days
        self.expiry_date = calculate_date(self.freshness_in_days)
        self.quantity = quantity or self.DEFAULT_QUANTITY


class Dairy(Product):
    CATEGORY = "diary"

    def __init__(self, name, expiry_date, quantity):
        super().__init__(name)
        self.expiry_date = expiry_date
        self.quantity = quantity or self.DEFAULT_QUANTITY


class Meat(Product):
    CATEGORY = "meat"

    def __init__(self, name, expiry_date, quantity):
        super().__init__(name)
        self.expiry_date = expiry_date
        self.quantity = quantity or self.DEFAULT_QUANTITY


class Grain(Product):
    CATEGORY = "grain"

    def __init__(self, name, expiry_date, quantity):
        super().__init__(name)
        self.expiry_date = expiry_date
        self.quantity = quantity or self.DEFAULT_QUANTITY
