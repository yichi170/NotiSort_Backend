import pytest

from main import schema
from firebase_db import db


@pytest.fixture(scope="module")
def test_data():
    print("create data")    
    yield
    print("delete data")


def test_esm_query(test_data):
    query = """
        query TestQuery($user_id: String) {
            esm(user_id: $user_id) {
                user_id
            }
        }
    """

    result = schema.execute_sync(
        query,
        variable_values={"user_id": "88"},
    )
    
    assert result.errors is None
    assert result.data["esm"] == [
        {
            "user_id": "88"
        }
    ]
