FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /rubbish_collection_day_v2_project
WORKDIR /rubbish_collection_day_v2_project

ADD . /rubbish_collection_day_v2_project

RUN pip install -r requirements.txt