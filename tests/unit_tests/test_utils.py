from datetime import date
from unittest.mock import patch

from utils import calculate_date


@patch("datetime.date")
def test_calculate_date(mock_today):
    mock_today.today.return_value = date(2024, 1, 24)
    assert calculate_date(1) == date(2024, 1, 25)
