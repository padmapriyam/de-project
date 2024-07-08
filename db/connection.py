import pg8000.native
from os import environ

username = environ.get("PGUSER")
password = environ.get("PGPASSWORD")
host = environ.get("PGHOST", "localhost")
port = environ.get("PGPORT", "5432")
database = environ.get("PGDATABASE")
con = pg8000.native.Connection(
    username, password=password, host=host, port=port, database=database
)
