---
title: "Ssh黑名单"
date: 2021-01-06T14:16:18+08:00
draft: false
tags:
- linux
categories:
---

## linux 服务器防止ssh暴力登录

最近折腾nas的时候意识到linux服务器安全性问题，这里主要是防止利用ssh暴力登录。ssh登录记录一般在`/var/log/auth.log`(debian系)或者`/var/log/secure`(centos系)中，可以通过这个文件查看ssh的登录记录，包括登录失败，拒绝登录，登录成功等信息。

参看登录失败IP

```shell
cat /var/log/auth.log | awk '/Failed/{print $(NF-3)}' | sort | uniq -c | awk '{print $2" = "$1;}'
```

参看登录成功IP

```shell
cat /var/log/auth.log | awk '/Accepted/{print $(NF-3)}' | sort | uniq -c | awk '{print $2" = "$1;}'
```

参考拒绝登录IP

 ```shell
cat /var/log/auth.log | awk '/refused/{print $(NF -1)}' | sort |uniq -c | awk '{print $2" = "$1}'
 ```

### 加入黑名单

将3次登录失败的IP加入`/etc/hostd.deny`黑名单，禁止其通过sshd登录。这里没10分钟检查一次log文件。脚本文件`/scripts/host_block.sh`如下：

```shell
#!/bin/bash
# -*- coding: UTF-8 -*-
# Filename: host_block.sh
# Description: 将SSH多次登录失败的IP加入黑名单
# Date: 2021-01-06

block_ip(){
        cat /var/log/auth.log | awk '/Failed/{print $(NF-3)}' | sort | uniq -c | awk '{print $2"="$1}' > /tmp/black
        list=`cat /tmp/black`

        for i in $list; do
                ip=`echo $i | awk -F= '{print $1}'`
                num=`echo $i | awk -F= '{print $2}'`
                if [[ $num -gt 3 ]]; then
                        grep $ip /etc/hosts.deny &> /dev/null
                        if [[ $? -gt 0 ]]; then
                                echo "sshd:$ip" >> /etc/hosts.deny
                        fi
                fi
        done

        cp /dev/null /tmp/black
}
# 10分钟一次
while(true)
do
        block_ip
        sleep 600
done
```



### 开机启动

通过systemd服务开机启动脚本，在`/etc/systemd/system`中创建一个服务`host_block.service`

```shell
[Unit]
Description=prevent unknow ip to log in by ssh

[Service]
Type=oneshot
ExecStart=/bin/bash /scripts/host_block.sh

[Install]
WantedBy=multi-user.target
```



最后执行

```shell
# 开机启动脚本
systemctl enable host_block.service
# 不重新启动，开机本次服务
nohup systemctl start host_block.service > /dev/null 2 > &1 &
```

### 修改端口（opt）

ssh的默认端口是22，所以攻击者一般攻击22端口，我们可以修改一下ssh的端口，可以降低被暴力破解的风险。修改文件`/etc/ssh/sshd_config`文件中的`port`参数，并重启ssh服务。需要注意的是我们一般先取消`#port 22`注释，再添一行`port xxxx`，然后尝试用新的端口登录，如果新端口能登录成功再注释掉`port 22`。

```shell
# port 22
```

反注释并添加新端口

```shell
port 22
port 1234
```

尝试新端口登录，登录成功后，注释掉22端口

```shell
# port 22
port 1234
```




