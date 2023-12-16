---
title: "PyTorch Traps"
date: 2023-12-14T10:42:25+08:00
description: PyTorch Traps and Pitfalls
categories: ["PyTorch", "dev", "misc"]
layout: search
tags: ["develop"]
---

# PyTorch-Traps

## 1. 意外的条件判断

众所周知 在Python的条件判断语句下 只有下面几个值判断为 `False` :
- `[]`/`()`
- `""`/`''`
- `0`/`0.0`
- `None`

但是可能不清楚 `tensor([0])` 也能隐式转换为 False

```python
>>> import torch as th
>>> zero = th.tensor([0])
>>> zero2d = th.tensor([0,0])
>>> empty = th.tensor([])
>>> if not zero:
...     print("zero is False")
... 
zero is False
>>> if not empty:
...     print("empty is False")
... 
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: Boolean value of Tensor with no values is ambiguous
>>> if not zero2d:
...     print("zero2d is False")
... 
RuntimeError: Boolean value of Tensor with more than one value is ambiguous
```

## 2. 复杂的广播规则

PyTorch 的广播机制可以很方便实现矩阵操作 不过会有一些广播上的意外情况发生 ~~具体实现自行查看PyTorch源码~~

试想象下面一些矩阵加法的结果
- `[2, 3, 4]+[2, 1, 4]`
- `[2, 3, 4]+[2, 3]`
- `[2, 3, 4]+[3, 4]`
- `[2, 1, 3]+[2, 3]`

```python
>>> a3d.shape, b2d.shape, c3d.shape, d2d.shape, e3d.shape
(torch.Size([2, 3, 4]), torch.Size([2, 3]), torch.Size([2, 1, 4]), torch.Size([3, 4]), torch.Size([2, 1, 3]))
```

答案揭晓为:
- `[2, 3, 4]+[2, 1, 4]=[2, 3, 4]` 相当于广播在dim=1的地方
- `[2, 3, 4]+[2, 3]=RuntimeError` The size of tensor a (4) must match the size of tensor b (3) at non-singleton dimension 2
- `[2, 3, 4]+[3, 4]=[2, 3, 4]` 相当于增加一个dim=0 再在dim=0出广播
- `[2, 1, 3]+[2, 3]=[2, 2, 3]` 

```python
>>> (a3d+c3d).shape # [2, 3, 4]+[2, 1, 4]
torch.Size([2, 3, 4])
>>> th.eq(c3d.tile(1,3,1) + a3d, a3d + c3d).all().item()
True


>>> (a3d+b2d).shape # [2, 3, 4]+[2, 3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: The size of tensor a (4) must match the size of tensor b (3) at non-singleton dimension 2


>>> (a3d+d2d).shape # [2, 3, 4]+[3, 4]
torch.Size([2, 3, 4])
>>> th.eq(a3d + d2d.unsqueeze(dim=0).tile(2,1,1), a3d + d2d).all().item()
True


>>> (e3d+b2d).shape # [2, 1, 3]+[2, 3]
torch.Size([2, 2, 3])
>>> th.eq(e3d.tile(1,2,1) + b2d.unsqueeze(dim=0).tile(2,1,1), e3d + b2d).all().item()
True
```

## 3. 保持单进程日志读写

在分布式训练时 注意日志读写与模型存储只使用单一进程来完成 一般使用 `rank==0` 的进程