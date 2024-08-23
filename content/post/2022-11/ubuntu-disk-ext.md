---
title: "Ubuntu Disk Extension"
date: 2022-11-24T11:49:05+08:00
description: 双系统Ubuntu根分区扩容
categories: ["Linux", "operation"]
layout: search
tags: ["develop"]
---

# 双系统Ubuntu根分区扩容记录

> 硬盘有价，**数据无价**，行动前要**三思**！

双系统下后装的系统扩容有点麻烦，涉及的问题可能包括

- 移动 EFI 分区
- 分区向左扩展

## 准备

1. Ubuntu 镜像U盘 推荐用Windows制作方便一点
2. Ubuntu 所在磁盘的空闲空间

## 具体操作

### 概述

1. 做完准备工作
2. 插入U盘 以U盘重启
3. 选择试用Ubuntu (Try Ubuntu)
4. 打开**GParted**
4. 备份 **EFI** 分区(空闲头部建立 **FAT32** 分区，然后复制挂载 /boot/efi 的那个分区)
4. 删除原来的 EFI 分区~~这一步感觉风险很大~~
4. 这时候 根分区就能向左扩容了
4. 保存更改
4. 尝试能否启动

### 过程与解疑

为什么要用U盘？ 因为直接用系统的话，分区是不能调整的

![local ref](https://img-blog.csdnimg.cn/20190516180733792.png)

图源网络：但是可以看见直接运行gparted分区会有锁，不能操作

使用U盘上系统gparted能解锁

![U-gparted](https://img-blog.csdnimg.cn/20190516182242813.jpg)

图源网络：这时候可以操作分区了

一般情况下 挂载根目录的分区与未分配是不相邻的

我分区时便是未分配和根分区中间夹了一个 EFI 系统分区

我的操作方式是直接复制 EFI 到未分配的最前段

> 更好一点的操作方式应该是 对 EFI 分区扩容再压缩

再之后就是正常的向左扩容了。

## 扩容结果

![扩容结果图](images/ubuntu-ext.png)

问题：

- 重启没有读取到Ubuntu的grub引导 需要手动BIOS引导引入
- 可能有一些软件报错~~比如我VSCode报错 但不知道为什么~~

参考

- https://zhuanlan.zhihu.com/p/422981369
- https://blog.csdn.net/Carina_Cao/article/details/90270389

> 免责：磁盘操作需谨慎，本文仅作为个人操作后的记录和尝试该行为的参考