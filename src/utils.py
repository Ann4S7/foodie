import datetime


def calculate_date(days: int) -> datetime.date:
    """Calculate the product expiry date based on the number of days and today's date.

    Args:
        days: number of days of product freshness.

    Returns: product expiry date.

    """
    return datetime.date.today() + datetime.timedelta(days=days)
