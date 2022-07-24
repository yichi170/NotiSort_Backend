from fastapi import FastAPI
import uvicorn
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from typing import List, Optional

from firebase_db import db
from schema import Diary, Category, Notification, Behavior
from example import notification_list, behavior_list

@strawberry.type
class Query:
    @strawberry.field
    def diary(self) -> List[Diary]:
        users_ref = db.collection(u'diary')
        docs = users_ref.stream()
        res = [Diary(**doc.to_dict()) for doc in docs]
        return res

    @strawberry.field
    def category(self) -> List[Category]:
        users_ref = db.collection(u'category')
        docs = users_ref.stream()
        res = [Category(**doc.to_dict()) for doc in docs]
        return res

    @strawberry.field
    def behavior(self, user_id: Optional[str] = None) -> List[Behavior]:
        # users_ref = db.collection(u'behavior')
        # docs = users_ref.stream()
        # res = [Behavior(**doc.to_dict()) for doc in docs]

        if user_id is None:
            res = [Behavior(**doc) for doc in behavior_list]
        else:
            res = [Behavior(**doc) for doc in behavior_list if doc["user_id"]==user_id]

        return res

    @strawberry.field
    def notification(self, user_id: Optional[str] = None) -> List[Notification]:
        # users_ref = db.collection(u'notification')
        # docs = users_ref.stream()
        # res = [Notification(**doc.to_dict()) for doc in docs]

        if user_id is None:
            res = [Notification(**doc) for doc in notification_list]
        else:
            res = [Notification(**doc) for doc in notification_list if doc["user_id"]==user_id]

        return res
        
        
schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False))
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=7777)
