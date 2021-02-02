---
title: "Pytorch基础"
date: 2020-12-18T11:30:07+08:00
draft: false
tags:
- pytorch
- language
categories:
- pytorch
---


[toc]

## Tensor的创建

`tensor`是基本的数据类型，基本的创建方式有

- `torch.empty(5, 3)` 未初始化的tensor, 里面的值为内存中原有的值
- `torch.randn(5,3)` 创建tensor，并随机初始化
- `torch.zeros(5, 3, dtype=torch.long)` 创建tensor，并初始化为0，指定数据类型
- `torch.tensor([5.5, 3])`创建tensor，并直接值初始化

除了上述的创建方式，还有可以利用已经存在的tensor来创建，假设现有`x = torch.zeros(5,3, dtype=torch.float32)`，那么，可以根据以下方式创建

- `x.new_ones(5,3)` 创建tensor，并值初始化为0，除了shape外，其他属性与x一致
- `torch.randn_like(x, dtype=torch.float)` 创建tensor，随机初始化值，除了明确指定的属性`type=torch.float`外，其他属性与x一致

## Operations

### 加法

- 直接加

  ```python
  x = torch.randn(5, 3)
  y = torch.randn(5, 3)
  # 直接加
  result1 = x + y 
  ```

- 函数方法

  ```python
  # 结果赋值到result2
  result2 = torch.add(x, y)
  # 预先指定结果保存到变量
  torch.add(x, y, out=result3)
  ```

- 立地加(in-place)

  ```python
  # 立地(in-place)加，结果直接加到被加数中, 一般立地加的函数都以_结束，
  # 例如x.copy_(y), x.t_()
  y.add_(x)
  ```

### 索引

可以使用标准的类似`numpy`的索引。例如`x[:, 1]`

### resize

resize或者reshape一个tensor，可以使用函数`torch.view`，例如

```python
x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8) # -1 表示该维度的值由其他维度推断，这里这个维度的值16/8 = 2
print(x.size(), y.size(), z.size)
# out
# >> torch.Size([4, 4]) torch.Size([16]) torch.Size([2, 8])
```

更多操作可以[参考这里](https://pytorch.org/docs/stable/torch.html)

## 与numpy连接

事实上，tensor的大多数操作都和numpy类似。这里简单介绍tensor与numpy的互相转换

### tensor -> numpy

```python
a = torch.ones(5) # a: tensor([1., 1., 1., 1., 1.])
b = a.numpy() # b: [1. 1. 1. 1. 1.]
```

注意tensor改变后，numpy数组的变化

```python
a.add_(1) 
# a: tensor([2., 2., 2., 2., 2.])
# b: [2. 2. 2. 2. 2.]
# tensor改变的同时也会改变numpy数组
```

### numpy -> tensor

```python
import numpy as np
a = np.ones(5)
b = torch.from_numpy(a)
np.add(a, 1, out=a)
# a: [2. 2. 2. 2. 2.]
# b: tensor([2., 2., 2., 2., 2.])
```

## 自动梯度

### tensor的`requires_grad`属性

每一个tensor有一个`requires_grad`的属性，如果这个属性设置为`True`，那么程序将会跟踪与这个tensor所有有关的计算过程，以此来在后续计算它的梯度，计算完的梯度**累加**在tensor的`grad`属性中。例如$y=f(x)=a+bx$，$z = g(y)=c+dy$，$f(x), g(y)$均会被跟踪，因为计算$x$的梯度为$\frac{\partial z}{\partial x}=\frac{\partial z}{\partial y}\frac{\partial y}{\partial x}$

#### `requires_grad`

用于指定是否需要加入跟踪以计算梯度，例如

```python
x = torch.ones(2, 2, requires_grad=True)
# x: tensor([[1., 1.],
#            [1., 1.]], requires_grad=True)
y = x + 2
# y: tensor([3., 3.],
#           [3., 3.], grad_fn=<AddBackward0>)
```

#### 临时暂停跟踪

有时，$x$ 参与的一些计算并不需要加入跟踪，也即不需要用于计算梯度，比如临时计算精准度，那么这时需要暂停跟踪。方法如下

##### `detach`

直接在需要暂停的变量后执行`detach()`获得一个不被跟踪的tensor以替代x

```python
x_detached = x.detach()
# do someting here using x_detached
```

##### `with torch.no_grad():`

除了detach创建变量，还可通过上下文管理器`torch.no_grad()`用于指示接下来的操作都不跟踪，例如

```python
with torch.no_grad():
  # do someting here using x
  # 这里的操作都不会被跟踪
# 上下文管理器外的操作又会继续跟踪
```

#### 更改requires_grad属性

对于`requires_grad`属性为`False`的tensor，可以通过`requires_grad_(True)`改变属性。例如

```python
a = torch.randn(2, 2)
a.requires_grad(True)
# 改变requires_grad属性
```

### Function

function说明了tensor的计算过程，tensor的`grad_fn`属性与一个function绑定，用于说明这个tensor如果计算传递过来的。例如

```python
x = torch.ones(2, 2, requires_grad=True)
y = x + 2
# y: tensor([[3., 3.],
#            [3., 3.]], grad_fn=<AddBackward0>)
z = y*y*3
out = z.mean()
# out: tensor(27., grad_fn=<MeanBackward0>)
```

### 梯度计算

带有`grad_fn`属性的`tensor`，调用`backward()`可以根据该tensor的`grad_fn`属性向前计算各个tensor的梯度，并存在各个tensor的`grad`属性中。例如

```python
out.backward()
print(x.grad)
# >> tensor([[4.5, 4.5],
#            [4.5, 4.5]])
```

### 其他方法

#### `item()`

对于一个只含有一个数的`tensor`可以使用`item()`方法获取这个数值，但如果`tensor`中的数据不止1个，则会报错，例如

```python
a = torch.tensor([1])
a.item()  # 1
b = torch.tensor([1,2,3])
b.item() # ValueError: only one element tensors can be converted to Python scalars
```


