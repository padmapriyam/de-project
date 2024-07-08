from unittest.mock import patch
from src.processing_lambda.utils.create_dim_counterparty import create_dim_counterparty
import pandas as pd
import pytest


@pytest.fixture
def dummy_counterparty_df():
    return pd.DataFrame(
        {
            "counterparty_id": [1, 2],
            "counterparty_legal_name": ["a", "b"],
            "legal_address_id": [1, 2],
            "commercial_contact": ["a", "b"],
            "delivery_contact": ["a", "b"],
            "created_at": ["staff_created_at1", "staff_created_at2"],
            "last_updated": ["staff_last_updated1", "staff_last_updated2"],
        }
    )


@pytest.fixture
def dummy_address_df():
    return pd.DataFrame(
        {
            "address_id": [1, 2],
            "address_line_1": ["dummy1", "dummy2"],
            "address_line_2": ["dum1", "dum2"],
            "district": ["dist1", "dist2"],
            "city": ["city1", "city2"],
            "postal_code": ["pc1", "pc22"],
            "country": ["con1", "con2"],
            "phone": ["123", "456"],
            "created_at": ["dpt_created_at1", "dpt_created_at2"],
            "last_updated": ["dpt_last_updated1", "dpt_last_updated2"],
        }
    )


def test_create_dim_counterparty_returns_a_dataframe(
    dummy_counterparty_df, dummy_address_df
):
    with patch(
        "src.processing_lambda.utils.create_dim_counterparty.get_df_from_s3_bucket"
    ) as patched_func:
        patched_func.return_value = dummy_address_df

        assert isinstance(create_dim_counterparty(dummy_counterparty_df), pd.DataFrame)


def test_create_dim_counterparty_returns_df_with_expected_columns(
    dummy_counterparty_df, dummy_address_df
):
    expected_cols = [
        "counterparty_id",
        "counterparty_legal_name",
        "counterparty_legal_address_line_1",
        "counterparty_legal_address_line_2",
        "counterparty_legal_district",
        "counterparty_legal_city",
        "counterparty_legal_postal_code",
        "counterparty_legal_country",
        "counterparty_legal_phone_number",
    ]

    with patch(
        "src.processing_lambda.utils.create_dim_counterparty.get_df_from_s3_bucket"
    ) as patched_func:
        patched_func.return_value = dummy_address_df

        result = create_dim_counterparty(dummy_counterparty_df)

    assert all([col in result.columns for col in expected_cols])


def test_create_dim_counterparty_returns_correct_name_and_location_for_each_department(
    dummy_counterparty_df, dummy_address_df
):
    with patch(
        "src.processing_lambda.utils.create_dim_counterparty.get_df_from_s3_bucket"
    ) as patched_func:
        patched_func.return_value = dummy_address_df

        result = create_dim_counterparty(dummy_counterparty_df)

    assert result["counterparty_legal_address_line_1"].equals(
        dummy_address_df["address_line_1"]
    )
    assert result["counterparty_legal_address_line_2"].equals(
        dummy_address_df["address_line_2"]
    )
    assert result["counterparty_legal_city"].equals(dummy_address_df["city"])
    assert result["counterparty_legal_district"].equals(dummy_address_df["district"])
    assert result["counterparty_legal_postal_code"].equals(
        dummy_address_df["postal_code"]
    )
    assert result["counterparty_legal_country"].equals(dummy_address_df["country"])
    assert result["counterparty_legal_phone_number"].equals(dummy_address_df["phone"])


def test_create_dim_counterparty_raises_ValueError_when_missing_required_address_details(
    dummy_counterparty_df, dummy_address_df
):
    with patch(
        "src.processing_lambda.utils.create_dim_counterparty.get_df_from_s3_bucket"
    ) as patched_func:
        patched_func.return_value = dummy_address_df[
            dummy_address_df["address_id"] == 1
        ]

        with pytest.raises(ValueError) as e:
            create_dim_counterparty(dummy_counterparty_df)
    assert str(e.value) == "One or more of the address fields are empty."


def test_create_dim_counterparty_throws_type_error_when_dataframe_not_passed():
    with pytest.raises(TypeError):
        create_dim_counterparty(True)
