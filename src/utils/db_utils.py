from src.utils.connection import connect_to_db, close_db_connection
from pg8000.exceptions import DatabaseError


def get_table_columns(columns: list) -> list[str]:
    """Returns table columns in a list for a given query

    Args:
        columns (list): for a connection object, connection.columns

    Returns:
        list[str]: list of column names in the query table
    """
    table_columns = []
    if isinstance(columns, list) and columns:
        table_columns = [col["name"] for col in columns]
    return table_columns


def run_query(query: str, json_key: str | None = None) -> dict | list:
    """Runs the specified query and returns the result in a dict/json.

    Args:
        query (str): the query string
        json_key (str): json key for the json result

    Returns:
        dict: dict of {json_key: result[list]}
              OR
              list  if json_key is not provided

    """
    db_conn = None

    try:
        db_conn = connect_to_db()
        db_result = db_conn.run(query)

    except DatabaseError as e:
        print(e)
        return {"message": "Error occured during database operation"}

    else:
        table_columns = get_table_columns(db_conn.columns)
        result = [dict(zip(table_columns, record)) for record in db_result]

        if db_conn:
            close_db_connection(db_conn)
        if json_key:
            return {json_key: result}
        else:
            return result
