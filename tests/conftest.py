import os
from unittest.mock import Mock
import pytest
import boto3
from moto import mock_aws
import sqlparse
from src.utils.connection import connect_to_db, close_db_connection


@pytest.fixture()
def table_columns():
    cols = [
        {
            "table_oid": ...,
            "column_attrnum": 1,
            "type_oid": 23,
            "type_size": 4,
            "type_modifier": -1,
            "format": 0,
            "name": "id",
        },
        {
            "table_oid": ...,
            "column_attrnum": 2,
            "type_oid": 25,
            "type_size": -1,
            "type_modifier": -1,
            "format": 0,
            "name": "name",
        },
    ]
    
    return cols


@pytest.fixture()
def db_conn():
    conn = connect_to_db()
    yield conn
    close_db_connection(conn)


@pytest.fixture(autouse=True)
def seed_database(db_conn):
    conn = db_conn
    sql_data = open("tests/seed-db-data/seed.sql", "r")
    queries = sqlparse.split(sql_data.read())

    for query in queries:
        conn.run(query)

    yield
    sql_data.close()



