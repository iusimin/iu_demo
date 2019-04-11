FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3.6
RUN apt install -y python3-pip
RUN apt-get install -y git
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get install -y nodejs
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN ln -sf /usr/bin/python3.6 /usr/bin/python

WORKDIR /iu/wms

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt