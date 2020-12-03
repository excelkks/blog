---
title: "修复latex公式矩阵换行在hugo下的渲染问题"
date: 2020-12-03T14:13:46+08:00
draft: false
tags:
- markdown
categories:
- 写作
---

目前我已经从hexo迁移到hugo写博客，我个人非常喜欢hugo的轻快，但是还有一个非常困扰我的问题就是latex矩阵的渲染。我在hugo使用的渲染公式的方案是用mathjax，由于hugo解析backslash`\`先用mathjax，这就会导致公式中的double backslash`\\`（在latex中表现为换行）会被解析为single backslash，从而导致mathjax解析换行失败，最后造成无法渲染矩阵。

在网上搜了一圈后，普遍给出的方案都是把 double backslash 换为quadruple backslash`\\\\`，这样确实可以解决问题，但是问题也很明显，就是无法与其他的 Markdown 编辑器兼容，特别是我平时喜欢用 Tyopra 编辑markdown文件。

我的最终方案是在hugo博客的根目录下建立一个data路径用于存放原始的markdown文件，平时的编辑，更改都在data/post路径下的mardown文件进行，写好后再用脚本将data/post文章的公式中的double backslash改为quadraple backslash后放入content/post中。这样平时只需要在data/post中编辑，编辑完后在用脚本renew一下就可以了。这应该是我能想到的最不折腾的方案了。

我的写作流程基本上可以归结为如下：
1. `blog -n "post title"` 基于hugo的`hugo new post/post_title` 创建post并放到data/post路径下
2. 在data/post路径下写作
3. `blog -r` 更新所有post，即处理`\\`
4. `blog -d "comment"` 提交到仓库，更新博客网站


