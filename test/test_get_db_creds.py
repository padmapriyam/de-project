import os
import pytest
import boto3
from moto import mock_aws
from botocore.exceptions import ClientError
from src.get_db_creds import get_database_credentials


@pytest.fixture(scope="class")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    yield


@pytest.fixture(scope="function")
def sm_client(aws_creds):
    with mock_aws():
        yield boto3.client("secretsmanager")


class TestRetrieveSecret:
    def test_get_database_credentials_finds_credentials(self, sm_client):
        sm_client.create_secret(
            Name="database_credentials",
            SecretString='{"database": "test_db", "username": "test_user"}',
        )

        assert get_database_credentials("database_credentials") == {
            "database": "test_db",
            "username": "test_user",
        }

    def test_get_database_credentials_returns_client_error(self, sm_client):
        with pytest.raises(ClientError):
            get_database_credentials("database_credentials")
