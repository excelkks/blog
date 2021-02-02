---
title: "Pytorch自定义函数"
date: 2020-12-18T11:33:36+08:00
draft: false
tags:
- pytorch
- language
categories:
- pytorch
---

[toc]

## `torch.autograd.Function`

自定义一个计算过程，并且定义其反向传播过程。例如计算 $y = a+bx+cx^2+dx^3$时，用两步替代该过程 $y= a+b\times P_3(c+dx), P_3(x) = \frac{1}{2}(5x^3-3x)$

那么可以通过`torch.autograd.Function`定义$P_3(x)$，过程如下：

```python
# -*- coding: utf-8 -*-
import torch
import math


class LegendrePolynomial3(torch.autograd.Function):
    """
    We can implement our own custom autograd Functions by subclassing
    torch.autograd.Function and implementing the forward and backward passes
    which operate on Tensors.
    """

    @staticmethod
    def forward(ctx, input):
        """
        In the forward pass we receive a Tensor containing the input and return
        a Tensor containing the output. ctx is a context object that can be used
        to stash information for backward computation. You can cache arbitrary
        objects for use in the backward pass using the ctx.save_for_backward method.
        """
        ctx.save_for_backward(input)
        return 0.5 * (5 * input ** 3 - 3 * input)

    @staticmethod
    def backward(ctx, grad_output):
        """
        In the backward pass we receive a Tensor containing the gradient of the loss
        with respect to the output, and we need to compute the gradient of the loss
        with respect to the input.
        """
        input, = ctx.saved_tensors
        return grad_output * 1.5 * (5 * input ** 2 - 1)
```

### `apply`方法

`torch.autograd.Function`定义的计算过程通过`apples`来调用。例如

```python
P3 = LegendrePolynomial3.apply
y_pred = a + b*P3(c+d*x)
```




