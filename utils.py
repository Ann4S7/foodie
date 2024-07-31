from datetime import date, timedelta


def calculate_date(days):
    return date.today() + timedelta(days=days)
