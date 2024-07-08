from src.loading_lambda.utils.loading_to_sql import loading_to_sql
from unittest.mock import patch
import pytest
import pandas as pd
import os
from dotenv import load_dotenv
import sqlalchemy as sa
from sqlalchemy import create_engine, text


@pytest.fixture
def db_con():

    load_dotenv()
    db_string = sa.engine.url.URL.create(
        drivername="postgresql+pg8000",
        username=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"],
        database=os.environ["PGDATABASE"],
    )
    db_engine = create_engine(db_string)

    return db_engine


@patch(
    "src.loading_lambda.utils.loading_to_sql.get_database_credentials",
    return_value={"schema": "public"},
)
def test_loading_to_sql_writes_to_database(patched_get_db_creds, db_con):

    df = pd.DataFrame(
        {"col1": ["Hello", "my", "friend"], "col2": ["Goodbye", "my", "friend"]}
    )

    with db_con.connect() as con:
        con.execute(text(f"DROP TABLE IF EXISTS test;"))
        con.commit()

    loading_to_sql("test", db_con, df)
    output = pd.read_sql("SELECT * FROM test", con=db_con)

    assert output.shape == (3, 2)
    assert list(output.columns) == ["col1", "col2"]
    assert output.equals(df)
