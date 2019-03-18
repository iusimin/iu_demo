# Setup seperate git account
1. Clone iu project to your local directory
```
git clone git@github.com:intelligenceunion/iu.git
```
2. Modify `~/iu/.git/config`, adding user inforamtion to your IU git account, sample:
```
[user]
        name = iumao
        email = iumao@h1n1.onaliyun.com
```
3. Generate seperate ssh key
```
ssh-keygen -t rsa -b 4096 -C "yourname@h1n1.onaliyun.com"
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/arthur/.ssh/id_rsa): /Users/arthur/.ssh/id_rsa_iu
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
ServerAliveInterval 120
...
```
4. Add your new SSH to git
5. Set an alias in .ssh/config like below
```
# IU git
Host github-iu
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa_iu
```
6. Test and verify
```
$ ssh git@github-iu
PTY allocation request failed on channel 0
Hi iumao! You've successfully authenticated, but GitHub does not provide shell access.
Connection to github.com closed.
```

# Setup
1. Config environment variable IU_HOME to your project home path(Write in .bashrc)
```
$ echo $IU_HOME
/home/arthur/iu
```
2. Run command iu/ci/setup.sh, this step require root password and may take several minutes to download images and packages.

# Run demo
1. Ensure 80 port is released (Stop nginx / apache server if it's running on 80 port)
2. Run command `iu-cli run server`
3. Run command `iu-cli run infra` (Nginx may crash if your server is not running)
4. Then you can access http://demo.iu.com to check results
