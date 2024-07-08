import logging

if __name__ == "lambda_handler":
    from utils.loading_to_sql import loading_to_sql
    from utils.read_processed_object_to_df import read_processed_into_df
    from utils.connect_dw import connect_dw
else:
    from src.loading_lambda.utils.loading_to_sql import loading_to_sql
    from src.loading_lambda.utils.read_processed_object_to_df import (
        read_processed_into_df,
    )
    from src.loading_lambda.utils.connect_dw import connect_dw


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    table_name = key.split("/")[0]

    logger.info(f"Processing file {key} from bucket {bucket_name}")

    try:
        df = read_processed_into_df(bucket_name, key)
    except Exception as e:
        logger.error(f"Error reading data from processed bucket into dataframe.{e}")
        return

    conn = None
    try:
        conn = connect_dw("data_warehouse_credentials")
    except Exception as e:
        logger.error(e)
        raise

    logger.info(f"Attempting to write data from {table_name} into warehouse")

    try:
        rows = loading_to_sql(table_name, conn, df)
        logger.info(f"Wrote {rows} rows into {table_name} warehouse")
    except Exception as e:
        logger.error(f"Error writing into warehouse from dataframe. {e}")
    finally:
        if conn:
            conn.dispose()
