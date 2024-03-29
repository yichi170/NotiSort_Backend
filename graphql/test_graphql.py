import pytest

from main import schema
from firebase_db import db
from example import data, collections


@pytest.fixture(scope="module")
def test_data():
    for c in collections:
        len = 3
        if c == "activity_recognition":
            len = 7
        for i in range(1,len):
            db.collection(c).document(f'test{i}').set(data[f'{c}_{i}'])

    yield

    for c in collections:
        len = 3
        if c == "activity_recognition":
            len = 7    
        for i in range(1,len):
            db.collection(c).document(f'test{i}').delete()


def test_esm_query(test_data):
    query = """
        query TestQuery($user_id: String) {
            esm(user_id: $user_id) {
                user_id
                survey_finish_time
                mode
                esm_context_q1
                esm_context_q2
                esm_context_q3
                esm_context_q4
                esm_context_q5
                pin_esm_notification_appname
                pin_esm_notification_title
                pin_esm_notification_content
                pin_esm_notification_posttime
                esm_category_name
                esm_pin_q1
                esm_pin_q2
                esm_pin_q3
                esm_pin_q4
                esm_pin_q5
                esm_pin_q6
                drag_esm_notification_content
                drag_esm_notification_appname
                drag_esm_notification_posttime
                drag_esm_notification_title
                esm_drag_q1
                esm_drag_q2
                esm_drag_q3
                esm_drag_q4
                esm_drag_q5
                esm_drag_q6
                esm_category_name
                esm_category_q1
                esm_auto_compare_original_noti_content
                esm_auto_compare_original_noti_appname
                esm_auto_compare_original_noti_posttime
                esm_auto_compare_original_noti_title
                esm_auto_compare_sort_noti_content
                esm_auto_compare_sort_noti_appname
                esm_auto_compare_sort_noti_posttime
                esm_auto_compare_sort_noti_title
                esm_auto_compare_q1
                esm_auto_compare_q2
                esm_auto_compare_q3
                esm_auto_compare_q4
            }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values={"user_id": "77"},
    )
    
    assert result.errors is None
    assert result.data["esm"] == [
        data['ESM_1']
    ]


def test_diary_query(test_data):
    query = """
        query TestQuery($user_id: String) {
            diary(user_id: $user_id) {
                user_id
                EsmQ1
                EsmQ2
                EsmQ3
                EsmQ4
                EsmQ5
                EsmQ6
            }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values={"user_id": "88"},
    )
    
    assert result.errors is None
    assert result.data["diary"] == [
        data['diary_2']
    ]


def test_activity_recognition_query(test_data):
    query = """
        query TestQuery($user_id: String) {
            activity(user_id: $user_id) {
                user_id
                time
                activity_type
            }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values={"user_id": "88"},
    )
    
    assert result.errors is None
    assert result.data["activity"] == [
        data['activity_recognition_4'],
        data['activity_recognition_5'],
        data['activity_recognition_6'],
    ]


def test_recent_use_query(test_data):
    query = """
        query TestQuery($user_id: String) {
            recent_use(user_id: $user_id) {
                user_id
                time
                action
                activity{
                    user_id
                    time
                    activity_type
                }
            }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values={"user_id": "77"},
    )
    
    assert result.errors is None
    assert result.data["recent_use"] == [
        {
            **data['recent_use_1'],
            "activity": data['activity_recognition_1'],
        }
    ]


def test_category_query(test_data):
    query = """
        query TestQuery($user_id: String) {
            category(user_id: $user_id) {
                user_id
                time
                action
                battery
                call_state
                category_name
                connectivity
                day_of_week
                is_charging
                is_device_idle
                is_power_save
                is_screen_on
                mode
                notification_mode
                time_of_day
                activity{
                    user_id
                    time
                    activity_type
                }
            }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values={"user_id": "77"},
    )
    
    assert result.errors is None
    assert result.data["category"] == [
        {
            **data['category_1'],
            "activity": data['activity_recognition_2'],
        }
    ]


def test_notification_query(test_data):
    query = """
        query TestQuery($user_id: String) {
            notification(user_id: $user_id) {              
                app_name
                app_title
                battery
                call_state
                connectivity
                content
                day_of_week
                is_charging
                is_device_idle
                is_power_save
                is_screen_on
                mode
                notification_id
                notification_mode
                post_time
                time_of_day
                user_id
                activity{
                    user_id
                    time
                    activity_type
                }
            }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values={"user_id": "77"},
    )
    
    assert result.errors is None
    assert result.data["notification"] == [
        {
            **data['notification_1'],
            "activity": data['activity_recognition_2'],
        }
    ]


def test_behavior_query(test_data):
    query = """
        query TestQuery($user_id: String, $mode: Int) {
            behavior(user_id: $user_id, mode: $mode) {              
                action
                battery
                call_state
                connectivity
                day_of_week
                is_charging
                is_device_idle
                is_power_save
                is_screen_on
                mode
                notification_id
                notification_belongs_category
                notification_mode
                time
                time_of_day
                user_id
                activity{
                    user_id
                    time
                    activity_type
                }
                notification_info{
                    app_name
                    app_title
                    battery
                    call_state
                    connectivity
                    content
                    day_of_week
                    is_charging
                    is_device_idle
                    is_power_save
                    is_screen_on
                    mode
                    notification_id
                    notification_mode
                    post_time
                    time_of_day
                    user_id
                    activity{
                        user_id
                        time
                        activity_type
                    }
                }
            }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values={"user_id": "77", "mode": 0},
    )
    
    assert result.errors is None
    assert result.data["behavior"] == [
        {
            **data['behavior_1'],
            "activity": data['activity_recognition_2'],
            "notification_info": [
                {
                    **data['notification_1'],
                    "activity": data['activity_recognition_2'],
                },
            ]
        }
    ]
