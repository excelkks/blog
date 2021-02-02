---
title: "systemd开机启动服务"
date: 2021-01-06T14:18:40+08:00
draft: false
tags:
categories:
---

# systemd开机运行服务

```shell
[Unit]
Description=renew ipv6 (ddns)
After=network.target # needed service

[Service]
Type=oneshot  # start once
ExecStart=/bin/bash /etc/scripts  # what to execute

[Install]
WantedBy=multi-user.target  # startup execute
```

参考[How to write startup script for systemd](https://unix.stackexchange.com/questions/47695/how-to-write-startup-script-for-systemd)


