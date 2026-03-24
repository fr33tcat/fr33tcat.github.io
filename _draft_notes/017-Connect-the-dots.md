
# 靶机描述

# 渗透过程

## 初始侦察

### 端口扫描

`192.168.240.151` 为目标靶机

**TCP端口扫描**

21,80,111,2049,7822,33895，56139，58087，58125
![[Pasted image 20250808112951.png]]

**常见UDP 端口扫描**

![[Pasted image 20250806005829.png]]

### 详细信息扫描

![[Pasted image 20250806010247.png]]

 ### 常见漏洞脚本扫描

![[Pasted image 20250806010518.png]]![[Pasted image 20250806010604.png]]
![[Pasted image 20250806010626.png]]![[Pasted image 20250806010642.png]]

### Web 目录爆破

![[Pasted image 20250806011927.png]]


![[Pasted image 20250806010931.png]]

`gobuster dir -u http://192.168.240.151/ -x html,txt,php,zip,sql --wordlist=/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`

![[Pasted image 20250806011102.png]]


### Nikto Web信息扫描

![[Pasted image 20250806011437.png]]

---------- 

hits.txt 提示继续信息收集，

![[Pasted image 20250806011827.png]]

/manual 目录是 apache 的一个服务页，

![[Pasted image 20250806011847.png]]

/backups 目录是一个小视频

![[Pasted image 20250808105832.png]]

均没有拿到有用信息

----------

**/mysite** 返回码 301 存在重定向 里面是一些 css,js,html 代码，其中`register.html`值得访问

![[Pasted image 20250808110041.png]]

查看时，bootstrap.min.cs 内容特殊，像是 jsfuck 内容混淆加密

![[Pasted image 20250808110201.png]]

在控制台，将10个变量拼接，拿去 jsfuck 在线解密

![[Pasted image 20250808110311.png]]

![[Pasted image 20250808110338.png]]

拿到一串提示字符，`TryToGuessThisNorris@2k19` 可能是密码，需要尝试下密码登录

/resigter  有一个登录界面，邮箱/密码 登录  
目前 没有 登录凭证
![[Pasted image 20250808110708.png]]

### SSH 密码登录

`TryToGuessThisNorris@2k19` 猜测用户名 norris ,root, amdin 等

尝试 ssh 登录，norris 登录成功

![[Pasted image 20250808113907.png]]



### FTP 下载文件

![[Pasted image 20250808142034.png]]

hits.txt.bak 文件 有一个url 跳转后，提示，让继续保持信息收集能力

![[Pasted image 20250808142142.png]]
![[Pasted image 20250808142238.png]]

game.jpg.bak 注释有隐藏信息，经过莫斯及URL编码解码后，得到

```txt
HEY NORRIS, YOU'VE MADE THIS FAR. FAR FAR FROM HEAVEN WANNA SEE HELL NOW? HAHA YOU SURELY MISSED ME, DIDN'T YOU? OH DAMN MY BATTERY IS ABOUT TO DIE AND I AM UNABLE TO FIND MY CHARGER SO QUICKLY LEAVING A HINT IN HERE BEFORE THIS SYSTEM SHUTS DOWN AUTOMATICALLY. I AM SAVING THE GATEWAY TO MY DUNGEON IN A 'SECRETFILE' WHICH IS PUBLICLY ACCESSIBLE.


嘿，Norris，你已经走到这了。远离天堂，想现在去看看地狱吗？哈哈，你肯定想念我了，不是吗？哦，糟糕，我的电池快没电了，找不到充电器了，所以在系统自动关闭之前，我赶紧在这里留下了一个提示。我把通往我的地牢的门户保存在一个名为“secretfile”的文件里，这个文件是公开可访问的。

```

公开可访问，这个 sercertfile 文件，我们曾在norris用户中看到过，现在通过web访问试试

![[Pasted image 20250808142613.png]]

提示快没电了，并没有什么发现有价值信息

重新登录，查看webroot目录下文件,存在 `.secretfile.swp` 文件
![[Pasted image 20250808142919.png]]

![[Pasted image 20250808143104.png]]

查找信息，.swp文件时 vim 遭遇中断产生的交换文件，这样看的话，它刚一直强调没电就解释的通了

尝试恢复

在 远程靶机上，没有vim,strings等工具，修复失败，因为在/var/www/html目录下，我们下载到本地
![[Pasted image 20250808144317.png]]

`vim -r .secertfilr.swp`

![[Pasted image 20250808143932.png]]

修复成功，拿到消失的字符串 `blehguessme090`，可能是另一个用户morris的登录凭证

尝试登录

ssh登录成功

![[Pasted image 20250808144807.png]]

![[Pasted image 20250808145851.png]]





























