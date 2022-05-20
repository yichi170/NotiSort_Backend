import requests
import pytest
import json
import re

input = {"data": [["app1", "title1", "content1", "category", 10000, 1],
                   ["app2", "title2", "content2", "category", 10000, 2],
                   ["app3", "title2", "content2", "category", 10000, 3]]}

def test_model(ip):
    res = requests.post(f"http://{ip}", data=json.dumps(input, ensure_ascii=False))
    assert res.status_code == 200
    assert re.search("^\"\\[[0-9, ]+\\]\"$", res.text) is not None
