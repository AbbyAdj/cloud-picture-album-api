import json
import os
from unittest.mock import Mock
import pytest
import boto3
from moto import mock_aws
import sqlparse
from src.utils.connection import connect_to_db, close_db_connection
from src.utils.aws_utils import USERS_BUCKET_NAME

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
    s3_client = boto3.client("s3", region="eu-west-2")
    yield s3_client


@pytest.fixture
@mock_aws
def s3_client_with_bucket(s3_client):
    s3_client.create_bucket(Bucket=USERS_BUCKET_NAME,
                            CreateBucketConfiguration={
                                "LocationConstraint":"eu-west-2"
                            })
    
    yield s3_client


@pytest.fixture
@mock_aws
def s3_client_with_object(s3_client_with_bucket):
    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "object"}),
        Bucket= USERS_BUCKET_NAME,
        Key="new-file"
    )

    yield s3_client_with_bucket
    
    
@pytest.fixture
@mock_aws
def s3_client_with_objects(s3_client_with_bucket):
    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "object"}),
        Bucket= USERS_BUCKET_NAME,
        Key="store/new-file"
    )    
    
    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "dict"}),
        Bucket= USERS_BUCKET_NAME,
        Key="store/newer-file"
    )   

    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "dict"}),
        Bucket= USERS_BUCKET_NAME,
        Key="some-file"
    )

    yield s3_client_with_bucket


@pytest.fixture
@mock_aws
def s3_client_with_user_objects(s3_client_with_bucket):
    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "object"}),
        Bucket= USERS_BUCKET_NAME,
        Key="user-1/store/new-file"
    )    
    
    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "dict"}),
        Bucket= USERS_BUCKET_NAME,
        Key="user-1/store/newer-file"
    )   

    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "dict"}),
        Bucket= USERS_BUCKET_NAME,
        Key="user-1/some-file"
    )

    s3_client_with_bucket.put_object(
        Body=json.loads({"type": "dict"}),
        Bucket= USERS_BUCKET_NAME,
        Key="user-2/some-file"
    )

    yield s3_client_with_bucket


