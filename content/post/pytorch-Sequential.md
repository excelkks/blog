---
title: "Pytorch Sequential"
date: 2020-12-18T11:39:33+08:00
draft: false
tags:
- pytorch
- language
categories:
- pytorch
---

## `torch.nn.Sequential`

快速构建一个neural network可以通过`torch.nn.Module`构建类，也可通过设计一个`torch.nn.Sequential`来构建网络计算过程。实际上，只需要将网络上的各个计算过程都堆叠在Sequential中既可以了，例如：

```python
model = torch.nn.Sequential(
        torch.nn.Linear(3, 1),
        torch.nn.Flatten(0,1))
```

Sequential是一个容器，一般来说，可以用多个Sequential来构建Module. 例如LeNet-5网络的构建

```python
class LeNet5(torch.nn.Module):
    def __init__(self):
        super(LeNet5,self).__init__()
        self.conv1 = torch.nn.Sequential(
            torch.nn.Conv2d(1,6,5),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2,2)
        )
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv2d(6,16,5),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2,2)
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv2d(16,120,5),
            torch.nn.ReLU()
        )
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(120,84),
            torch.nn.ReLU(),
            torch.nn.Linear(84,10),
            torch.nn.LogSoftmax(dim=-1)
        )
    def forward(self, image):
        output = self.conv1(image)
        output = self.conv2(output)
        output = self.conv3(output)
        output = output.view(image.size(0),-1)
        output = self.fc(output)
        return output
```




