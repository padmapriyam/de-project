import boto3
from moto import mock_aws
import os
import pytest
from unittest.mock import patch
from src.write_object_to_s3_bucket import write_object_to_s3_bucket
from src.custom_exceptions import NoSuchBucket
import io
import pandas as pd
from src.processing_lambda.utils.convert_dataframe import (
    convert_dataframe_to_parquet,
)


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def mock_client(aws_credentials):
    with mock_aws():
        yield boto3.client("s3")


@pytest.fixture(scope="function")
def mock_client_without_credentials():
    with mock_aws():
        yield boto3.client("s3")


@pytest.fixture(scope="function")
def mock_bucket(mock_client):
    bucket_name = "test-bucket"

    mock_client.create_bucket(
        ACL="private",
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )


def test_write_object_to_s3_bucket_returns_success_message_on_successful_write(
    mock_client, mock_bucket
):
    file_key = "test-file"

    response = write_object_to_s3_bucket("test-bucket", file_key, "test\n")

    assert response == "File test-file successfully written to bucket test-bucket"


def test_write_object_to_s3_bucket_successfully_writes_data_to_file(
    mock_client, mock_bucket
):
    bucket_name = "test-bucket"
    file_key = "test-file"

    write_object_to_s3_bucket(bucket_name, file_key, "test\n")

    response = mock_client.get_object(Bucket=bucket_name, Key=file_key)

    assert response["Body"].read().decode("utf_8") == "test\n"


def test_write_object_to_s3_bucket_raises_error_when_bucket_does_not_exist(mock_client):
    bucket_name = "test-bucket"
    file_key = "test-file"

    with pytest.raises(NoSuchBucket):
        write_object_to_s3_bucket(bucket_name, file_key, "test\n")


def test_write_object_to_s3_bucket_succeeds_with_empty_data(mock_client, mock_bucket):
    bucket_name = "test-bucket"
    file_key = "test-file"

    write_object_to_s3_bucket(bucket_name, file_key, "")

    response = mock_client.get_object(Bucket=bucket_name, Key=file_key)

    assert response["Body"].read() == b""


def test_write_object_to_s3_bucket_succeeds_with_prefixed_key(mock_client, mock_bucket):
    bucket_name = "test-bucket"
    file_key = "prefix/test-file"

    write_object_to_s3_bucket(bucket_name, file_key, "test\n")

    response = mock_client.get_object(Bucket=bucket_name, Key=file_key)

    assert response["Body"].read().decode("utf_8") == "test\n"


def test_write_object_to_s3_bucket_correctly_writes_binary_data(
    mock_client, mock_bucket
):
    bucket_name = "test-bucket"
    file_key = "test-file"
    df = pd.DataFrame(
        {
            "one": [-1, 0, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )
    parquet_data = convert_dataframe_to_parquet(df)

    write_object_to_s3_bucket(bucket_name, file_key, parquet_data, binary=True)

    response = mock_client.get_object(Bucket=bucket_name, Key=file_key)
    pq_file = io.BytesIO(response["Body"].read())
    retrieved_df = pd.read_parquet(pq_file)

    assert retrieved_df.equals(df)
