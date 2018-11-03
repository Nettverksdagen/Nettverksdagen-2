FROM python:3
ENV PYTHONUNBUFFERED 1
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "netcat-traditional"]
RUN mkdir /nvdnew
WORKDIR /nvdnew
ADD requirements.txt /nvdnew/
RUN pip install -r requirements.txt
ADD . /nvdnew/
