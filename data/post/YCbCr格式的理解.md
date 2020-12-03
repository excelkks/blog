---
title: YCbCr格式的理解
date: 2019-12-05 16:37:21
tags:
- 视频编解码
- 视频格式
categories:
- 视频编解码
---

### YCbCr格式的理解
#### YUV格式
YUV格式有别于传统的RGB三原色格式，YUV是将亮度分量Y和两个色度分量U、V分开，其中Y表示灰阶值，U表示蓝色与亮度值之间的差异，V表示红色与亮度之间的差异，于是对亮度分量的处理Y并不影响U、V分量，此外单独传输Y分量可向后兼容老式黑白电视。YCbCr格式与YUV格式类似，YCbCr主要应用于图像、视频压缩的数字彩色信息表示，是YUV压缩和偏移的版本。RGB与YCbCr的转换如下：

$$
\begin{bmatrix}
    Y \\
    Cb \\
    Cr
\end{bmatrix} = 
\begin{bmatrix}
    0.299 & 0.587& 0.114 \\
    -0.169& -0.331& 0.449 \\
    0.449 & -0.418& -0.0813 \\
\end{bmatrix}
\begin{bmatrix}
    R \\ G \\ B
\end{bmatrix}+
\begin{bmatrix}
    0 \\ 128 \\ 128
\end{bmatrix}
$$


$$
\begin{bmatrix}
    R \\ G \\ B
\end{bmatrix} =
\begin{bmatrix}
    1.0 & 0.0 & 1.402 \\
    1.0 & -0.344 & -0.714 \\
    1.0 & 1.772 & 0.0 
\end{bmatrix}
\begin{bmatrix}
    Y \\ Cb-128 \\ Cr-128
\end{bmatrix}
$$


#### 色度亚采样
由于人眼对于色度的敏感度要低于对亮度的敏感度，因此，可采用低于亮度的采样率对色度采样，从而达到视频压缩的目的，衍生的YCbCr采样格式有4:4:4、4:2:2、4:1:1、4:2:0。它们的采用方式如下图所示，4:4:4采样比较容易理解，不作表述。4:2:2采样表示水平方向上，每4个Y分量对应2个Cb分量和2个Cr分量；4:1:1采样表示水平方向上，每4个Y分量对应1个Cb分量和1个Cr分量；4:2:0采样表示水平方向上，每4个Y分量对应2个Cb分量和0个Cr分量，或者每4个Y分量对应0个Cb分量和2个Cr分量。
![YUV采样](/images/YUV_sampling.png "YUV采样")

#### YCbCr格式的存储方式
YCbCr数据的存放分为两类，packed formats和planar formats。Packed formats的Y, Cr(U), Cb(V)一起存放在一个数组中，依据像素点交替存放，类似YCbCrYCbCrYCbCr....；Planar formats的Y, Cr(U), Cb(V)每个分量单独存放，存放的方式类似YYY...CbCbCb...CrCrCr...
Packed formats以4:2:0采样方法举例，假设分辨率为8x2，如下图所示：
