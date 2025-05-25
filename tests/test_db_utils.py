import pytest
from src.utils.db_utils import get_table_columns, run_query


# @pytest.mark.skip
class TestGetTableColumns:

    def test_gets_table_columns(self, table_columns):
        cols = table_columns

        result = get_table_columns(cols)

        assert result == ["id", "name"]

    def test_ignores_non_list_instances_and_returns_empty_list(self):
        test_one = {"a": 1}
        test_two = "hey"

        assert get_table_columns(test_one) == []
        assert get_table_columns(test_two) == []


# @pytest.mark.skip
class TestRunQuery:

    def test_returns_proper_response_with_json_key_provided(self):

        query = """
                    SELECT * FROM users
                    WHERE user_id = 1;
                """

        result = run_query(query=query, json_key="user")

        assert result == {
            "user": [{"user_id": 1, "first_name": "User", "last_name": "one"}]
        }

    def test_returns_proper_response_without_json_key_provided(self):

        query = """
                    SELECT * FROM users
                    WHERE user_id = 1;
                """

        result = run_query(query=query)

        assert result == [{"user_id": 1, "first_name": "User", "last_name": "one"}]

    def test_returns_error_for_non_valid_queries(self):

        query = "SELECT wrong_column FROM users WHERE user_id = 10;"

        result = run_query(query=query, json_key="all")
        print(result)

        assert result["message"] == "Error occured during database operation"