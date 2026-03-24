# 靶机描述


# 渗透过程

## 初始侦察

**主机发现** `192.168.240.149` 为目标靶机

### 端口扫描

110,143 都是邮件服务，那看来主要攻击点集中在 80 端口
![[Pasted image 20250804094638.png]]

| 特性     | **POP3**                | **IMAP**                         |
| ------ | ----------------------- | -------------------------------- |
| 协议全称   | Post Office Protocol v3 | Internet Message Access Protocol |
| 主要用途   | **下载** 邮件到本地并删除服务器副本    | **同步** 邮件，保留在服务器                 |
| 多设备支持  | 差，只有一个设备能保留完整副本         | 好，多个设备可实时同步                      |
| 默认端口   | 110（非加密），995（SSL/TLS）   | 143（非加密），993（SSL/TLS）            |
| 邮件存储位置 | 本地                      | 服务器                              |
| 操作体验   | 类似“领取信件”，领完就没了          | 类似“远程访问邮箱”，随时同步                  |
| 文件夹支持  | 不支持                     | 支持文件夹（如收件箱、草稿、星标）                |

### 详细信息扫描

![[Pasted image 20250804095837.png]]


## 80 Web渗透


### 目录扫描

![[Pasted image 20250804104009.png]]

OpenSSH 7.2p2 Ubuntu 4ubuntu2.4 (Ubuntu Linux; protocol 2.0) 


![[Pasted image 20250804114800.png]]
![[Pasted image 20250804115342.png]]
![[Pasted image 20250804115500.png]]

![[Pasted image 20250804160558.png]]

![[Pasted image 20250804212132.png]]
![[Pasted image 20250804212909.png]]

![[Pasted image 20250804213102.png]]

![[Pasted image 20250804215808.png]]
![[Pasted image 20250804220845.png]]


`find / -writable -type f -not -path "/proc/*" -not -path "/sys/*" -not -path "/var/*" 2>/dev/null`

