import pandas as pd
import pytest
from src.processing_lambda.utils.create_fact_purchase_order import (
    create_fact_purchase_order,
)
import datetime


@pytest.fixture
def dummy_purchase_order_df():
    return pd.DataFrame(
        {
            "purchase_order_id": [1, 2],
            "created_at": [
                datetime.datetime(2024, 5, 21, 12, 0, 0, 0),
                datetime.datetime(2024, 5, 22, 12, 34, 56, 789000),
            ],
            "last_updated": [
                datetime.datetime(2024, 5, 21, 18, 0, 0, 0),
                datetime.datetime(2024, 5, 22, 12, 34, 56, 789000),
            ],
            "staff_id": [1, 2],
            "counterparty_id": [1, 2],
            "item_code": ["ABCD", "EFGH"],
            "item_quantity": [1, 999],
            "item_unit_price": [3.1, 999.9],
            "currency_id": [1, 3],
            "agreed_delivery_date": ["2024-01-01", "2024-05-22"],
            "agreed_payment_date": ["2023-12-31", "2024-05-22"],
            "agreed_delivery_location_id": [1, 2],
        }
    )


def test_create_fact_purchase_order_returns_two_dataframes(dummy_purchase_order_df):
    fact_purchase_order_df, dim_date_df = create_fact_purchase_order(
        dummy_purchase_order_df
    )

    assert isinstance(fact_purchase_order_df, pd.DataFrame)
    assert isinstance(dim_date_df, pd.DataFrame)


def test_create_fact_purchase_order_returns_df_with_expected_columns(
    dummy_purchase_order_df,
):
    expected_cols = [
        "purchase_order_id",
        "created_date",
        "created_time",
        "last_updated_date",
        "last_updated_time",
        "staff_id",
        "counterparty_id",
        "item_code",
        "item_quantity",
        "item_unit_price",
        "currency_id",
        "agreed_delivery_date",
        "agreed_payment_date",
        "agreed_delivery_location_id",
    ]

    result, _ = create_fact_purchase_order(dummy_purchase_order_df)

    assert all([col in result.columns for col in expected_cols])
    assert all([col in expected_cols for col in result.columns])


def test_create_fact_purchase_order_returns_df_with_correct_types(
    dummy_purchase_order_df,
):
    types = {
        "purchase_order_id": int,
        "created_date": datetime.date,
        "created_time": datetime.time,
        "last_updated_date": datetime.date,
        "last_updated_time": datetime.time,
        "staff_id": int,
        "counterparty_id": int,
        "item_code": str,
        "item_quantity": int,
        "item_unit_price": float,
        "currency_id": int,
        "agreed_delivery_date": datetime.date,
        "agreed_payment_date": datetime.date,
        "agreed_delivery_location_id": int,
    }

    result, _ = create_fact_purchase_order(dummy_purchase_order_df)

    for col in types:
        assert all([isinstance(value, types[col]) for value in result[col]])


def test_create_fact_purchase_order_returns_df_with_correct_values(
    dummy_purchase_order_df,
):
    result, _ = create_fact_purchase_order(dummy_purchase_order_df)

    expected = pd.DataFrame(
        {
            "purchase_order_id": dummy_purchase_order_df["purchase_order_id"],
            "created_date": dummy_purchase_order_df["created_at"].dt.date,
            "created_time": dummy_purchase_order_df["created_at"].dt.time,
            "last_updated_date": dummy_purchase_order_df["last_updated"].dt.date,
            "last_updated_time": dummy_purchase_order_df["last_updated"].dt.time,
            "staff_id": dummy_purchase_order_df["staff_id"],
            "counterparty_id": dummy_purchase_order_df["counterparty_id"],
            "item_code": dummy_purchase_order_df["item_code"],
            "item_quantity": dummy_purchase_order_df["item_quantity"],
            "item_unit_price": dummy_purchase_order_df["item_unit_price"],
            "currency_id": dummy_purchase_order_df["currency_id"],
            "agreed_delivery_date": pd.to_datetime(
                dummy_purchase_order_df["agreed_delivery_date"]
            ).dt.date,
            "agreed_payment_date": pd.to_datetime(
                dummy_purchase_order_df["agreed_payment_date"]
            ).dt.date,
            "agreed_delivery_location_id": dummy_purchase_order_df[
                "agreed_delivery_location_id"
            ],
        }
    )

    assert result.equals(expected)


def test_create_fact_purchase_order_raises_TypeError_when_argument_not_a_dataframe():
    with pytest.raises(TypeError):
        create_fact_purchase_order(True)
