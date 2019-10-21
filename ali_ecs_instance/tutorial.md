# 1. ssh ecs instance
1.1 chmod 400 iu_key.pem

1.2 ssh -i iu_key.pem root@168.62.6.74

# 2. create your own user
2.1 adduser iuqian

2.2 usermod -aG sudo iuqian

2.3 su - iuqian

2.4 mkdir ~/.ssh

2.5 cat "your_public_ssh_key" > ~/.ssh/authorized_keys

2.6 create ssh config:

    Host iu_demo
        HostName 168.62.6.74
        User iuqian
        IdentityFile ~/.ssh/id_rsa_iu
        
2.7 ssh iu_demo
