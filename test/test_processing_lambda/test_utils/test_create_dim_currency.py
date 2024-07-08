from src.processing_lambda.utils.create_dim_currency import create_dim_currency
import pandas as pd
import pytest


def test_create_dim_currency_returns_a_dataframe():
    df = pd.DataFrame({"currency_id": [1, 2], "currency_code": ["GBP", "USD"]})

    assert isinstance(create_dim_currency(df), pd.DataFrame)


def test_create_dim_currency_returns_df_with_currency_name():
    df = pd.DataFrame({"currency_id": [1, 2], "currency_code": ["GBP", "USD"]})

    create_dim_currency(df)
    assert "currency_name" in df.columns


def test_create_dim_currency_returns_correct_currency_name_for_each_code():
    df = pd.DataFrame({"currency_id": [1, 2], "currency_code": ["GBP", "USD"]})

    create_dim_currency(df)
    assert df["currency_name"].equals(
        pd.Series(["Pound Sterling", "United States Dollar"])
    )


def test_create_dim_currency_throws_key_error_when_currency_code_not_found():
    df = pd.DataFrame({"currency_id": [1, 2], "currency_code": ["GBP", "INR"]})

    with pytest.raises(KeyError) as e:
        create_dim_currency(df)
    assert str(e.value) == "\"Currency code 'INR' not found!!\""


def test_create_dim_currency_throws_type_error_when_dataframe_not_passed():
    with pytest.raises(TypeError):
        create_dim_currency(True)
