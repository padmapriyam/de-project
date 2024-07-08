from unittest.mock import patch
from src.processing_lambda.utils.create_dim_location import create_dim_location
import pandas as pd
import pytest


@pytest.fixture
def dummy_location_df():
    return pd.DataFrame(
        {
            "address_id": [123],
            "address_line_1": ["rock street"],
            "address_line_2": ["dev"],
            "district": ["Yorkshire"],
            "city": ["Leeds"],
            "postal_code": ["L1 2FF"],
            "country": ["England"],
            "phone": ["07522940881"],
            "created_at": ["2024-01-01"],
            "last_updated": ["2024-01-01"],
        }
    )


def test_create_dim_location_returns_pandas_dataframe(dummy_location_df):

    result = create_dim_location(dummy_location_df)

    assert isinstance(result, pd.DataFrame)


def test_create_dim_location_returns_expected_columns(dummy_location_df):

    expected = [
        "location_id",
        "address_line_1",
        "address_line_2",
        "district",
        "city",
        "postal_code",
        "country",
        "phone",
    ]

    result = create_dim_location(dummy_location_df)

    assert list(result.columns) == expected
    assert "created_at" not in list(result.columns)
    assert "last_updated" not in list(result.columns)


def test_create_dim_location_raises_an_error():

    greeting = "hello"
    with pytest.raises(TypeError):
        create_dim_location(greeting)
