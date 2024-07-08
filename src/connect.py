import pg8000.native
import os

# from dotenv import load_dotenv
try:
    from utils.get_db_creds import get_database_credentials
except ModuleNotFoundError:
    from src.ingestion_lambda.utils.get_db_creds import get_database_credentials

# load_dotenv()


def connect_db(db_id = "database_credentials") -> pg8000.native.Connection:
    """Connects to a PostgreSQL database using pg8000.

    This function uses the get_database_credentials function to retrieve the
    necessary credentials for the totesys database or the data warehouse, which
    are stored in AWS secrets manager.

    Args:
        secret_id: The relevant db_id for retrieving credentials

    Returns:
        An instance of the pg8000.native.Connection class.
    """
    return pg8000.native.Connection(
        user=get_database_credentials(db_id)["username"],
        password=get_database_credentials(db_id)["password"],
        database=get_database_credentials(db_id)["database"],
        host=get_database_credentials(db_id)["hostname"],
        port=str(get_database_credentials(db_id)["port"]),
    )
