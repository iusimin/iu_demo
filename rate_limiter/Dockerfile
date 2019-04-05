FROM ubuntu:18.04

WORKDIR /iu/rate_limiter

RUN apt-get update
RUN apt install -y nginx
RUN apt-get install -y vim
RUN apt-get install -y python3.6
RUN apt install -y python3-pip
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN ln -s /usr/bin/python3.6 /usr/bin/python
RUN mkdir -p /etc/rate_limiter/static
RUN touch /etc/rate_limiter/static/index.html
RUN touch /etc/rate_limiter/zones.conf
RUN touch /etc/rate_limiter/queue_rate.conf

COPY ./requirements.txt ./
COPY ./.vimrc /root
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt