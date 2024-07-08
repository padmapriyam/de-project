from unittest.mock import patch
from src.processing_lambda.utils.create_dim_staff import create_dim_staff
import pandas as pd
import pytest


@pytest.fixture
def dummy_staff_df():
    return pd.DataFrame(
        {
            "staff_id": [1, 2],
            "first_name": ["a", "b"],
            "last_name": ["c", "d"],
            "department_id": [1, 2],
            "email_address": ["a@a.com", "b@b.com"],
            "created_at": ["staff_created_at1", "staff_created_at2"],
            "last_updated": ["staff_last_updated1", "staff_last_updated2"],
        }
    )


@pytest.fixture
def dummy_department_df():
    return pd.DataFrame(
        {
            "department_id": [1, 2],
            "department_name": ["dummy1", "dummy2"],
            "location": ["location1", "location2"],
            "manager": ["me", "you"],
            "created_at": ["dpt_created_at1", "dpt_created_at2"],
            "last_updated": ["dpt_last_updated1", "dpt_last_updated2"],
        }
    )


def test_create_dim_staff_returns_a_dataframe(dummy_staff_df, dummy_department_df):
    with patch(
        "src.processing_lambda.utils.create_dim_staff.get_df_from_s3_bucket"
    ) as patched_func:
        patched_func.return_value = dummy_department_df

        assert isinstance(create_dim_staff(dummy_staff_df), pd.DataFrame)


def test_create_dim_staff_returns_df_with_expected_columns(
    dummy_staff_df, dummy_department_df
):
    expected_cols = [
        "staff_id",
        "first_name",
        "last_name",
        "department_name",
        "location",
        "email_address",
    ]

    with patch(
        "src.processing_lambda.utils.create_dim_staff.get_df_from_s3_bucket"
    ) as patched_func:
        patched_func.return_value = dummy_department_df

        result = create_dim_staff(dummy_staff_df)

    assert all([col in result.columns for col in expected_cols])


def test_create_dim_staff_returns_correct_name_and_location_for_each_department(
    dummy_staff_df, dummy_department_df
):
    with patch(
        "src.processing_lambda.utils.create_dim_staff.get_df_from_s3_bucket"
    ) as patched_func:
        patched_func.return_value = dummy_department_df

        result = create_dim_staff(dummy_staff_df)

    assert result["department_name"].equals(dummy_department_df["department_name"])
    assert result["location"].equals(dummy_department_df["location"])


def test_create_dim_staff_raises_ValueError_when_missing_department_name_or_location(
    dummy_staff_df, dummy_department_df
):
    with patch(
        "src.processing_lambda.utils.create_dim_staff.get_df_from_s3_bucket"
    ) as patched_func:
        patched_func.return_value = dummy_department_df[
            dummy_department_df["department_id"] == 1
        ]

        with pytest.raises(ValueError) as e:
            create_dim_staff(dummy_staff_df)

    assert str(e.value) == "department_name or location not found"


def test_create_dim_staff_throws_type_error_when_dataframe_not_passed():
    with pytest.raises(TypeError):
        create_dim_staff(True)
