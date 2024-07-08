from src.processing_lambda.utils.convert_dataframe import convert_dataframe_to_parquet
import io
import pandas as pd
import pytest


def test_convert_dataframe_to_parquet_returns_parquet():
    df = pd.DataFrame(
        {
            "one": [-1, 0, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )

    result = convert_dataframe_to_parquet(df)

    pq_file = io.BytesIO(result)
    assert isinstance(pd.read_parquet(pq_file), pd.DataFrame)


def test_convert_dataframe_to_parquet_correctly_retains_correct_data_in_columns():
    input_df = pd.DataFrame(
        {
            "one": [-1, 0, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )

    parquet = convert_dataframe_to_parquet(input_df)

    pq_file = io.BytesIO(parquet)
    output_df = pd.read_parquet(pq_file)

    assert output_df["one"].equals(input_df["one"])
    assert output_df["two"].equals(input_df["two"])
    assert output_df["three"].equals(input_df["three"])


def test_convert_dataframe_to_parquet_raises_TypeError_if_arg_not_dataframe():
    with pytest.raises(TypeError):
        convert_dataframe_to_parquet(True)


def test_convert_dataframe_to_parquet_raises_ValueError_when_given_empty_dataframe():
    with pytest.raises(ValueError):
        convert_dataframe_to_parquet(pd.DataFrame())
