import json
import os
from unittest.mock import patch
import pytest
import boto3
from moto import mock_aws
import sqlparse
from fastapi.testclient import TestClient
from src.api.main import app
from src.utils.connection import connect_to_db, close_db_connection
from src.utils.aws_utils import USERS_BUCKET_NAME

####################################
# DB CONNECTION                    #
####################################


@pytest.fixture()
def table_columns() -> list[dict]:
    """Returns a test response for db_conn.columns

    Returns:
        list[dict]: A list of dictionaries for each column metadata
    """
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
    """Yields a db connection"""    
    conn = connect_to_db()
    yield conn
    close_db_connection(conn)


####################################
# DB SEEDIING                      #
####################################


@pytest.fixture(autouse=True)
def seed_database(db_conn):
    """Runs a seed sql file to seed db with each test

    Args:
        db_conn (connection): connection to the database
    """    
    conn = db_conn
    sql_data = open("tests/seed-db-data/seed.sql", "r")
    queries = sqlparse.split(sql_data.read())

    for query in queries:
        conn.run(query)

    yield
    sql_data.close()


####################################
# AWS MOTO MOCKING                 #
####################################


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture
@mock_aws
def s3_client(aws_credentials):
    """Yields an s3 client for aws resource mocking

    Args:
        aws_credentials (fixture): aws credentials for testing

    Yields:
        boto3.client: mocked s3 client
    """    
    s3_client = boto3.client("s3", region="eu-west-2")
    yield s3_client


@pytest.fixture
@mock_aws
def s3_client_with_bucket(s3_client):
    """Yields a mocked s3 client with a bucket

    Args:
        s3_client: mocked s3 client

    Yields:
        s3_client: s3 client with bucket
    """    
    s3_client.create_bucket(
        Bucket=USERS_BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )

    yield s3_client


@pytest.fixture
@mock_aws
def s3_client_with_object(s3_client_with_bucket):
    """Yields a mocked s3 client with object

    Args:
        s3_client_with_bucket: mocked s3 client with bucket

    Yields:
        s3_client: s3 client with bucket and object
    """    
    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "object"}), Bucket=USERS_BUCKET_NAME, Key="new-file"
    )

    yield s3_client_with_bucket


@pytest.fixture
@mock_aws
def s3_client_with_objects(s3_client_with_bucket):
    """Yields a mocked s3 client with objects

    Args:
        s3_client_with_bucket: mocked s3 client with bucket

    Yields:
        s3_client: s3 client with bucket and objects
    """    
    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "object"}),
        Bucket=USERS_BUCKET_NAME,
        Key="store/new-file",
    )

    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "dict"}),
        Bucket=USERS_BUCKET_NAME,
        Key="store/newer-file",
    )

    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "dict"}), Bucket=USERS_BUCKET_NAME, Key="some-file"
    )

    yield s3_client_with_bucket


@pytest.fixture
@mock_aws
def s3_client_with_user_objects(s3_client_with_bucket):
    """Yields a mocked s3 client with objects with user-{id} prefix

    Args:
        s3_client_with_bucket: mocked s3 client with bucket

    Yields:
        s3_client: s3 client with bucket and objects with user-{id} prefix
    """    
    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "object"}),
        Bucket=USERS_BUCKET_NAME,
        Key="user-1/store/new-file",
    )

    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "dict"}),
        Bucket=USERS_BUCKET_NAME,
        Key="user-1/store/newer-file",
    )

    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "dict"}),
        Bucket=USERS_BUCKET_NAME,
        Key="user-1/some-file",
    )

    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "dict"}),
        Bucket=USERS_BUCKET_NAME,
        Key="user-2/some-file",
    )

    yield s3_client_with_bucket


####################################
# FASTAPI TEST CLIENT              #
####################################


@pytest.fixture
def test_client():
    """Returns a FastAPI test client"""
    client = TestClient(app)
    return client


####################################
# AWS UTIL RESPONSE PATCH          #
####################################


@pytest.fixture()
def s3_post_mock():
    """Mocks the response from the insert_into_bucket aws util

    Yields:
        mock: mock with return value of response expected
    """    
    with patch("src.api.main.insert_into_bucket") as mock:
        mock.return_value = {
            "picture_name": "new-pic.jpeg",
            "s3_key_name": "user-1/summer/new-pic.jpeg",
            "date_created": "2025-05-24",
            "picture_description": "test picture",
            "album_name": "summer",
        }
    yield mock


@pytest.fixture()
def s3_delete_mock_success():
    """Mocks the response from the delete_from_bucket aws util

    Yields:
        mock: mock with return value of success response expected
    """   
    with patch("src.api.main.insert_into_bucket") as mock:
        mock.return_value = {"Success": "Object deleted successfully"}
    yield mock


@pytest.fixture()
def s3_delete_mock_error():
    """Mocks the response from the delete_from_bucket aws util

    Yields:
        mock: mock with return value of error response expected
    """
    with patch("src.api.main.insert_into_bucket") as mock:
        mock.return_value = {
            "error": "Deletion unsuccessful. Try again later",
            "details": "arbitrary error",
        }
    yield mock
