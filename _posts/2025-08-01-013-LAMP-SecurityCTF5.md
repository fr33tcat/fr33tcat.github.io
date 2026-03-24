---
title: 013-LAMP SecurityCTF5
date: 2025-08-01 12:00:00 +0800
categories: [网安学习, 靶机实战]
tags: [学习笔记, Writeup]
---


# 靶机描述



# 渗透过程

## 初始侦察

**主机发现** `192.168.240.147` 为目标靶机

### 端口扫描

`22,25,80,110,111,139,143,445,901,3306,54755`

![Pasted image 20250731090135.png](/assets/img/attachments/Pasted%20image%2020250731090135.png)

### 详细信息扫描

![Pasted image 20250731150633.png](/assets/img/attachments/Pasted%20image%2020250731150633.png)![Pasted image 20250731151201.png](/assets/img/attachments/Pasted%20image%2020250731151201.png)


## 攻击面 初步信息收集

#### **25, 110, 143 邮件服务**

|端口|协议|作用|
|---|---|---|
|25|SMTP|发邮件 / 邮件服务器中继|
|110|POP3|收邮件（客户端拉邮件）|
|143|IMAP|收邮件（更高级，支持多端同步）|

#### **139, 445 Samba 服务**

未发现共享文件夹

![Pasted image 20250731153526.png](/assets/img/attachments/Pasted%20image%2020250731153526.png)
## 80 Web  渗透

主界面 /index.php

![Pasted image 20250731153836.png](/assets/img/attachments/Pasted%20image%2020250731153836.png)

Phake 环境管理 存在账户登录窗口

![Pasted image 20250731154446.png](/assets/img/attachments/Pasted%20image%2020250731154446.png)

发现 NanoCMS 框架及后台登录界面

![Pasted image 20250731154903.png](/assets/img/attachments/Pasted%20image%2020250731154903.png)

`http://192.168.240.147/~andy/data/nanoadmin.php?`

尝试该框架的默认账户密码 admin:demo 登录失败
![Pasted image 20250731154823.png](/assets/img/attachments/Pasted%20image%2020250731154823.png)

![Pasted image 20250731155130.png](/assets/img/attachments/Pasted%20image%2020250731155130.png)
### Nikto Web 信息探测

`sudo nikto -h 192.168.240.147`

Apaceh : 2.2.6
php: 5.2.4
存在 phpinfo() 环境配置泄露
存在 phpmyadmin Web登录界面

![Pasted image 20250731154249.png](/assets/img/attachments/Pasted%20image%2020250731154249.png)

### 目录扫描

![Pasted image 20250731155500.png](/assets/img/attachments/Pasted%20image%2020250731155500.png)

**phpinfo 信息泄露**

![Pasted image 20250731155653.png](/assets/img/attachments/Pasted%20image%2020250731155653.png)

**phpmyadmin**

![Pasted image 20250731160014.png](/assets/img/attachments/Pasted%20image%2020250731160014.png)



![Pasted image 20250731163807.png](/assets/img/attachments/Pasted%20image%2020250731163807.png)![Pasted image 20250731164012.png](/assets/img/attachments/Pasted%20image%2020250731164012.png)

**/data/pagesdata.txt 做路径拼接** 


发现一串 passwd 字符串，hash 识别为 md5
![Pasted image 20250801112731.png](/assets/img/attachments/Pasted%20image%2020250801112731.png)

破解密码为 `shannon`

![Pasted image 20250731165234.png](/assets/img/attachments/Pasted%20image%2020250731165234.png)

尝试登录 cms  管理界面 admin:shannon

登录成功，发现可以新建page，执行php代码

上传反弹 shell,成功回弹，拿到初始权限

![Pasted image 20250801090817.png](/assets/img/attachments/Pasted%20image%2020250801090817.png)

![Pasted image 20250801090744.png](/assets/img/attachments/Pasted%20image%2020250801090744.png)

![Pasted image 20250801090608.png](/assets/img/attachments/Pasted%20image%2020250801090608.png)


## 提权

没有定时任务，sudo 版本 较低，可能存在提权漏洞

Linux version 2.6.23.1-42.fc
Sudo version 1.6.9p4

![Pasted image 20250801094718.png](/assets/img/attachments/Pasted%20image%2020250801094718.png)


具有较多用户，查询下是否有敏感信息泄露

![Pasted image 20250801093556.png](/assets/img/attachments/Pasted%20image%2020250801093556.png)

`grep -R -i pass /home/* 2>/dev/null`

![Pasted image 20250801102718.png](/assets/img/attachments/Pasted%20image%2020250801102718.png)

![Pasted image 20250801113754.png](/assets/img/attachments/Pasted%20image%2020250801113754.png)

发现一个特殊字符串 `50$cent`

尝试切换  root 用户，成功提权
![Pasted image 20250801102345.png](/assets/img/attachments/Pasted%20image%2020250801102345.png)


# 总结

总体而言感觉这个靶机也不算复杂，但在web渗透和提权的过程还是需要一些经验。寻找cms密码的时候也是需要一些经验的，如果执迷于dirb目录爆破，虽然可以看到很多文件，但都不可利用，容易耗费大量的时间。同时由于这个靶机开放的端口比较多，暴露的攻击面也比较多，有可能让我们钻入兔子洞难以出来。最后提权的时候，搜索含有pass字符串的文件也是很有经验的操作，而这步操作正是基于/etc/passwd文件中的多用户bash的情况，很有可能有用户为了方便提权操作，会在自己的目录下存放有关提权的密码文件，我们正是利用了这一点。最后总结一下打靶过程：



```txt
第一步：主机发现和端口扫描：漏洞扫描发现了80端口存在很多漏洞，还是从web入手。

第二步：web渗透，发现NanoCMS及其后台登录界面，寻找登录密码，最后Google搜索到了NanoCMS的凭据泄露漏洞，成功登录后台。

第三步：CMS后台代码执行：登录NanoCMS后台，寻找代码执行的位置，添加反弹shell的payload，保存修改并点击对应页面触发代码执行，拿到了初始立足点。

第四步：提权。寻找敏感信息，最后发现用户patrick家目录中的文件包含root密码，提权成功。
```
