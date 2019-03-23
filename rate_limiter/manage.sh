#!/bin/bash
cp /etc/rate_limiter/queue_rate.conf /etc/rate_limiter/queue_rate.conf.bak
vim /etc/rate_limiter/queue_rate.conf
echo $?