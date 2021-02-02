---
title: "在linux中开启samba服务"
date: 2021-01-06T14:32:55+08:00
draft: false
tags:
categories:
---

## linux中samba的应用

### 服务器端

在linux中开启samba共享服务，首先安装samba服务

```shell
# ubuntu
apt install samba
```

配置文件的路径在`/etc/samba/smb.conf`，如果需要添加共享，需要添加如下内容

```shell
[share]
  comment = comments
  path = /path/to/share
  browseable = yes
  writeable = yes
  public = yes
  # create mask = 0775   # 创建文件的权限
  # directory mask = 0775  # 创建目录的权限
  # valid users = heijunma,root  #允许访问该共享的用户
  # write list = heijunma,root  #可写入共享的用户列表
```

重启smb服务

```shell
service smbd restart
service nmb restart
```



 ### 在linux中访问samba共享

首先需要安装`cifs`，再进行挂载，samba的默认端口为445和139

```shell
apt install cifs-utils
mount.cifs -o username=user,password=passwd,port=<port> //ip/share/path/ /mount/point
```


