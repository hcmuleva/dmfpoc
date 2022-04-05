FROM python:3.8-slim-buster

COPY . .
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR .

CMD [ "python3", "mockserver.py"]
