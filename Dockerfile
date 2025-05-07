FROM python:3.9-slim

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY . /action
WORKDIR /action

ENTRYPOINT ["python", "/action/src/main.py"] 
