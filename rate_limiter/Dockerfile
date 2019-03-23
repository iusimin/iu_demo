FROM nginx:1.15.9

WORKDIR /iu/rate_limiter

RUN apt-get update
RUN apt-get install -y vim
RUN mkdir -p /etc/rate_limiter/static
RUN touch /etc/rate_limiter/static/index.html
COPY ./queue_rate.conf /etc/rate_limiter/queue_rate.conf
COPY ./zones.conf /etc/rate_limiter/zones.conf