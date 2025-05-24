import pytest
from pg8000.native import Connection
from src.utils.db_utils import get_table_columns, run_query


@pytest.mark.skip
class TestGetTableColumns:

    def test_gets_table_columns(self, table_columns):
        cols = table_columns

        result = get_table_columns(cols)

        assert result == ["id", "name"]

    def test_ignores_non_list_instances(self):
        test_one = {"a": 1}
        test_two = "hey"

        assert get_table_columns(test_one) is None
        assert get_table_columns(test_two) is None


@pytest.mark.skip
class TestRunQuery:

    def test_returns_proper_response_with_json_key_provided(
        self, db_conn: Connection
    ):

        query = """
                    SELECT * FROM users
                    WHERE user_id == 1;
                """

        result = run_query(query=query, json_key="user")

        assert result == {
            "user": [{"user_id": "1", "first_name": "User", "last_name": "one"}]
        }

    def test_returns_proper_response_without_json_key_provided(
        self, seed_database: Connection
    ):
        seed_database()

        query = """
                    SELECT * FROM users
                    WHERE user_id == 1;
                """

        result = run_query(query=query)

        assert result == [{"user_id": "1", "first_name": "User", "last_name": "one"}]

    def test_returns_error_for_non_valid_queries(self, seed_database):
        seed_database()

        query = "SELECT * FROM unknown_table;"

        result = run_query(query=query, json_key="all")

        assert "Error" in result.values()
