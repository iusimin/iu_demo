# 1. ssh ecs instance
1.1 chmod 400 iu_key.pem

1.2 ssh -i iu_key.pem root@47.103.49.204

# 2. create your own user
2.1 adduser iuqian

2.2 usermod -aG sudo iuqian

2.3 su - iuqian