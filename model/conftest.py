import argparse
import requests
import pytest
import json
import re

def ip_type(arg_value):
    regex = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    pattern = re.compile(regex)
    if not pattern.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value

def pytest_addoption(parser):
    parser.addoption('--ip', help='specify IP address of the host', type=ip_type)

def pytest_generate_tests(metafunc):
    option_val = metafunc.config.option.ip
    if 'ip' in metafunc.fixturenames and option_val is not None:
        metafunc.parametrize('ip', [option_val])

