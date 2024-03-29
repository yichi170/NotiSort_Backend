import re
from fastapi.testclient import TestClient
from server_fastapi import *

client = TestClient(app)

input = {"data": [["app1", "title1", "content1",
                   "category1", "STILL", "WEEKDAY",
                   "time_of_day", 10000, 1],
                  ["app2", "title2", "content2",
                   "category2", "STILL", "WEEKDAY",
                   "MIDNIGHT", 10000, 2],
                  ["app3", "title3", "content3",
                   "category3", "STILL", "WEEKDAY",
                   "MIDNIGHT", 10000, 3]]}

def test_model():
    res = client.post("/", json=input)
    assert res.status_code == 200
    assert re.search("^\"\\[[0-9, ]+\\]\"$", res.text) is not None
