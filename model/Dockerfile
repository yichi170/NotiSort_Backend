FROM python:3.8-slim-buster

WORKDIR /model

COPY . .

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python3", "/model/server_fastapi.py"]