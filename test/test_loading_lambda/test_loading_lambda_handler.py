import logging
import pytest
import pandas as pd
from unittest.mock import patch
from src.loading_lambda.lambda_handler import lambda_handler

@pytest.fixture
def event():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "mock_bucket", "arn": f"arn:aws:s3:::mock_bucket"},
                    "object": {
                        "key": "mock_table_name",
                        "size": 1024,
                        "eTag": "0123456789abcdef0123456789abcdef",
                        "sequencer": "0123456789ABCDEF",
                    },
                }
            }
        ]
    }
    return event

def test_lambda_handler_logs_error_read_data(caplog,event):
    caplog.set_level(logging.ERROR)
    with (
        patch("src.loading_lambda.lambda_handler.connect_dw") as mock_conn,
        patch("src.loading_lambda.lambda_handler.loading_to_sql") as mock_loading_to_sql,
        patch("src.loading_lambda.lambda_handler.read_processed_into_df") as mock_read_to_df
    ):
        mock_read_to_df.side_effect= Exception("read data error")
        lambda_handler(event,None)
    assert "Error reading data from processed bucket into dataframe." in caplog.text

def test_lambda_handler_logs_error_loading_into_sql(caplog, event):
    caplog.set_level(logging.ERROR)
    with (
        patch("src.loading_lambda.lambda_handler.connect_dw") as mock_conn,
        patch("src.loading_lambda.lambda_handler.loading_to_sql") as mock_loading_to_sql,
        patch("src.loading_lambda.lambda_handler.read_processed_into_df") as mock_read_to_df
    ):  
        mock_read_to_df.return_value = pd.DataFrame()
        mock_loading_to_sql.side_effect= Exception("writing into warehouse error")
        lambda_handler(event,None)
    assert "Error writing into warehouse from dataframe." in caplog.text
    

def test_lambda_handler_logs_successful(caplog, event):
    caplog.set_level(logging.INFO)
    with (
        patch("src.loading_lambda.lambda_handler.connect_dw") as mock_conn,
        patch("src.loading_lambda.lambda_handler.loading_to_sql") as mock_loading_to_sql,
        patch("src.loading_lambda.lambda_handler.read_processed_into_df") as mock_read_to_df
    ):  
        mock_loading_to_sql.return_value = 5
        mock_read_to_df.return_value = pd.DataFrame()
        lambda_handler(event,None)
    assert f"Wrote 5 rows into mock_table_name warehouse" in caplog.text
