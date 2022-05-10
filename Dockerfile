FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt upgrade -y && apt install -y --no-install-recommends --allow-unauthenticated \
    build-essential \
    vim \
    cmake \
    git \
    wget \
    curl \
    python-setuptools \
    python3 \

RUN apt-get install -y python3-pip

RUN pip3 install setuptools

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

COPY . /opt

WORKDIR /opt

RUN pip3 install -r requirements.txt

# set environment variables
RUN echo "PYTHONPATH=/opt/gira-app:" >> /etc/environment
RUN echo "SQLALCHEMY_DATABASE_URI=mysql://root:ErolTaskin@localhost:3306/gira:" >> /etc/environment
RUN echo "SQLALCHEMY_TRACK_MODIFICATIONS=false:" >> /etc/environment
RUN echo "DEBUG_FLAG=true:" >> /etc/environment
RUN echo "JWT_SECRET_KEY=W85~4PpF" >> /etc/environment


RUN /bin/bash -c "source /etc/environment"

# install supervisor to run flask app
RUN mkdir /var/log/supervisord/
RUN pip3 install supervisor
ADD gira_app.supervisord.conf /etc/supervisor/supervisord.conf
RUN /usr/bin/python3 /usr/local/bin/supervisord -c /etc/supervisor/supervisord.conf


CMD  bash
