import argparse
import requests
import pytest
import json
import re

def test(ip):
    res = requests.get(f"http://{ip}:7000/hello")
    assert res.status_code == 200
    assert "Hello world\n" == res.text
