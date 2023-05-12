---
title: "Projection"
date: 2020-12-18T11:45:23+08:00
draft: false
tags:
- linear algbra
categories:
---

# projection

$p = \hat{x}a$

$e = b - \hat{x}a$

$a\perp e \to a^T(b-\hat{x}a)=a^Tb - \hat{x}a^Ta = 0 \to \hat{x}=\frac{a^Tb}{a^Ta}$

$p = \hat{x}a = a\frac{a^Tb}{a^Ta}$

$p = Pb = \frac{aa^T}{a^Ta}b \to P = \frac{aa^T}{a^Ta}$

$P = P^T$, $P = P^2$

$P$ is a line trough $a$.

## why projection?

Because $Ax = b$ may have no solution. So we may find a $p$ closest to $b$ that makes  $A\hat{x} = p$ do have solution. Here $p$ is the projection of $b$ onto the column space. 

Let $a_1, a_2\in R^2$ independent, then $a_1, a_2$ consist a plane. 

$\hat{x}_1a_1 + \hat{x}_2a_2 = p = A\hat{x}$

$e = b - A\hat{x}$

$e\perp column space$, so, $a_1^T(b-A\hat{x}) = 0$, and $a_2^T(b-A\hat{x})=0$, that is $A^T(b-A\hat{x}) = 0$

$A^Te = 0$, so $e$ is in $N(A^T)$, $e \perp C(A)$

**KEY EQUATION** $A^TA\hat{x} = A^Tb$

solution: $\hat{x} = (A^TA)^{-1}A^Tb$

projection: $p = A\hat{x} = A(A^TA)^{-1}A^Tb$

projection matrix: $P = A(A^TA)^{-1}A^T$

$P^2 = A(A^TA)^{-1}A^TA(A^TA)^{-1}A^T = A(A^TA)^{-1}A^T$

## least squares

Given batch of points close to but not on the line. Suppose those points are $(1, 1)$, $ (2,2)$, $(3,2)$. Find $C, D$ makes those points closest to the line $C+Dt = b$.

$$\left[\begin{matrix}1 & 1 \\\\ 1 & 2 \\\\ 1 & 3\end{matrix}\right]\left[\begin{matrix}C\\\\D\end{matrix}\right]=\left[\begin{matrix}1\\\\2\\\\3\end{matrix}\right] \to A\left[\begin{matrix}C\\\\D\end{matrix}\right]=b$$

No solution to this equation. So we Minimize the $||Ax - b||^2 = ||e||^2$, $||e||^2 = e_1^2+e_2^2+e_3^2$


