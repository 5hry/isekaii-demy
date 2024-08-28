FROM python:3.8

RUN mkdir /code
WORKDIR /code
# CAT requirements.txt
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/