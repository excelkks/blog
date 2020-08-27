---
title: "转移到hugo"
date: 2020-08-26T17:06:33+08:00
draft: false
---

## 博客环境搭建

介于hexo框架太麻烦了，要安装nodejs，又要安装各种包，实在是难同步。由于电脑前段时间崩了，重新搭建hexo环境总是失败，实在浪费了很多时间，于是决定迁移到hugo。

在mac搭建hugo环境非常简单，只需要用homebrew即可安装
```shell
brew install hugo
```
这就算安装好hugo了，初始化新的hugo站点则至于要在任意路径下执行，再将主题放到theme中，我这里用的是yihui的[hugo-ivy](https://github.com/yihui/hugo-ivy)进行的修改，~~除了[yihui](https://yihui.org)的字体好像经过优化了，其他基本类似~~.
```shell
hugo new site </path/to/site>
git clone https://github.com/yihui/hugo-ivy themes/hugo-ivy
```
yihui的主题可以很好的支持行间公式(双美元符`$$`)，但是不能支持行内公式(单美元符`$`)，于是从[这里](https://note.qidong.name/2018/03/hugo-mathjax)中找到解决方案，即在`layouts/partials/mathjax.html`中加入：
```html
<script type="text/javascript"
        async
        src="https://cdn.bootcss.com/mathjax/2.7.3/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
MathJax.Hub.Config({
  tex2jax: {
    inlineMath: [['$','$'], ['\\(','\\)']],
    displayMath: [['$$','$$'], ['\[\[','\]\]']],
    processEscapes: true,
    processEnvironments: true,
    skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
    TeX: { equationNumbers: { autoNumber: "AMS" },
         extensions: ["AMSmath.js", "AMSsymbols.js"] }
  }
});

MathJax.Hub.Queue(function() {
    // Fix <code> tags after MathJax finishes running. This is a
    // hack to overcome a shortcoming of Markdown. Discussion at
    // https://github.com/mojombo/jekyll/issues/199
    var all = MathJax.Hub.getAllJax(), i;
    for(i = 0; i < all.length; i += 1) {
        all[i].SourceElement().parentNode.className += ' has-jax';
    }
});
</script>

<style>
code.has-jax {
    font: inherit;
    font-size: 100%;
    background: inherit;
    border: inherit;
    color: #515151;
}
</style>
```
最后在`partials/header_custom.html`中加入
```html
{{ partials "mathjax.html" }}
```

### 关于字体

yihui源博客采用的是思源字体，需要在css中嵌入js，登录[adobe fonts](https://fonts.adobe.com)中搜索`Source Han Serif Simplified Chinese`，选中后点击`</> Add to Web Project`，之后根据提示将`<script>`嵌入`partials/header_custom.html`中。可参考[这篇](https://imjad.cn/archives/lab/how-to-introduce-source-han-fonts-into-web-pages-through-typekit/)博客。

## 博客部署

首先在github上创建部署文件仓库excelkks.github.io，再在github上创建一个仓库blog用于存放源文件。

在hugo站点的路径blog下把hugo站点使用版本控制
```shell
cd blog
git init
```

最后在站点目录下添加子仓库excelkks.github.io
```shell
git submodule add https://github.com/excelkks/excelkks.github.io
```

最后进行部署，1.在blog站点下生成部署文件到excelkks.github.io，2.推送子仓库excelkks.github.io，3.推送站点源文件仓库blog
```shell
hugo -d excelkks.github.io
cd excelkks.github.io
git add .
git commit -m "comment"
git push
cd ..
git add .
git commit -m "comment"
git push
```

为了简化部署步骤，我写了一个[脚本](https://raw.githubusercontent.com/excelkks/blog/master/deploy.py)将部署、推送步骤合并
