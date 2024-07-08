import boto3
import pandas as pd
import io


def read_object_into_dataframe(bucket_name, key):
    """This function is used to read data newly ingested json lines data from the table folders in the ingestion s3 bucket, into a dataframe, ready for transformation in one of the specific transformation functions.

    Args:
        bucket_name: the name of the bucket to access tables containing json lines data from, in this case, the imgestion s3 bucket.
        key: the filepath within the bucket to the json lines file to be read into a dataframe.

    Returns:
        A dataframe of the newly ingested json lines data.

    Raises:
        TyperError is the bucket_name or key arguments passed are not strings.
    """
    if not isinstance(bucket_name, str):
        raise TypeError("bucket_name must be a string")

    if not isinstance(key, str):
        raise TypeError("the specified key must be a string")

    try:
        s3_client = boto3.client("s3")
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        body = response["Body"].read()
        df = pd.read_json(io.BytesIO(body), lines=True)
        return df
    except Exception as e:
        raise ValueError(f"Error reading or processing the object from S3: {e}")
