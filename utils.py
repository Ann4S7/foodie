from datetime import date, timedelta


def calculate_date(days: int) -> date:
    return date.today() + timedelta(days=days)
