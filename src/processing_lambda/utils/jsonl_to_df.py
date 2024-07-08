import boto3
import pandas as pd
import io
from botocore.exceptions import ClientError

try:
    from utils.custom_exceptions import *
except ModuleNotFoundError:
    from src.custom_exceptions import *

tables = [
    "counterparty",
    "currency",
    "department",
    "design",
    "staff",
    "sales_order",
    "address",
    "payment",
    "purchase_order",
    "payment_type",
    "transaction",
]


def get_df_from_s3_bucket(table_name):
    #    """
    #    Retrieves and concatenates JSON Lines files into a single DataFrame.
    #     This function lists all objects in the specified S3 bucket with the given prefix (table_name),
    #     reads each object as a JSON Lines file, and concatenates the contents into a single Pandas DataFrame.
    #     Args:
    #         table_name: A string representing the prefix of the objects(table name) to retrieve from the S3 bucket.
    #     Returns:
    #         A Pandas DataFrame containing the concatenated data from all the JSON Lines in the table.
    #     Raises:
    #         NoSuchKey: If the df is empty, no such table exists
    #         ClientError: If there's an issue with accessing the S3 bucket or its contents.
    #     """
    s3_client = boto3.client("s3")
    df = pd.DataFrame()
    try:
        objects = s3_client.list_objects_v2(
            Bucket="de-watershed-ingestion-bucket", Prefix=table_name
        ).get("Contents", [])
        for obj in objects:
            file = s3_client.get_object(
                Bucket="de-watershed-ingestion-bucket", Key=obj["Key"]
            )
            content = file["Body"].read().decode("utf-8")
            obj_df = pd.read_json(io.StringIO(content), lines=True)
            df = pd.concat([df, obj_df], ignore_index=True)
        if df.empty:
            raise NoSuchTable
        return df
    except ClientError as e:
        error_handler(e)
        raise ClientError(e.response, e.operation_name)


def get_latest_df_from_s3_bucket(key):
    #    """
    #    Retrieves and concatenates JSON Lines files into a single DataFrame.
    #     This function takes a key and reads the object as a JSON Lines file, and concatenates the contents into a single Pandas DataFrame.
    #     Args:
    #         key: A string representing the object to retrieve from the S3 bucket.
    #     Returns:
    #         A Pandas DataFrame containing the concatenated data from all the JSON Lines in the table.
    #     Raises:
    #         NoSuchKey: If the df is empty, no such key exists
    #         ClientError: If there's an issue with accessing the S3 bucket or the key.
    #     """
    try:
        s3_client = boto3.client("s3")
        file = s3_client.get_object(Bucket="de-watershed-ingestion-bucket", Key=key)
        content = file["Body"].read().decode("utf-8")
        df = pd.read_json(io.StringIO(content), lines=True)
        if df.empty:
            raise NoSuchKey
        return df
    except ClientError as e:
        error_handler(e)
        raise ClientError(e.response, e.operation_name)
