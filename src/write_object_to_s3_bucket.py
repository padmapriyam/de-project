import boto3
from botocore.exceptions import ClientError

# from hashlib import sha256
try:
    from utils.custom_exceptions import *
except ModuleNotFoundError:
    from src.custom_exceptions import *


client = boto3.client("s3")


def write_object_to_s3_bucket(
    bucket_name: str, file_key: str, data: str | bytes, binary: bool = False
) -> str:
    """Writes a new object to an S3 bucket.

    This function uses the boto3 S3 client put_object method to attempt to
    write the provided data to provided key in the specified bucket.
    The data will be UTF-8 encoded if it is a string.

    Args:
        bucket_name: A string of the name of the destination S3 bucket.
        file_key: A string of the target file name (including prefix if
          applicable) to which to save the data in S3.
        data: Data to be written to the body of the file.
        binary: Boolean value indicating whether data arg is binary.

    Returns:
        A string reporting success if successful.

    Raises:
        A custom exception named after the "Code" in the Boto3 error response
        if found in the exceptions at src.custom_exceptions, otherwise a
        botocore.exceptions.ClientError
    """
    try:
        body = data if binary else data.encode("utf_8")
        response = client.put_object(
            Body=body,
            Bucket=bucket_name,
            # ChecksumSHA256 = sha256(bytes(data, encoding='utf_8')),
            Key=file_key,
        )

        if (
            "ResponseMetadata" in response
            and "HTTPStatusCode" in response["ResponseMetadata"]
            and response["ResponseMetadata"]["HTTPStatusCode"] == 200
        ):
            return f"File {file_key} successfully written to bucket {bucket_name}"

    except ClientError as e:
        error_handler(e)

        raise ClientError(e.response, e.operation_name)
