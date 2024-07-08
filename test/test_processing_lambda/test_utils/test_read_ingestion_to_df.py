from src.processing_lambda.utils.read_ingestion_object_to_df import (
    read_object_into_dataframe,
)
import io
import pandas as pd
import pytest
import boto3
from moto import mock_aws
import os


@pytest.fixture
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture
def s3_client(aws_creds):
    with mock_aws():
        yield boto3.client("s3")


@pytest.fixture
def s3_bucket(s3_client):
    bucket_name = "test-bucket"
    region = "eu-west-2"
    bucket = s3_client.create_bucket(
        Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region}
    )
    return bucket_name


@pytest.fixture
def add_bucket_object(s3_client, s3_bucket):
    json_data = """{"col1": 1, "col2": "value1", "col3": true}
                    {"col1": 2, "col2": "value2", "col3": false}
                    {"col1": 3, "col2": "value3", "col3": true}"""

    key = "test-key.json"
    s3_client.put_object(Bucket=s3_bucket, Key=key, Body=json_data.encode("utf-8"))
    return key


def test_function_converts_json_lines_to_df(add_bucket_object, s3_bucket):
    key = add_bucket_object
    df = read_object_into_dataframe(s3_bucket, key)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ["col1", "col2", "col3"]


def test_function_raises_type_error_when_first_param_is_not_string():
    with pytest.raises(TypeError):
        read_object_into_dataframe(123, "test-key.json")


def test_function_raises_type_error_when_second_param_is_not_string():
    with pytest.raises(TypeError):
        read_object_into_dataframe("test-bucket", 123)


def test_function_raises_value_error_when_it_fails_to_process_s3_object():
    with pytest.raises(ValueError):
        read_object_into_dataframe("not-a-bucket", "not-a-key.jsonl")
