import sqlalchemy as sa
from sqlalchemy import create_engine
try:
    from utils.get_db_creds import get_database_credentials
except ModuleNotFoundError: 
    from src.get_db_creds import get_database_credentials

def connect_dw(db_id):
    """Connects to a PostgreSQL database using sqlalchemy.

    This function uses the get_database_credentials function to retrieve the
    necessary credentials for the data warehouse, which
    are stored in AWS secrets manager.

    Args:
        secret_id: The relevant db_id for retrieving credentials

    Returns:
        An instance of the sqlalchemy.engine.base.Engine class.
    """
    db_creds = get_database_credentials(db_id)

    db_string = sa.engine.url.URL.create(
                drivername="postgresql+pg8000",
                username=db_creds["username"],
                password=db_creds["password"],
                host=db_creds["hostname"],
                port=db_creds["port"],
                database=db_creds["database"])

    db_engine = create_engine(db_string)

    return db_engine