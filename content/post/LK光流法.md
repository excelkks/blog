---
title: LK光流法
date: 2019-11-18 11:10:53
tags:
- 光流法
- 超定方程
- 最小二乘法
categories:
- 视频编解码
---
## 1 超定方程组求解

### 1.1 超定方程组


超定方程组是指方程的个数大于未知数个数的方程组，例如

`
$$
\begin{bmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
... & ... & ... \\
a_{n1} & a_{n2} & a_{n3} \\
\end{bmatrix}\times
\begin{bmatrix} 
x_1 \\ x_2 \\ x_3 \\
\end{bmatrix} = 
\begin{bmatrix} 
b_1 \\ b_2 \\ ... \\ b_n \\
\end{bmatrix}
$$
`

其中，$n>3$，将上述方程表示为$\boldsymbol{A}\_{n\times 3}x\_{3\times 1}=b\_{n\times 1}$，该方程不能按照一般的求解方法求解，但可以求的最小二乘法的解。


先给出结论，该超定方程组的最小二乘解为：
$$x=(\boldsymbol{A}^{T}\boldsymbol{A})^{-1}\boldsymbol{A}^{T}b$$

### 1.2 超定方程组的最小二乘解
对于无一般解的超定方程组$\boldsymbol{A}x=b$来说，假设$r=\boldsymbol{A}x -b$，使得$||r||^2_2=（\boldsymbol{A}x -b)^{T}(\boldsymbol{A}x -b)$的值最小的解即为最小二乘解。于是，问题转变为最小化$(\boldsymbol{A}x -b)^{T}(\boldsymbol{A}x -b)$，令
$$J(x)=(\boldsymbol{A}x-b)^T(\boldsymbol{A}x-b)$$
对上式求导，可得 

`$$
\begin{aligned}
\frac{\partial J(x)}{\partial x} & =\frac{\partial{(\boldsymbol{A}x-b)^T(\boldsymbol{A}x-b)}}{\partial{x}} \\
& =\frac{\partial(x^T\boldsymbol{A}^T\boldsymbol{A}x-x^T\boldsymbol{A}^Tb-b^T\boldsymbol{A}x+b^Tb)}{\partial{x}} \\
& =(\boldsymbol{A}^T\boldsymbol{A}x)^T+x^T\boldsymbol{A}\boldsymbol{A}-b^T\boldsymbol{A}-b^T\boldsymbol{A} \\
& =2(x^T\boldsymbol{A}^T\boldsymbol{A}-b^T\boldsymbol{A})
\end{aligned}
$$`

令$\frac{\partial{J(x)}}{\partial{x}}=0$，那么，可以解得

$$
x=(\boldsymbol{A}^T\boldsymbol{A})^{-1}\boldsymbol{A}^Tb
$$

## 2 LK光流法
Optical flow光流简单来说是描述物体的运动，可理解为运动向量。光流法可用于运动检测、物体切割、运动补偿编码等等方向。
### 2.1 光流的计算
光流法实际是通过检测图像像素点的强度随时间的变化进而推断出物体移动速度及方向的方法.

光流法的假设条件：
- 物体移动很小
- 相同像素点移动前后像素强度不变（一般指亮度）

现假设在时间$t$时，点$(x,y)$处像素点强度为$I(x,y,t)$，那么$\Delta{t}$时间后，该像素点将移动到$(x+\Delta{x},y+\Delta{y})$处，像素强度为$I(x+\Delta{x},y+\Delta{y},t+\Delta{t})$，对其进行泰勒级数展开得到：

`$$
\begin{aligned}
    & I(x+\Delta{x},y+\Delta{y},t+\Delta{t}) \\
= & I(x,y,t)+\frac{\partial{I}}{\partial{x}}\Delta{x}+\frac{\partial{I}}{\partial{y}}\Delta{y}+\frac{\partial{I}}{\partial{t}}\Delta{t}+H.O.T.
\end{aligned}
$$`

基于假设条件，相同像素移动前后的强度不变，同时忽略$H.O.T$，可得：
$$
\frac{\partial{I}}{\partial{x}}\Delta{x}+\frac{\partial{I}}{\partial{y}}\Delta{y}+\frac{\partial{I}}{\partial{t}}\Delta{t}=0
$$
可写作：
$$
\frac{\partial{I}}{\partial{x}}\frac{\Delta{x}}{\Delta{t}}+\frac{\partial{I}}{\partial{y}}\frac{\Delta{y}}{\Delta{t}}+\frac{\partial{I}}{\partial{t}}\frac{\Delta{t}}{\Delta{t}}=0
$$
令$\frac{\Delta{x}}{\Delta{t}}=V_x$表示$x$方向上的运动速度，$\frac{\Delta{y}}{\Delta{t}}=V_y$表示$y$方向上的运动速度，那么最终可得：
$$
\frac{\partial{I}}{\partial{x}}V_x+\frac{\partial{I}}{\partial{y}}V_y+\frac{\partial{I}}{\partial{t}}=0
$$
$V_x$, $V_y$也即为$I(x,y,t)$的光流，$\frac{\partial{I}}{\partial{x}}$,$\frac{\partial{I}}{\partial{y}}$,$\frac{\partial{I}}{\partial{t}}$为图像$(x,y,t)$在对应方向的偏导数。

显然上式中，两个未知数，一个方程，无法求解，以下介绍LK光流法求解。

### 2.2 LK光流法求解
卢卡斯-卡纳徳(Bruce D. Lucas和Takeo Kanade)光流法在光流假设条件下增加了另一个假设条件
- 假设光流在像素点的邻域是一个常数

那么，假设研究领域大小为$N\times{N}$，那么在该区域内的光流均相等，根据光流的计算方法，该区域内有等式：

`$$
\begin{aligned}
    & I_x(p_1)V_x+I_y(p_1)V_y = -I_t(p_1) \\
    & I_x(p_2)V_x+I_y(p_2)V_y = -I_t(p_2) \\
    & \cdots                              \\
    & I_x(p_n)V_x+I_y(p_n)V_y = -I_t(p_n)
\end{aligned}
$$`

写成矩阵形式

`$$
\begin{bmatrix}
    I_x(p_1) & I_y(p_1) \\
    I_x(p_2) & I_y(p_2) \\
    \cdots \\
    I_x(p_n) & I_y(p_n)
\end{bmatrix}
\begin{bmatrix}
    V_x \\ V_y
\end{bmatrix}
=\begin{bmatrix}
    -I_t(p_1)\\
    -I_t(p_2) \\
    \cdots \\
    -I_t(p_n)
\end{bmatrix}
$$`

根据最小二乘法求解超定方程$Ax=b$方法，$x=(\boldsymbol{A}^T\boldsymbol{A})^{-1}\boldsymbol{A}^Tb$，上述矩阵解为
`$$
\begin{bmatrix}
    V_x \\ V_y
\end{bmatrix}
=\begin{bmatrix}
    \sum_iI_x(p_i)^2 & \sum_iI_x(p_i)I_y(p_i) \\
    \sum_iI_y(p_i)I_x(p_i) & \sum_iI_y(p_i)^2 \\
\end{bmatrix}^{-1}
\begin{bmatrix}
    -\sum_iI_x(p_i)I_t(p_i) \\
    -\sum_iI_y(p_i)I_t(p_i)
\end{bmatrix}
$$`

最终求的该区域内的光流为$V_x,V_y$。

总结:
- 三个条件
  1. 物体运动足够小
  2. 同一像素点移动前后的强度不变
  3. 一定区域内的光流值一致
- 最小二乘法求解超定方程
