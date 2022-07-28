import pytest

from main import schema
from firebase_db import db
from example import behavior_list, notification_list, activity_list, recent_use_list, ESM_list, diary_list, category_list


@pytest.fixture(scope="module")
def test_data():
    db.collection(u'behavior_test').document(u'test1').set(behavior_list[0])
    db.collection(u'behavior_test').document(u'test2').set(behavior_list[1])
    db.collection(u'notification_test').document(u'test1').set(notification_list[0])
    db.collection(u'notification_test').document(u'test2').set(notification_list[1])
    db.collection(u'activity_test').document(u'test1').set(activity_list[0])
    db.collection(u'activity_test').document(u'test2').set(activity_list[1])
    db.collection(u'activity_test').document(u'test3').set(activity_list[2])
    db.collection(u'activity_test').document(u'test4').set(activity_list[3])
    db.collection(u'recent_use_test').document(u'test1').set(recent_use_list[0])
    db.collection(u'recent_use_test').document(u'test2').set(recent_use_list[1])
    db.collection(u'ESM_test').document(u'test1').set(ESM_list[0])
    db.collection(u'ESM_test').document(u'test2').set(ESM_list[1])
    db.collection(u'diary_test').document(u'test1').set(diary_list[0])
    db.collection(u'diary_test').document(u'test2').set(diary_list[1])
    db.collection(u'category_test').document(u'test1').set(category_list[0])
    db.collection(u'category_test').document(u'test2').set(category_list[1])
    yield
    db.collection(u'behavior_test').document(u'test1').delete()
    db.collection(u'behavior_test').document(u'test2').delete()
    db.collection(u'notification_test').document(u'test1').delete()
    db.collection(u'notification_test').document(u'test2').delete()
    db.collection(u'activity_test').document(u'test1').delete()
    db.collection(u'activity_test').document(u'test2').delete()
    db.collection(u'activity_test').document(u'test3').delete()
    db.collection(u'activity_test').document(u'test4').delete()
    db.collection(u'recent_use_test').document(u'test1').delete()
    db.collection(u'recent_use_test').document(u'test2').delete()
    db.collection(u'ESM_test').document(u'test1').delete()
    db.collection(u'ESM_test').document(u'test2').delete()
    db.collection(u'diary_test').document(u'test1').delete()
    db.collection(u'diary_test').document(u'test2').delete()
    db.collection(u'category_test').document(u'test1').delete()
    db.collection(u'category_test').document(u'test2').delete()


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
