import os
import json
import boto3
import pytest
from moto import mock_aws
from src.processing_lambda.lambda_handler import lambda_handler
import datetime
from unittest.mock import patch


@pytest.fixture(scope="function")
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
def s3_processed_bucket(s3_client):
    bucket_name = "de-watershed-processed-bucket"
    region = "eu-west-2"
    bucket = s3_client.create_bucket(
        Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region}
    )
    return bucket_name


@pytest.fixture
def add_bucket_object(s3_client, s3_bucket):
    json_data = """{"col1": 1, "col2": "value1", "col3": true, "created_at": "time", "last_updated": "time"}
                    {"col1": 2, "col2": "value2", "col3": false, "created_at": "time", "last_updated": "time"}
                    {"col1": 3, "col2": "value3", "col3": true, "created_at": "time", "last_updated": "time"}"""

    key = "address/"
    s3_client.put_object(Bucket=s3_bucket, Key=key, Body=json_data.encode("utf-8"))
    return key


@pytest.fixture
def event(s3_bucket, add_bucket_object):
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": s3_bucket, "arn": f"arn:aws:s3:::{s3_bucket}"},
                    "object": {
                        "key": add_bucket_object,
                        "size": 1024,
                        "eTag": "0123456789abcdef0123456789abcdef",
                        "sequencer": "0123456789ABCDEF",
                    },
                }
            }
        ]
    }
    return event


def test_function_reads_table_data_and_converts_to_parquet(
    s3_client, s3_bucket, s3_processed_bucket, add_bucket_object, event
):

    lambda_handler(event, None)
    response = s3_client.list_objects_v2(Bucket=s3_processed_bucket)
    objects = response.get("Contents", [])
    assert len(objects) == 1

    processed_key = objects[0]["Key"]

    assert processed_key.endswith(".parquet")


@patch("src.processing_lambda.lambda_handler.read_object_into_dataframe")
def test_read_object_from_s3_error_handling(
    mock_read_object, s3_client, s3_bucket, event, caplog
):
    mock_read_object.side_effect = Exception("Mocked S3 read error")
    lambda_handler(event, None)
    assert "Error reading data from ingestion bucket into dataframe" in caplog.text


@patch("src.processing_lambda.lambda_handler.write_object_to_s3_bucket")
def test_write_object_to_s3_error_handling(
    mock_write_object, s3_client, s3_bucket, s3_processed_bucket, event, caplog
):
    mock_write_object.side_effect = Exception("Mocked S3 write error")
    lambda_handler(event, None)
    assert "Error writing parquet data to processed s3 bucket" in caplog.text
