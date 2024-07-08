import pandas as pd
import pytest
from src.processing_lambda.utils.create_fact_payment import create_fact_payment
import datetime


@pytest.fixture
def dummy_payment_df():
    return pd.DataFrame(
        {
            "payment_id": [1, 2],
            "created_at": [
                datetime.datetime(2024, 5, 21, 12, 0, 0, 0),
                datetime.datetime(2024, 5, 22, 12, 34, 56, 789000),
            ],
            "last_updated": [
                datetime.datetime(2024, 5, 21, 18, 0, 0, 0),
                datetime.datetime(2024, 5, 22, 12, 34, 56, 789000),
            ],
            "transaction_id": [1, 2],
            "counterparty_id": [1, 2],
            "payment_amount": [10.0, 20.0],
            "currency_id": [1, 2],
            "payment_type_id": [1000, 100000],
            "paid": [True, False],
            "payment_date": ["2024-01-01", "2024-05-22"],
            "company_ac_number": ["12345678", "87654321"],
            "counterparty_ac_number": ["11111111", "22222222"],
        }
    )


def test_create_fact_payment_returns_two_dataframes(dummy_payment_df):
    fact_payment_df, dim_date_df = create_fact_payment(dummy_payment_df)

    assert isinstance(fact_payment_df, pd.DataFrame)
    assert isinstance(dim_date_df, pd.DataFrame)


def test_create_fact_payment_returns_df_with_expected_columns(dummy_payment_df):
    expected_cols = [
        "payment_id",
        "created_date",
        "created_time",
        "last_updated_date",
        "last_updated_time",
        "transaction_id",
        "counterparty_id",
        "payment_amount",
        "currency_id",
        "payment_type_id",
        "paid",
        "payment_date",
    ]

    result, _ = create_fact_payment(dummy_payment_df)

    assert all([col in result.columns for col in expected_cols])
    assert all([col in expected_cols for col in result.columns])


def test_create_fact_payment_returns_df_with_correct_types(dummy_payment_df):
    types = {
        "payment_id": int,
        "created_date": datetime.date,
        "created_time": datetime.time,
        "last_updated_date": datetime.date,
        "last_updated_time": datetime.time,
        "transaction_id": int,
        "counterparty_id": int,
        "payment_amount": float,
        "currency_id": int,
        "payment_type_id": int,
        "paid": bool,
        "payment_date": datetime.date,
    }

    result, _ = create_fact_payment(dummy_payment_df)

    for col in types:
        assert all([isinstance(value, types[col]) for value in result[col]])


def test_create_fact_payment_returns_df_with_correct_values(dummy_payment_df):
    result, _ = create_fact_payment(dummy_payment_df)

    expected = pd.DataFrame(
        {
            "payment_id": dummy_payment_df["payment_id"],
            "created_date": dummy_payment_df["created_at"].dt.date,
            "created_time": dummy_payment_df["created_at"].dt.time,
            "last_updated_date": dummy_payment_df["last_updated"].dt.date,
            "last_updated_time": dummy_payment_df["last_updated"].dt.time,
            "transaction_id": dummy_payment_df["transaction_id"],
            "counterparty_id": dummy_payment_df["counterparty_id"],
            "payment_amount": dummy_payment_df["payment_amount"],
            "currency_id": dummy_payment_df["currency_id"],
            "payment_type_id": dummy_payment_df["payment_type_id"],
            "paid": dummy_payment_df["paid"],
            "payment_date": pd.to_datetime(dummy_payment_df["payment_date"]).dt.date,
        }
    )

    assert result.equals(expected)


def test_create_fact_payment_raises_TypeError_when_argument_not_a_dataframe():
    with pytest.raises(TypeError):
        create_fact_payment(True)
