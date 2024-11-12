from datetime import date


class Product:
    """A class representing the product."""

    CATEGORY = "product"
    DEFAULT_QUANTITY = 1

    def __init__(self, name: str, expiry_date: date, quantity: int) -> None:
        """Initialise the new instance of the Product class. Assign values to object properties.

        Args:
            name: product name.
            expiry_date: product expiry date.
            quantity: product quantity.

        """
        self.name = name
        self.expiry_date = expiry_date
        self.quantity = quantity or self.DEFAULT_QUANTITY

    def __repr__(self) -> str:
        """Create a printable representation of the Product instance.

        Returns: a string that contains the product properties
            such as name, expiry date and quantity.

        """
        return f"(name: {self.name}, expiry date: {self.expiry_date}, quantity: {self.quantity})"


class Fruit(Product):
    """A class representing the fruit."""

    CATEGORY = "fruit"


class Vegetable(Product):
    """A class representing the vegetable."""

    CATEGORY = "vegetable"


class Dairy(Product):
    """A class representing the dairy product."""

    CATEGORY = "dairy"


class Meat(Product):
    """A class representing the meat."""

    CATEGORY = "meat"


class Grain(Product):
    """A class representing the grain product."""

    CATEGORY = "grain"
