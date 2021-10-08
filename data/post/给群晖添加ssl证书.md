---
title: "给群晖添加ssl证书"
date: 2021-10-05T08:14:44+08:00
draft: false
tags: https
categories:
---

> acme.sh已经把申请默认证书从Let's Encrypt改为了ZeroSSL了. 本文利用acme.sh给群晖申请ZeroSSL证书, 并自动续期, 步骤包括: 
>
> 1. 获取DNS的API用以后续验证域名属于你.
> 2. 申请zerossl帐户.
> 3. 利用acme.sh申请证书.
> 4. 安装证书
> 5. 自动续期证书.

## 获取DNS服务商的API

在申请证书的时候需要验证DNS属于是属于你的, 所以要先获取dns服务商的API以便在利用[acme.sh](https://github.com/acmesh-official/acme.sh)申请时自动验证. 我这里使用的是godaddy的域名服务商自带的dns, 所以这里以godaddy举例.

首先打开[godaddy的开发者网页](https://developer.godaddy.com/), 点击API Keys

![godaddy](/images/ssl/godaddy.png)

根据提示申请一个Production的API Key

![production](/images/ssl/production.png)

之后获得Key和Secret

![created](/images/ssl/created.png)

其他服务商获取方法大同小异.

## 申请ZeroSSL帐户

打开[ZeroSSL官网](https://zerossl.com), 根据提示申请帐户, 这里需要提供一个邮箱, 这个邮箱在acme.sh申请证书时需要用到. 这里多说一句, 利用ZeroSSL官网就已经可以通过图形界面来申请证书了, 并不一定需要acme.sh, 但是我们可以利用acme.sh来自动化续签, 所以还是采用acme.sh的方法来申请证书.

## acme.sh申请证书

首先下载acme.sh

```shell
# 下载并解压acme.sh
wget https://github.com/acmesh-official/acme.sh/archive/master.tar.gz
tar xvf master.tar.gz
cd acme.sh-master/
chmod a+x acme.sh
```

在acme.sh的目录下, 有一个dnsapi的目录, 里面存放的是修改各个DNS服务商的API的样本文件, 我这里使用的godaddy, 所以编辑dnsapi/dns_gd.sh, 修改GD_Key和GD_Secret为之前申请的值.

```shell
#!/usr/bin/env sh

#Godaddy domain api
#
#GD_Key="这里修改为申请到的GD_Key"
#
#GD_Secret="这里修改为申请到的GD_Secret"

GD_Api="https://api.godaddy.com/v1"
```

申请证书, `--email`参数为申请ZeroSSL时所用的邮箱, `--dns`为dns服务商

```shell
./acme.sh  --email example@email.com --issue   -d  example.com   --dns  dns_gd
```

如果没有问题的话, 证书已经位于`~/.acme.sh/example.com`路径下了.

## 安装证书

申请好证书后, 安装到群晖上. 首先登陆到群晖的web管理页面, 打开控制面板, 进入高级模式, 点击安全性点击证书, 到达以下界面

![cert](/images/ssl/cert.png)



点击`新增->导入新证书->导入证书`, 按步骤导入`~/.acme.sh/example.com`下的私钥和证书. 将导入的证书设为默认, 此时https已经是加密状态了.由于免费证书只有90天的有效期, 下一步, 自动更新证书.

## 证书更新

### 证书更新

```shell
./acme.sh --renew -d example.com
```

证书更新后依旧存放在`~/.acme.sh/example.com`下, 需要再次上传到群晖中. 但是可以通过脚本来实现.

### 自动上传

查看证书存放路径

```shell
# 查看证书
ls /usr/syno/etc/certificate/_archive
```

该路径下一般有多个子路径, 包括自带了synology证书和我们自己申请的证书, 确定好我们自己申请的证书目录, 假设为`dQPaUd`, 那么就可以将证书上传(这里上传表示更新)

```shell
./acme.sh --install-cert -d example.com \
    --certpath /usr/syno/etc/certificate/_archive/dQPaUd/cert.pem \
    --keypath /usr/syno/etc/certificate/_archive/dQPaUd/privkey.pem \
    --fullchainpath /usr/syno/etc/certificate/_archive/dQPaUd/fullchain.pem \
    --capath /usr/syno/etc/certificate/_archive/dQPaUd/chain.pem \
    --reloadcmd
```

同步默认的证书

```shell
rsync -avzh /usr/syno/etc/certificate/_archive/dQPaUd/ /usr/syno/etc/certificate/system/default
```

重启服务

```shell
/usr/syno/etc/rc.sysv/nginx.sh reload
```

此时, 证书更新完成.

## 自动更新证书

证书更新部分属于每90天更新一次, 可以通过自动执行脚本去实现, 而不是每90天自己去执行. 这设定每个月执行一次. 打开`控制面板->任务计划`

### 更新证书

首先新增一个更新证书脚本, 周期设置如下

![time](/images/ssl/time.png)

添加一个脚本

![script](/images/ssl/script.png)

由于我把acme.sh执行文件放在了`/volume1/docker/cert/acme.sh-master`下, 所以我的脚本为

```shell
# 不要忘了吧example.com换成你自己的域名
/volume1/docker/cert/acme.sh-master/acme.sh --renew -d example.com
```

### 自动上传

和上一步一样, 再增加一个计划事件, 但是事件运行时间改为`4:30`, 比更新证书晚30分钟, 脚本设置如下

```shell
/volume1/docker/cert/acme.sh-master/acme.sh \
    --install-cert -d example.com \
    --certpath /usr/syno/etc/certificate/_archive/dQPaUd/cert.pem \
    --keypath /usr/syno/etc/certificate/_archive/dQPaUd/privkey.pem \
    --fullchainpath /usr/syno/etc/certificate/_archive/dQPaUd/fullchain.pem \
    --capath /usr/syno/etc/certificate/_archive/dQPaUd/chain.pem \
    --reloadcmd

rsync -avzh /usr/syno/etc/certificate/_archive/dQPaUd/ /usr/syno/etc/certificate/system/default/

/usr/syno/etc/rc.sysv/nginx.sh reload
```



至此, 自动更新证书完成.
