---
title: skip、merge、AMVP模式
date: 2019-12-10 19:09:17
tags:
- 视频编码
- 帧间
categories:
- 视频编解码
---
在H.265中，帧间预测模式包括Skip模式、Merge模式、AMVP模式，其中，Skip模式是一种特殊的Merge模式。它们所需要编码的信息如下

||MVP|MVD|量化残差|
|:-:|:-:|:-:|:-:|
|Skip|✔|❌|❌|
|Merge|✔|❌|✔|
|AMVP|✔|✔|✔|

MVP的获取方法都是通过在编解码端建立候选列表，但要注意的是Skip模式和Merge模式建立MVP列表的方法**一样**，而AMVP建立候选列表的方式与Merge模式建立候选列表的方式**不一样**