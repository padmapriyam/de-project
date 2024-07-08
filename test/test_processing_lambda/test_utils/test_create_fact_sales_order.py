import pandas as pd
import pytest
from src.processing_lambda.utils.create_fact_sales_order import create_fact_sales_order
import datetime


@pytest.fixture
def dummy_sales_order_df():
    return pd.DataFrame(
        {
            "sales_order_id": [1, 2],
            "created_at": [datetime.datetime.now(), datetime.datetime.now()],
            "last_updated": [datetime.datetime.now(), datetime.datetime.now()],
            "design_id": [1, 2],
            "staff_id": [1, 2],
            "counterparty_id": [1, 2],
            "units_sold": [1000, 100000],
            "unit_price": [2.00, 4.00],
            "currency_id": [1, 2],
            "agreed_delivery_date": ["2024-01-01", "2024-05-22"],
            "agreed_payment_date": ["2024-01-01", "2024-05-22"],
            "agreed_delivery_location_id": [1, 2],
        }
    )


def test_create_fact_sales_order_returns_two_dataframes(dummy_sales_order_df):
    fact_sales_order_df, dim_date_df = create_fact_sales_order(dummy_sales_order_df)

    assert isinstance(fact_sales_order_df, pd.DataFrame)
    assert isinstance(dim_date_df, pd.DataFrame)


def test_create_fact_sales_order_returns_df_with_expected_columns(dummy_sales_order_df):
    expected_cols = [
        "sales_order_id",
        "created_date",
        "created_time",
        "last_updated_date",
        "last_updated_time",
        "sales_staff_id",
        "counterparty_id",
        "units_sold",
        "unit_price",
        "currency_id",
        "design_id",
        "agreed_payment_date",
        "agreed_delivery_date",
        "agreed_delivery_location_id",
    ]

    result, _ = create_fact_sales_order(dummy_sales_order_df)

    assert all([col in result.columns for col in expected_cols])


def test_create_fact_sales_order_returns_df_with_correct_types(dummy_sales_order_df):
    types = {
        "sales_order_id": int,
        "created_date": datetime.date,
        "created_time": datetime.time,
        "last_updated_date": datetime.date,
        "last_updated_time": datetime.time,
        "sales_staff_id": int,
        "counterparty_id": int,
        "units_sold": int,
        "unit_price": float,
        "currency_id": int,
        "design_id": int,
        "agreed_payment_date": datetime.date,
        "agreed_delivery_date": datetime.date,
        "agreed_delivery_location_id": int,
    }

    result, _ = create_fact_sales_order(dummy_sales_order_df)

    for col in types:
        assert all([isinstance(value, types[col]) for value in result[col]])


def test_create_fact_sales_order_raises_TypeError_when_argument_not_a_dataframe():
    with pytest.raises(TypeError):
        create_fact_sales_order(True)
