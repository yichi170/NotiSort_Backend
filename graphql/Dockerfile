FROM python:3.8-slim-buster

WORKDIR /graphql

ADD . /graphql

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["strawberry", "server", "main"]
