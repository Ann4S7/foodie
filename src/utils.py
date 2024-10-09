import datetime


def calculate_date(days: int) -> datetime.date:
    return datetime.date.today() + datetime.timedelta(days=days)
