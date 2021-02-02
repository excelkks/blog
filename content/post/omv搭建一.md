---
title: "omv搭建一"
date: 2021-01-06T14:21:43+08:00
draft: false
tags:
categories:
---

# omv配置网络

在面板上设置了静态网络发现无法上网，因此这里直接编辑netplan的配置文件实现静态ipv4.

编辑文件`/etc/netplan/10-openmediavault-eno1.yaml`

```shell
network:
  ethernets:
    eno1:
      match:
        macaddress: xx:xx:xx:xx:xx:xx
      dhcp4: false
      dhcp6: false
      addresses: [192.168.2.222/24]
      gateway4: 192.168.2.1
      nameservers:
        addresses: [114.114.114.114, 8.8.8.8]
      link-local: []
```

最后执行

```shell
netplan apply
```

上面编辑的配置文件中相当于没有启用ipv6，如果要启用ipv6，可以把 `dhcp6: false` 改为`dhcp6: true` .

### docker安装

```shel
wget -O - https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/install | bash
```









## ipv6 ddns

首先要有一个域名，可以使用常见的[阿里云域名](wanwang.aliyun.com)、[cloudflare ](www.cloudflare.com)或者是[godaddy](www.godaddy.com)。由于我之前已经有了一个godaddy的域名，我这里直接用godaddy。关于阿里云域名的教程在网上很多，可以更容易解决。

关于申请域名部分比较简单，这里不赘述。

### 增加AAAA记录

打开管理域名页面.

![product](/images/nas/product.png)

![manage](/images/nas/manage.png)

![add](/images/nas/add.png)

![AAAA](/images/nas/AAAA.png)

### 创建API Key

进入[管理API](https://developer.godaddy.com/keys#)页面，创建api key

![create_api](/images/nas/create_api.png)

![ote](/images/nas/ote.png)



Next后得到 Key和Secret.

![created](/images/nas/created.png)

### 创建脚本

将上面的到的Key和Secret填入下方

```shell
#!/bin/bash

#这里是你购买的域名
mydomain="domain.xyz"
#这里是dns配置中的名称
myhostname="router"
#这里key和Secret之间注意有个冒号
gdapikey="你的key:你的Secret"
logdest="local7.info"
#另外注意，我这里的ipv6地址，所以使用的是AAAA类型解析，如果是ipv4那么下面所有的AAAA需改为A

setNewIp(){
    #这里的地址也是为ipv6服务，ipv4地址为https://api.ipify.org
    myip=`curl -s "https://api6.ipify.org"`
    dnsdata=`curl -s -X GET -H "Authorization: sso-key ${gdapikey}" "https://api.godaddy.com/v1/domains/${mydomain}/records/AAAA/${myhostname}"`#这里最后的2-9是针对性取得ipv6的字符, dnsdata中的返回字符串是一个json格式，需对齐解析。
    gdip=`echo $dnsdata | cut -d ',' -f 1 | tr -d '"' | cut -d ":" -f 2-9`
    echo "`date '+%Y-%m-%d %H:%M:%S'` - Current External IP is $myip, GoDaddy DNS IP is $gdip"

    if [ "$gdip" != "$myip" -a "$myip" != "" ]; then
        echo "IP has changed!! Updating on GoDaddy"
        curl -s -X PUT "https://api.godaddy.com/v1/domains/${mydomain}/records/AAAA/${myhostname}" -H "Authorization: sso-key ${gdapikey}" -H "Content-Type: application/json" -d "[{\"data\": \"${myip}\"}]"
        logger -p $logdest "Changed IP on ${hostname}.${mydomain} from ${gdip} to ${myip}"
    fi
}
while(true):
do
    setNewIp
    # 每15分钟更新一下IP
    sleep 900
done
```

### 开机执行脚本

将上面的脚本命名为`ddnsipv6.sh`放如路径`/etc/scripts`中，利用systemd开机启动脚本，在`/etc/systemd/system`中创建服务`renewip.service`

```shell
[Unit]
Description=renew ipv6 (ddns)
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/bash /etc/scripts

[Install]
WantedBy=multi-user.target
```
