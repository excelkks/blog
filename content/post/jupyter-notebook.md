---
title: "Jupyter Notebook"
date: 2020-12-09T10:00:18+08:00
draft: false
tags: 
- python
categories: 
---


在本地使用服务器上的jupyter-notebook
1. 在服务器端开启
```shell
jupyter notebook --no-browser --port=9009
```

2. 在本地端
```shell
ssh -N -f -L localhost:9008:localhost:9009 user@server-ip
```
