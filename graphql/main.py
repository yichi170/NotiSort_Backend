from fastapi import FastAPI
import uvicorn
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from typing import List, Optional

from firebase_db import db
from schema import Activity, RECENT_USE, ESM, Diary, Category, Notification, Behavior


@strawberry.type
class Query:

    @strawberry.field
    def activity(self, user_id: Optional[str] = None) -> List[Activity]:
        users_ref = db.collection(u'activity_recognition')
        docs = users_ref.stream()

        if user_id is None:
            res = [Activity(**doc.to_dict()) for doc in docs]
        else:
            res = [Activity(**doc.to_dict()) for doc in docs if doc.to_dict()["user_id"]==user_id]

        return res


    @strawberry.field
    def recent_use(self, user_id: Optional[str] = None) -> List[RECENT_USE]:
        users_ref = db.collection(u'recent_use')
        docs = users_ref.stream()

        if user_id is None:
            res = [RECENT_USE(**doc.to_dict()) for doc in docs]
        else:
            res = [RECENT_USE(**doc.to_dict()) for doc in docs if doc.to_dict()["user_id"]==user_id]

        return res


    @strawberry.field
    def esm(self, user_id: Optional[str] = None) -> List[ESM]:
        users_ref = db.collection(u'ESM')
        docs = users_ref.stream()

        if user_id is None:
            res = [ESM(**doc.to_dict()) for doc in docs]
        else:
            res = [ESM(**doc.to_dict()) for doc in docs if doc.to_dict()["user_id"]==user_id]

        return res


    @strawberry.field
    def diary(self, user_id: Optional[str] = None) -> List[Diary]:
        users_ref = db.collection(u'diary')
        docs = users_ref.stream()

        if user_id is None:
            res = [Diary(**doc.to_dict()) for doc in docs]
        else:
            res = [Diary(**doc.to_dict()) for doc in docs if doc.to_dict()["user_id"]==user_id]

        return res


    @strawberry.field
    def category(self, user_id: Optional[str] = None) -> List[Category]:
        users_ref = db.collection(u'category')
        docs = users_ref.stream()

        if user_id is None:
            res = [Category(**doc.to_dict()) for doc in docs]
        else:
            res = [Category(**doc.to_dict()) for doc in docs if doc.to_dict()["user_id"]==user_id]

        return res


    @strawberry.field
    def notification(self, user_id: Optional[str] = None) -> List[Notification]:
        users_ref = db.collection(u'notification')
        docs = users_ref.stream()

        if user_id is None:
            res = [Notification(**doc.to_dict()) for doc in docs]
        else:
            res = [Notification(**doc.to_dict()) for doc in docs if doc.to_dict()["user_id"]==user_id]

        return res


    @strawberry.field
    def behavior(self, user_id: Optional[str] = None, mode: Optional[int] = None) -> List[Behavior]:
        users_ref = db.collection(u'behavior')
        docs = users_ref.stream()

        if user_id is None and mode is None:
            res = [Behavior(**doc.to_dict()) for doc in docs]
        elif user_id is None and mode is not None:
            res = [Behavior(**doc.to_dict()) for doc in docs if doc.to_dict()["mode"]==mode]
        elif user_id is not None and mode is None:
            res = [Behavior(**doc.to_dict()) for doc in docs if doc.to_dict()["user_id"]==user_id]
        else:
            res = [Behavior(**doc.to_dict()) for doc in docs if doc.to_dict()["user_id"]==user_id and doc.to_dict()["mode"]==mode]

        return res

        
schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False))
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=7777)
