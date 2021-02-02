---
title: "os模块"
date: 2020-12-11T10:49:06+08:00
draft: false
tags:
- python
categories:
---

### os.walk

`os.walk(path)`用于遍历目录。返回值是一个遍历器，需要用`for`循环不断遍历，每次遍历得到长度为3的tuple，分别为(目录, [目录下的子目录], [目录下的文件])。
使用方法示例:
```python
for root, dirs, files in os.walk('.'):
    for file in files:
        print(os.path.join(root, file))
    for dir in dirs:
        print(os.path.join(root, dir))
```
```shell
./directory_2
./directory_1
./directory_2/file_2_1
./directory_2/directory_2_1
./directory_2/directory_2_1/file_2_1_1
./directory_1/directory_1_1
./directory_1/directory_1_2
./directory_1/directory_1_1/file_1_1_2
./directory_1/directory_1_1/file_1_1_1
./directory_1/directory_1_2/file_1_2_1
```
### glob模块
#### glob.glob
`glob.glob`用于以shell-style的方式匹配目录下的文件, 例如shell匹配所有jpg图片
```shell
*.jpg
```
在python中用`glob.glob`的方式为
```python
files = glob.glob('*.py')
```

### numpy模块
#### random.get_state

`numpy.random.get_state()`一般与`numpy.random.set_state()`和`numpy.random.shuffle()`一起使用，用于打乱numpy数组的顺序。例如打乱数据集
```python
state = np.random.get_state()
np.random.shuffle(dataset_images)
# 保证打乱的顺序与之前一致
np.random.set_state(state)
np.random.shuffle(dataset_labels)
```
