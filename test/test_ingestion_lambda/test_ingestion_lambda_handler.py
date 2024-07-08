from src.ingestion_lambda.lambda_handler import lambda_handler
import datetime
import logging
from unittest.mock import patch


def test_lambda_handler_logs_successful_table_reads(caplog):
    caplog.set_level(logging.INFO)
    with (
        patch("src.ingestion_lambda.lambda_handler.get_table") as mock_get_table,
        patch(
            "src.ingestion_lambda.lambda_handler.set_parameter"
        ) as mock_set_parameter,
        patch(
            "src.ingestion_lambda.lambda_handler.write_object_to_s3_bucket"
        ) as mock_write_to_s3,
    ):
        mock_get_table.return_value = []
        lambda_handler(None, None)

    for table in [
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
    ]:
        assert f"get_table ran successfully on table '{table}'" in caplog.text


def test_lambda_handler_logs_successful_s3_writes(caplog):
    caplog.set_level(logging.INFO)
    with (
        patch("src.ingestion_lambda.lambda_handler.get_table") as mock_get_table,
        patch(
            "src.ingestion_lambda.lambda_handler.set_parameter"
        ) as mock_set_parameter,
        patch(
            "src.ingestion_lambda.lambda_handler.write_object_to_s3_bucket"
        ) as mock_write_to_s3,
    ):
        mock_get_table.return_value = [{"test": True}]

        lambda_handler(None, None)

    for table in [
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
    ]:
        assert f"Data for table '{table}' successfully written to S3" in caplog.text
