# 靶机描述

	这台靶机开放较多端口，其中两个ftp服务端口，一个smb服务端口。ftp 支持匿名登录，存在很多日志文件，但匿名账户不能下载。smb登录上后可以下载这些文件，其中ssh_config显示禁用ssh密码登录，允许密钥登录，认证密钥为.ssh/authorized.keys 及 在secure 用户及组操作日志文件中，发现了对smbuser用户进行密码修改的记录，密码为chauthtok。但尝试登录均失败。后续在80Web渗透中，rebots.txt文件中隐藏着密码 rootroot1 ,尝试ftp登录成功，并具有上传权限。想到可通过制作上传ssh私钥文件，通过密钥认证完成登录。成功拿到系统立足点。但权限极低，内核版本较低，使用linpeas枚举后，发现可以利用 dirtycow 漏洞提权。

#  渗透过程

## 初始侦察

**主机发现** ： 确定目标靶机为 `192.168.240.143`

**TCP 端口扫描**

![[Pasted image 20250723195702.png]]

**详细信息扫描**

`21，2121` 端口开放 `ftp` 服务，允许匿名登录
`445` 端口运行 `samba` 服务
`80` 端口运行 `http` 服务

![[Pasted image 20250723200225.png]]![[Pasted image 20250723200255.png]]
![[Pasted image 20250723200311.png]]

**常见漏洞扫描**

未发现可利用信息
![[Pasted image 20250723200937.png]]

## 21、2121 FTP服务

两个端口内容一样，大部分文件无法下载
![[Pasted image 20250723201453.png]]

### SMB服务探测

内容同 ftp 一致，尝试将文件下载到本地
![[Pasted image 20250723201724.png]]

下载成功
	`lcd /home/kali/MyFileServer`  切换本地保存目录
	`recure` 递归打开子目录
	`prompt` 关闭交换
![[Pasted image 20250723211132.png]]

**查看文件**

cron 文件中写了一些定时任务日志

-----

`Secure` 文件 记录了一些用户及组操作记录
其中更改了 **smbuser** 用户密码，更改为 **chauthtok**
![[Pasted image 20250723211748.png]]
![[Pasted image 20250723211823.png]]

->尝试 ssh、smb、ftp登录，均失败
![[Pasted image 20250723212257.png]]

----
**`ssh_config`**** 文件

禁用密码登录
![[Pasted image 20250723213131.png]]

默认启用密钥登录，认证密钥文件保存在 `.ssh/authorized_keys`
![[Pasted image 20250723213334.png]]

要想 ssh 登录 `smbuser` 用户,必须使用密钥登录


## 80 端口 WEB 渗透

**目录扫描**

![[Pasted image 20250723202325.png]]

存在 `readme.txt` 文件,提示密码是 **rootroot1**
![[Pasted image 20250723202204.png]]

### smbuser 用户 制作 ssh密钥 登录

使用密码 `rootroot1` ftp 登录成功，对当前文件夹具有rwx权限

![[Pasted image 20250723214042.png]]

制作密钥

![[Pasted image 20250723214506.png]]

创建存储认证密钥的文件夹

![[Pasted image 20250723215546.png]]

**ssh 私钥登录成功，拿到初始立足点**
![[Pasted image 20250723220112.png]]

## 提权

当前/home目录下，只有一个 smbuser 用户

进行常见提权枚举

**Sudo -l 特权枚举**

不存在特殊权限

![[Pasted image 20250724150810.png]]

**定时任务枚举**

不存在定时任务

![[Pasted image 20250724150932.png]]

**SUID 提权枚举**

![[Pasted image 20250724151746.png]]

**内核枚举**

![[Pasted image 20250724152219.png]]

查找可利用漏洞

![[Pasted image 20250724152324.png]]

大多利用都利用不成功

## Linpeas 提权枚举

两个高可能性 Dirtycow 漏洞，40611，40839 利用存在问题，利用失败


![[Pasted image 20250724153244.png]]

40847 利用成功

![[Pasted image 20250724154703.png]]

root密码为 dirtyCowFun

su - 切换 root 用户，提权成功

![[Pasted image 20250724154936.png]]

# 总结

通过此靶机，学会使用 `linpeas` 工具做本地提权枚举。