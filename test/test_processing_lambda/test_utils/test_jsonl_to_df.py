import os
import pytest
import boto3
import pandas as pd
from moto import mock_aws
from botocore.exceptions import ClientError
from src.custom_exceptions import *
from unittest.mock import patch
from src.processing_lambda.utils.jsonl_to_df import (
    get_df_from_s3_bucket,
    get_latest_df_from_s3_bucket,
)


@pytest.fixture(scope="function")
def s3_client(aws_creds):
    with mock_aws():
        yield boto3.client("s3", region_name="eu-west-2")


@pytest.fixture(scope="function")
def ingestion_bucket(s3_client):
    s3_client.create_bucket(
        Bucket="de-watershed-ingestion-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    s3_client.put_object(
        Bucket="de-watershed-ingestion-bucket",
        Key="test/file1.jsonl",
        Body=b'{"key": "value1"}\n{"key": "value2"}',
    )
    s3_client.put_object(
        Bucket="de-watershed-ingestion-bucket",
        Key="test/file2.jsonl",
        Body=b'{"key": "value3"}\n{"key": "value4"}',
    )
    s3_client.put_object(
        Bucket="de-watershed-ingestion-bucket",
        Key="table/key_parameter.jsonl",
        Body=b'{"key": "value1"}\n{"key": "value2"}\n{"key": "value3"}',
    )


@pytest.fixture(scope="class")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


def test_json_to_df_returns_df_object(s3_client, ingestion_bucket):
    result = get_df_from_s3_bucket("test")
    assert isinstance(result, pd.DataFrame)


def test_json_to_df_raises_error_when_invalid_table_given(s3_client, ingestion_bucket):
    with pytest.raises(NoSuchTable):
        get_df_from_s3_bucket("test1234")


def test_json_to_df_concat_all_the_jsonl_files(s3_client, ingestion_bucket):
    result = get_df_from_s3_bucket("test")
    assert len(result["key"]) == 4
    assert result.loc[3]["key"] == "value4"


def test_json_to_df_returns_lastest_df_from_file(s3_client, ingestion_bucket):
    result = get_latest_df_from_s3_bucket("table/key_parameter.jsonl")
    assert len(result["key"]) == 3
    assert result.loc[0]["key"] == "value1"


def test_json_to_latest_df_raises_error_when_invalid_key_given(
    s3_client, ingestion_bucket
):
    with pytest.raises(NoSuchKey):
        get_latest_df_from_s3_bucket("lalalala")
