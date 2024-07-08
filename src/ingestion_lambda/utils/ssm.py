import boto3
from botocore.exceptions import ClientError

try:
    from utils.custom_exceptions import *
except ModuleNotFoundError:
    from src.custom_exceptions import *


def get_parameter(param: str):
    """Retrieves a parameter from AWS Systems Manager Parameter Store.

    This function uses the boto3 SSM client get_parameter method to attempt to
    retrieve the value of the parameter.

    Args:
        param: A string of the name of the parameter.

    Returns:
        A string of the value of the parameter.

    Raises:
        A custom exception named after the "Code" in the Boto3 error response
        if found in the exceptions at src.custom_exceptions, otherwise a
        botocore.exceptions.ClientError
    """
    ssm_client = boto3.client("ssm")

    try:
        response = ssm_client.get_parameter(Name=param)

        return response["Parameter"]["Value"]

    except ClientError as e:
        error_handler(e)

        raise ClientError(e.response, e.operation_name)


def set_parameter(param: str, value: str):
    """Stores a parameter in AWS Systems Manager Parameter Store.

    This function uses the boto3 SSM client put_parameter method to attempt to
    store the value of the parameter.

    Args:
        param: A string of the name of the parameter.
        value: A string of the value to be set for the parameter.

    Returns:
        None.

    Raises:
        A custom exception named after the "Code" in the Boto3 error response
        if found in the exceptions at src.custom_exceptions, otherwise a
        botocore.exceptions.ClientError
    """
    ssm_client = boto3.client("ssm")

    try:
        ssm_client.put_parameter(Name=param, Value=value, Type="String", Overwrite=True)

    except ClientError as e:
        error_handler(e)

        raise ClientError(e.response, e.operation_name)
