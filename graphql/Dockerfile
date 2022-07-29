FROM python:3.8-slim-buster

WORKDIR /graphql

COPY . .

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python3", "/graphql/main.py"]