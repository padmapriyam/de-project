import boto3
import pandas as pd
import io

def read_processed_into_df(bucket_name, key):
    """This function is used to read data newly added into processing bucket into dataframe, ready for insertion into the warehouse.

    Args:
        bucket_name: the name of the bucket to access tables containing parquet data from, in this case, the processing s3 bucket.
        key: the filepath within the bucket to the parquet file to be read into a dataframe.

    Returns:
        A dataframe of the newly processed parquet data.

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
        df = pd.read_parquet(io.BytesIO(body))
        return df
    except Exception as e:
        raise ValueError(f"Error reading or processing the object from S3: {e}")
