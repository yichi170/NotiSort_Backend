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
        if user_id is None:
            users_ref = db.collection(u'activity_recognition')
        else:
            users_ref = db.collection(u'activity_recognition').where(u'user_id', u'==', user_id)

        docs = users_ref.stream()
        res = [Activity(**doc.to_dict()) for doc in docs]
        return res


    @strawberry.field
    def recent_use(self, user_id: Optional[str] = None) -> List[RECENT_USE]:
        if user_id is None:
            users_ref = db.collection(u'recent_use')
        else:
            users_ref = db.collection(u'recent_use').where(u'user_id', u'==', user_id)

        docs = users_ref.stream()
        res = [RECENT_USE(**doc.to_dict()) for doc in docs]
        return res


    @strawberry.field
    def esm(self, user_id: Optional[str] = None) -> List[ESM]:
        if user_id is None:
            users_ref = db.collection(u'ESM')
        else:
            users_ref = db.collection(u'ESM').where(u'user_id', u'==', user_id)

        docs = users_ref.stream()
        res = [ESM(**doc.to_dict()) for doc in docs]
        return res


    @strawberry.field
    def diary(self, user_id: Optional[str] = None) -> List[Diary]:
        if user_id is None:
            users_ref = db.collection(u'diary')
        else:
            users_ref = db.collection(u'diary').where(u'user_id', u'==', user_id)

        docs = users_ref.stream()
        res = [Diary(**doc.to_dict()) for doc in docs]
        return res


    @strawberry.field
    def category(self, user_id: Optional[str] = None) -> List[Category]:
        if user_id is None:
            users_ref = db.collection(u'category')
        else:
            users_ref = db.collection(u'category').where(u'user_id', u'==', user_id)

        docs = users_ref.stream()
        res = [Category(**doc.to_dict()) for doc in docs]
        return res


    @strawberry.field
    def notification(self, user_id: Optional[str] = None) -> List[Notification]:
        if user_id is None:
            users_ref = db.collection(u'notification')
        else:
            users_ref = db.collection(u'notification').where(u'user_id', u'==', user_id)

        docs = users_ref.stream()
        res = [Notification(**doc.to_dict()) for doc in docs]
        return res


    @strawberry.field
    def behavior(self, user_id: Optional[str] = None, mode: Optional[int] = None) -> List[Behavior]:
        if user_id is None and mode is None:
            users_ref = db.collection(u'behavior')
        elif user_id is None and mode is not None:
            users_ref = db.collection(u'behavior').where(u'mode', u'==', mode)
        elif user_id is not None and mode is None:
            users_ref = db.collection(u'behavior').where(u'user_id', u'==', user_id)
        else:
            users_ref = db.collection(u'behavior').where(u'user_id', u'==', user_id).where(u'mode', u'==', mode)

        docs = users_ref.stream()
        res = [Behavior(**doc.to_dict()) for doc in docs]
        return res

        
schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False))
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
