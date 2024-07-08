from unittest.mock import patch
from src.processing_lambda.utils.create_dim_date import create_dim_date
import pandas as pd
import pytest
from pandas import DatetimeIndex
from datetime import date


@pytest.fixture
def dummy_dates_v2():
    return [
        date(2024, 1, 3),
        date(2024, 2, 15),
        date(2024, 3, 25),
        date(2020, 4, 1),
        date(2023, 5, 15),
        date(2024, 6, 25),
        date(2024, 7, 1),
        date(2023, 8, 15),
        date(2024, 9, 25),
        date(2024, 10, 1),
        date(2023, 11, 15),
        date(2024, 12, 27),
    ]


def test_create_dim_date_returns_dataframe(dummy_dates_v2):

    result = create_dim_date(dummy_dates_v2)

    assert isinstance(result, pd.DataFrame)


def test_create_dim_date_returns_columns(dummy_dates_v2):

    expected = [
        "date_id",
        "year",
        "month",
        "day",
        "day_of_week",
        "day_name",
        "month_name",
        "quarter",
    ]

    result = create_dim_date(dummy_dates_v2)

    assert all(col in result.columns for col in expected)


def test_create_dim_date_works_return_correct_amount(dummy_dates_v2):

    result = create_dim_date(dummy_dates_v2)

    assert len(result.year) == 12
    assert len(result.month) == 12
    assert len(result.day) == 12


def test_create_dim_date_works_returns_day_of_week(dummy_dates_v2):

    result = create_dim_date(dummy_dates_v2)

    assert result.day_of_week[0] == 2
    assert result.day_of_week[1] == 3
    assert result.day_of_week[11] == 4


def test_create_dim_date_works_returns_name_of_day(dummy_dates_v2):

    result = create_dim_date(dummy_dates_v2)

    assert result.day_name[0] == "Wednesday"
    assert result.day_name[1] == "Thursday"


def test_create_dim_date_works_returns_name_of_month(dummy_dates_v2):

    result = create_dim_date(dummy_dates_v2)

    assert result.month_name[0] == "January"
    assert result.month_name[11] == "December"


def test_create_dim_date_returns_correct_year(dummy_dates_v2):

    result = create_dim_date(dummy_dates_v2)

    assert result.year[0] == 2024
    assert result.year[3] == 2020


def test_create_dim_date_works_returns_correct_quarter(dummy_dates_v2):

    result = create_dim_date(dummy_dates_v2)

    print(result.quarter)

    assert list(result.quarter) == [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]


def test_create_dim_date_raised_type_error(dummy_dates_v2):

    greeting = "hello"

    with pytest.raises(TypeError):
        create_dim_date(greeting)
