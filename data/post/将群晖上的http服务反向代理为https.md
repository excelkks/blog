---
title: "将群晖上的http服务反向代理为https"
date: 2021-10-08T09:05:51+08:00
draft: false
tags:
categories:
---

> 在文章[给群晖添加ssl证书](给群晖添加ssl证书.md)中已经讲诉了如何添加ssl证书, 这对群晖默认端口的服务是直接生效的, 但是对其他如docker等的服务是无效的, 对此, 只需要利用群晖自带的反向代理就可以完成ssl加密. 需要完成反向代理和路由器端口映射. 本文以设置jellyfin反向代理为例.  ## 前提

假设已经架设好jellyfin服务了, 我使用的是docker中[jellyfin](https://hub.docker.com/r/linuxserver/jellyfin)服务, 也可以是其他方式, 主要目的是架设好jellyfin服务. 假设架设好的jellyfin服务后的端口号为8096, 此时已经可以通过8096端口访问jellyfin的http服务了, 以上为前提条件.

## 反向代理

打开群晖的`控制面板->应用程序门户->反向代理服务规则`, 像下图一样填写, 表示将来自于https的18096端口的服务代理到http的8096端口, 完成后, 即可通过https的18096访问jellyfin了, 但是此时还未添加证书.

![反向代理](/images/ssl/revert.png)



## 为反向代理添加证书

打开群晖的`控制面板->安全性->证书->配置`, 如下图, 给10896端口的服务选择你的证书.

![设置证书](/images/ssl/certsettings.png)

此时, 已经通过ssl加密了. 下一步需要在路由器上设置防火墙.



## 防火墙设置

在防火墙中放行18096端口即可.
