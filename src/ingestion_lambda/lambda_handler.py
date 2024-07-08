import boto3
from botocore.exceptions import ClientError
import datetime
import logging

if __name__ == "__main__" or __name__ == "lambda_handler":
    from utils.connect import connect_db
    from utils.get_table import get_table
    from utils.convert_results_to_json_lines import convert_results_to_json_lines
    from utils.custom_exceptions import *
    from utils.write_object_to_s3_bucket import write_object_to_s3_bucket
    from utils.ssm import get_parameter, set_parameter
else:
    from src.ingestion_lambda.utils.connect import connect_db
    from src.ingestion_lambda.utils.get_table import get_table
    from src.ingestion_lambda.utils.convert_results_to_json_lines import (
        convert_results_to_json_lines,
    )
    from src.custom_exceptions import *
    from src.write_object_to_s3_bucket import write_object_to_s3_bucket
    from src.ingestion_lambda.utils.ssm import get_parameter, set_parameter

client = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TIMESTAMP_PARAM = "timestamp_of_last_successful_execution"


def lambda_handler(event: dict, context):
    """Fetches new data from ingestion source db and writes to ingestion bucket.

    Records current time at start of execution. Fetches time of last successful
    execution using get_parameter. If no value is returned, uses the earliest
    date+time representable as a datetime object. Uses this time in calls to
    get_table, which returns a list of dictionaries of rows that have been
    created or updated since this reference timestamp.

    Any records returned from this call are saved into the ingestion S3 bucket
    in JSON Lines format in a new file prefixed with the appropriate table name.

    If this all executes without a problem, set_parameter updates the timestamp
    of last successful execution with the value set at the beginning of the
    function.

    Args:
        event: A dictionary of values passed to the Lambda function.
        context: An awslambdaric.lambda_context.LambdaContext object.

    Returns:
        None.

    Raises:
        A custom exception named after the "Code" in the Boto3 error response
        if found in the exceptions at src.custom_exceptions, otherwise a
        botocore.exceptions.ClientError
    """

    curr_timestamp = datetime.datetime.now(datetime.UTC)
    curr_timestamp_string = curr_timestamp.strftime("%Y-%m-%d_%H-%M-%S")

    try:
        last_timestamp = get_parameter(TIMESTAMP_PARAM)
        last_timestamp = datetime.datetime.fromisoformat(last_timestamp)

    except ParameterNotFound:
        last_timestamp = datetime.datetime.min

    except ClientError as e:
        error_handler(e)

        raise ClientError(e.response, e.operation_name)

    tables = [
        "address",
        "counterparty",
        "currency",
        "department",
        "design",
        "payment_type",
        "staff",
        "purchase_order",
        "sales_order",
        "transaction",
        "payment",
    ]

    conn = None

    results = {}
    output = {}

    try:
        conn = connect_db()
    except Exception as e:
        logger.error(e)

    for table in tables:
        try:
            results[table] = get_table(table, conn, last_timestamp)
            logger.info(f"get_table ran successfully on table '{table}'")
        except Exception as e:
            logger.error(e)

    if conn:
        conn.close()

    for table in results:
        if results[table]:
            logger.info(f"New/Updated data found in '{table}'")
            output[table] = convert_results_to_json_lines(results[table])
        else:
            logger.info(f"No new/updated data found in '{table}'")

    for table in output:
        logger.info(f"Attempting to write '{table}' data into S3")
        write_object_to_s3_bucket(
            "de-watershed-ingestion-bucket",
            f"{table}/{curr_timestamp_string}.jsonl",
            output[table],
        )
        logger.info(f"Data for table '{table}' successfully written to S3")

    set_parameter(TIMESTAMP_PARAM, curr_timestamp.isoformat())
    logger.info("Parameter has been updated with the recent timestamp")
