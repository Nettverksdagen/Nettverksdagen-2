FROM python:3
ENV PYTHONUNBUFFERED 1
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "netcat-traditional"]
RUN mkdir api
WORKDIR /api
ADD requirements.txt /api/requirements.txt
RUN pip install -r requirements.txt
ADD . /api
