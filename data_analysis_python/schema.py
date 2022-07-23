import strawberry

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
    notification_id: int
    notification_belongs_category: str
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
    time: float
    time_of_day: int
    user_id: str
