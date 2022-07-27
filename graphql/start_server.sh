#!/usr/bin/env bash

if [[ "$(docker images -q graphql_server 2> /dev/null)" == "" ]]; then
  docker build -t graphql_server . --no-cache
fi

docker run --rm -p 8000:8000 graphql_server -d
