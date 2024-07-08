from pg8000.native import identifier, Connection
import datetime


def get_table(
    table_name: str,
    conn: Connection,
    last_timestamp: datetime.datetime = datetime.datetime.min,
) -> list[dict]:
    """Fetches newly created or updated rows (since last_timestamp) from a table.

    Uses a pg8000 connection to a PostgreSQL database. Valid on tables with
    `last_updated` and `created_at` columns containing SQL date-type data.

    Args:
        table_name: A string of the name of the table to be queried.
        conn: A pg8000.native connection.
        last_timestamp: A Python datetime.datetime object.

    Returns:
        A list of dictionaries containing data from all columns of the rows
        fulfilling the query criteria.
    """
    try:
        query = f"SELECT * FROM {identifier(table_name)} "
        query += "WHERE last_updated > :last_timestamp OR created_at > :last_timestamp"
        result = conn.run(query, last_timestamp=last_timestamp)
        output_list = [
            dict(zip([column["name"] for column in conn.columns], r)) for r in result
        ]
        return output_list

    except Exception as e:
        raise e
