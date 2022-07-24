import strawberry
from typing import List, Any

from example import notification_list, behavior_list


@strawberry.type
class Activity:
    user_id: str
    time: float
    activity_type: int

def get_activity(root: Any) -> Activity:
    return Activity(user_id=root.user_id, time=11111, activity_type=3)


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

    activity: Activity = strawberry.field(resolver=get_activity)

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

    activity: Activity = strawberry.field(resolver=get_activity)

    @strawberry.field
    def notification_info(self) -> List[Notification]:
        noti_list = [Notification(**doc) for doc in notification_list]
        return filter(lambda noti: noti.user_id==self.user_id and noti.notification_id==self.notification_id, noti_list)

    
