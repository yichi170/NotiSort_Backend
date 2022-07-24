import strawberry
from firebase_admin import firestore
from typing import List, Union

from example import notification_list, behavior_list
from firebase_db import db


@strawberry.type
class Activity:
    user_id: str
    time: float
    activity_type: int

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
        users_ref = db.collection(u'activity_recognition_test')
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
        users_ref = db.collection(u'activity_recognition_test')
        users_ref = users_ref.where(u'time', u'<=', self.time).order_by(u'time', direction=firestore.Query.DESCENDING)
        docs = users_ref.stream()

        for doc in docs:
            doc = doc.to_dict()
            if doc["user_id"] == self.user_id:
                return Activity(**doc)

    @strawberry.field
    def notification_info(self) -> List[Notification]:
        users_ref = db.collection(u'notification_test')
        users_ref = users_ref.where(u'user_id', u'==', self.user_id).where(u'notification_id', u'==', self.notification_id)
        docs = users_ref.stream()
        res = [Notification(**doc.to_dict()) for doc in docs]
        return res
