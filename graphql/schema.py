import strawberry
from firebase_admin import firestore
from typing import List, Union

from firebase_db import db


@strawberry.type
class Activity:
    user_id: str
    time: float
    activity_type: int


@strawberry.type
class RECENT_USE:
    user_id: str
    time: float
    action: str

    @strawberry.field
    def activity(self) -> Union[Activity, None]:
        users_ref = db.collection(u'activity_recognition')
        users_ref = users_ref.where(u'time', u'<=', self.time).order_by(u'time', direction=firestore.Query.DESCENDING)
        docs = users_ref.stream()

        for doc in docs:
            doc = doc.to_dict()
            if doc["user_id"] == self.user_id:
                return Activity(**doc)


@strawberry.type
class ESM:
    user_id: str
    survey_finish_time: float
    mode: int
    esm_context_q1: str
    esm_context_q2: str
    esm_context_q3: str
    esm_context_q4: str
    esm_context_q5: str
    pin_esm_notification_appname: str
    pin_esm_notification_title: str
    pin_esm_notification_content: str
    pin_esm_notification_posttime: str
    esm_category_name: str
    esm_pin_q1: str
    esm_pin_q2: str
    esm_pin_q3: str
    esm_pin_q4: str
    esm_pin_q5: str
    esm_pin_q6: str
    drag_esm_notification_content: str
    drag_esm_notification_appname: str
    drag_esm_notification_posttime: str
    drag_esm_notification_title: str
    esm_drag_q1: str
    esm_drag_q2: str
    esm_drag_q3: str
    esm_drag_q4: str
    esm_drag_q5: str
    esm_drag_q6: str
    esm_category_name: str
    esm_category_q1: str
    esm_auto_compare_original_noti_content: List[str]
    esm_auto_compare_original_noti_appname: List[str]
    esm_auto_compare_original_noti_posttime: List[str]
    esm_auto_compare_original_noti_title: List[str]
    esm_auto_compare_sort_noti_content: List[str]
    esm_auto_compare_sort_noti_appname: List[str]
    esm_auto_compare_sort_noti_posttime: List[str]
    esm_auto_compare_sort_noti_title: List[str]
    esm_auto_compare_q1: str
    esm_auto_compare_q2: str
    esm_auto_compare_q3: str
    esm_auto_compare_q4: str


@strawberry.type
class Diary:
    user_id: str
    EsmQ1: str
    EsmQ2: str
    EsmQ3: str
    EsmQ4: str
    EsmQ5: str
    EsmQ6: str


@strawberry.type
class Category:
    action: str
    battery: int
    call_state: str
    category_name: str
    connectivity: str
    day_of_week: int
    is_charging: bool
    is_device_idle: bool
    is_power_save: bool
    is_screen_on: bool
    mode: int
    notification_mode: str
    time: float
    time_of_day: int
    user_id: str

    @strawberry.field
    def activity(self) -> Union[Activity, None]:
        users_ref = db.collection(u'activity_recognition')
        users_ref = users_ref.where(u'time', u'<=', self.time).order_by(u'time', direction=firestore.Query.DESCENDING)
        docs = users_ref.stream()

        for doc in docs:
            doc = doc.to_dict()
            if doc["user_id"] == self.user_id:
                return Activity(**doc)


@strawberry.type
class Notification:
    app_name: str
    app_title: str
    battery: int
    call_state: str
    connectivity: str
    content: str
    day_of_week: int
    is_charging: bool
    is_device_idle: bool
    is_power_save: bool
    is_screen_on: bool
    mode: int
    notification_id: float
    notification_mode: str
    post_time: float
    time_of_day: int
    user_id: str

    @strawberry.field
    def activity(self) -> Union[Activity, None]:
        users_ref = db.collection(u'activity_recognition')
        users_ref = users_ref.where(u'time', u'<=', self.post_time).order_by(u'time', direction=firestore.Query.DESCENDING)
        docs = users_ref.stream()

        for doc in docs:
            doc = doc.to_dict()
            if doc["user_id"] == self.user_id:
                return Activity(**doc)


@strawberry.type
class Behavior:
    action: str
    battery: int
    call_state: str
    connectivity: str
    day_of_week: int
    is_charging: bool
    is_device_idle: bool
    is_power_save: bool
    is_screen_on: bool
    mode: int
    notification_id: float
    notification_belongs_category: str
    notification_mode: str
    time: float
    time_of_day: int
    user_id: str

    @strawberry.field
    def activity(self) -> Union[Activity, None]:
        users_ref = db.collection(u'activity_recognition')
        users_ref = users_ref.where(u'time', u'<=', self.time).order_by(u'time', direction=firestore.Query.DESCENDING)
        docs = users_ref.stream()

        for doc in docs:
            doc = doc.to_dict()
            if doc["user_id"] == self.user_id:
                return Activity(**doc)

    @strawberry.field
    def notification_info(self) -> List[Notification]:
        users_ref = db.collection(u'notification')
        users_ref = users_ref.where(u'user_id', u'==', self.user_id).where(u'notification_id', u'==', self.notification_id)
        docs = users_ref.stream()
        res = [Notification(**doc.to_dict()) for doc in docs]
        return res
