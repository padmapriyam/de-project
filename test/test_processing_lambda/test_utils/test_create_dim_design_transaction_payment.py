from unittest.mock import patch
from src.processing_lambda.utils.create_dim_design_transaction_payment import (
    drop_update_created_at_two_columns,
)
import pandas as pd
import pytest


@pytest.fixture
def dummy_design_df():
    return pd.DataFrame(
        {
            "design_id": 1,
            "created_at": ["2024-01-01"],
            "last_updated": ["2024-01-01"],
            "design_name": [123],
            "file_location": ["rock street"],
            "file_name": ["dev"],
        }
    )


def test_drop_update_created_at_two_columns_returns_pandas_dataframe(dummy_design_df):
    result = drop_update_created_at_two_columns(dummy_design_df)

    assert isinstance(result, pd.DataFrame)


def test_drop_update_created_at_two_columns_returns_expected_columns(dummy_design_df):

    expected = ["design_id", "design_name", "file_location", "file_name"]

    result = drop_update_created_at_two_columns(dummy_design_df)

    assert list(result.columns) == expected


def test_create_dim_location_raises_an_error():
    with pytest.raises(TypeError):
        drop_update_created_at_two_columns(False)
