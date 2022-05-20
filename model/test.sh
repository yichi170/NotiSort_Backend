#!/bin/bash

BLUE='\033[1;34m'
NC='\033[0m'

printf "${BLUE}=================== simple test ===================${NC}\n"

python3 flaskapp.py > /tmp/null 2>&1 &
# pytest test_flaskapp.py --ip `curl https://ipinfo.io/ip`
pytest test_flaskapp.py --ip 0.0.0.0
ps -A | grep 'python3 flaskapp.py' | awk '{print $1}' | xargs kill -9 $1

printf "${BLUE}============== test api from internal ==============${NC}\n"

pytest test_api.py --ip 0.0.0.0
printf "${BLUE}============== test api from external ==============${NC}\n"
pytest test_api.py --ip `curl https://ipinfo.io/ip`
