import pytest
import pandas as pd 
import boto3
from moto import mock_aws
import os 
from src.loading_lambda.utils.read_processed_object_to_df import read_processed_into_df

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
def add_bucket_object(s3_client, s3_bucket):
    
    df = pd.DataFrame({
        "col1" : ["hello", "my", "friend"],
        "col2" : ["goodbye", "my", "friend"],

    })

    df_parquet = df.to_parquet()


    key = "address/"
    s3_client.put_object(Bucket=s3_bucket, Key=key, Body=df_parquet)
    return key


def test_read_processed_into_df_returns_a_dataframe(add_bucket_object, s3_bucket):

    key = add_bucket_object
    df = read_processed_into_df(s3_bucket, key)

    assert isinstance(df, pd.DataFrame)


def test_read_processed_into_df_returns_correct_columns(add_bucket_object, s3_bucket):

    key = add_bucket_object
    df = read_processed_into_df(s3_bucket, key)

    assert list(df.columns) == ["col1", "col2"]
    assert len(df) == 3


def test_read_processed_into_df_returns_error_when_key_not_found(s3_bucket):

    with pytest.raises(ValueError):
        read_processed_into_df(s3_bucket, 'hello')


def test_read_processed_into_df_returns_error_when_no_bucket():

    with pytest.raises(ValueError):
        read_processed_into_df("1", "2")


def test_read_processed_into_df_returns_message_when_not_str():

    with pytest.raises(TypeError):
        read_processed_into_df(1, 2)


# def test_read_processed_into_df_returns_