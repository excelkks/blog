---
title: "Tensorflow"
date: 2020-12-09T09:58:47+08:00
draft: false
tags:
- tensorflow
- language
categories:
---

### 使用GPU

为了避免占用全部GPU，需要加上

```python
import os
os.environ['CUDA_DEVICES_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
config = tf.ConfigProto()
#config.gpu_options.per_process_gpu_memory_fraction = 0.9
config.gpu_options.allow_growth = True
```





`tf.truncated_normal_initializer`

生成截断正态分布的初始化器**类**

- 参数
  - mean: 分布的均值
  - stddev: standard deviation，标准差
  - seed: 随机种子
  - dtype: 数据类型，只能是float的类型，可选位数

`tf.get_variable()`

获取一个变量或者创建一个新的变量

- 重要参数
  - shape: list类型，是指变量的shape
  - Initializer: 用于生成变量的初始化器 

`tf.nn.conv2d()`

2维卷积函数，列举主要参数tf.nn.conv2d(input, filter=None, strides=None, paddig=None, data_format='NHWC')。

- 重要参数
  - input: 输入4-D的Tensor，数据格式只能是`half`,`bfloat16`,`float32`,`float64`
  - filter: 卷积核，也是一个4-D tensor，数据格式必须与input一样
  - strides: 移动步长，可以是长度为1,2,4的list，长度为1时，表示宽高方向的移动步长，并且一致。长度为2时，分别指定宽高方向的移动步长。长度为4时，设定根据data_format指定的位置对应方向移动步长。
  - padding: 'VALID'表示不填充， SAME'表示填充。填充方式根据filter而定，如果filter的一个维度上的长度为奇数，则在该维度起始处和结束处填充0，如果为偶数则在结束处填充0。

一般来说，input的各个维度为`[batch, in_height, in_width, in_channels]`，filter的各个维度为 `[filter_height, filter_width, in_channels, out_channels]`

## 初始化变量

变量需要初始化，初始化方法有单独初始化和全局初始化。

### 单独初始化

```python
v1 = tf.Variable(tf.random_normal([2, 3], stddev=2))
v2 = tf.Variable(tf.random_normal([2, 3], stddev=1))

sess = tf.Session()
sess.run(v1.initializer)
sess.run(v2.initializer)
```

### 全局初始化

```python
v1 = tf.Variable(tf.random_normal([2, 3], stddev=2))
v2 = tf.Variable(tf.random_normal([2, 3], stddev=1))

sess = tf.Session()
init_op = tf.global_variable_initializer()
sess.run(init_op) # initialize all varibles
```

变量的维度一般不变，但也可以在运行时改变，例如

```python
w1 = tf.Variable(tf.random_normal([2,3], stddev=1), name="w1")
w2 = tf.Variable(tf.random_normal([2,2], stddev=1), name="w2")

tf.assign(w1, w2)  # error, shapes not match
tf.assign(w1, w2, validate_shape=False) # normally eval
```

`tf.reduce_mean()`: 默认将所有数放到一维空间计算均值，可指定计算的维度。

## 梯度下降

- 全局梯度下降：会陷入局部最优解，且耗时
- 随机梯度下降：速度提升了，但只在部分数据上优化，达不到全局最优，甚至达不到全局最优
- mini-batch随机梯度下降：速度提升了，不易陷入局部最优

### softmax

`tf.nn.softmax_cross_entropy_with_logits_v2（label=y_, logits=y)` 用于计算对y经过softmax之后的结果与标签y_的交叉熵。也就是
$$
\sum\limits_{i=1}^ny\_i\log\frac{e^{y_i}}{\sum_{j=1}^ne^{y_j}}
$$
对于只有一个正确答案的分类问题，也就是标签都形如$y\_i=[\cdots,0,0,1,0,0,\cdots]$，可以用`tf.nn.sparse_softmax_cross_entropy_with_logits`来加快运算。


