from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List

from firebase_db import db
from schema import Diary, Category, Notification, Behavior


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
    def behavior(self) -> List[Behavior]:
        users_ref = db.collection(u'behavior')
        docs = users_ref.stream()
        res = [Behavior(**doc.to_dict()) for doc in docs]
        return res[:100]

    @strawberry.field
    def notification(self) -> List[Notification]:
        users_ref = db.collection(u'notification')
        docs = users_ref.stream()
        res = [Notification(**doc.to_dict()) for doc in docs]
        return res[:100]
        
        
schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
