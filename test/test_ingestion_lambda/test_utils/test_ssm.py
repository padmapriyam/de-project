import pytest
from src.custom_exceptions import *
from src.ingestion_lambda.utils.ssm import get_parameter, set_parameter
import boto3
from moto import mock_aws
import os


@pytest.fixture(scope="function")
def ssm_client(aws_creds):
    with mock_aws():
        yield boto3.client("ssm")


@pytest.fixture(scope="class")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


class TestGetParameter:
    """Tests the get_parameter helper."""

    @pytest.mark.it("unit test: get_parameter returns existing parameter")
    def test_get_parameter_with_valid_parameter(self, ssm_client):
        parameter_name = "test_parameter"
        parameter_value = "test_value"
        ssm_client.put_parameter(
            Name=parameter_name, Value=parameter_value, Type="String"
        )

        result = get_parameter(parameter_name)

        assert result == parameter_value

    @pytest.mark.it(
        "unit test: get_parameter raises ParameterNotFound for nonexistent parameter"
    )
    def test_get_parameter_with_invalid_parameter(self, ssm_client):
        parameter_name = "test_parameter"
        parameter_value = "test_value"
        ssm_client.put_parameter(
            Name=parameter_name, Value=parameter_value, Type="String"
        )
        invalid_parameter = "wrong"

        with pytest.raises(ParameterNotFound):
            get_parameter(invalid_parameter)


class TestSetParameter:
    """Tests the set_parameter helper."""

    @pytest.mark.it("unit test: set_parameter sets parameter")
    def test_set_parameter(self, ssm_client):
        parameter_name = "test_parameter"
        parameter_value = "test_value"

        set_parameter(parameter_name, parameter_value)

        stored_value = ssm_client.get_parameter(Name=parameter_name)["Parameter"][
            "Value"
        ]

        assert stored_value == parameter_value

    @pytest.mark.it("unit test: set_parameter updates value of parameter")
    def test_set_parameter_updates_value(self, ssm_client):
        parameter_name = "test_parameter"
        parameter_value_initial = "test_value_1"
        parameter_value_final = "test_value_2"
        ssm_client.put_parameter(
            Name=parameter_name, Value=parameter_value_initial, Type="String"
        )

        set_parameter(parameter_name, parameter_value_final)

        stored_value = get_parameter(parameter_name)

        assert stored_value == parameter_value_final
