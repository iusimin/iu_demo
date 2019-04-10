FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3.6
RUN apt install -y python3-pip
RUN apt-get install -y git
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN ln -s /usr/bin/python3.6 /usr/bin/python

WORKDIR /iu/wms_backend

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt