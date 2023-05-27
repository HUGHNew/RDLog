---
title: "Immutable Linux"
date: 2023-05-27T21:43:27+08:00
categories: ["Linux", "introduction", "concept"]
layout: search
tags: ["develop"]
---

# Immutable Linux

简单介绍一下不可变Linux的概念

> 不可变发行版确保操作系统的核心保持不变

上面这句话是一个比较经典的解释[2] 不过正常人是看不懂的

不可变Linux系统 也被称为不可变基架(Infrastructure)或者不可变部署(Deployment) 在安装之后**系统文件和路径**不可更改(pre-install的部分) 所有的更改在系统重启后都会恢复(就像恢复到快照一样)

优势在于
- 更安全
- 更好维护: 升级的粒度为系统级而不是包级别
- 更可靠: 系统只读

系统的升级方式为: 生成一个新的系统镜像 然后替换掉原来的镜像(image-based upgrade)

在传统的Linux和Immutable Linux之间 还存在带有不可变特性的一种方案: 事务性更新(Transactional upgrades)

通过ABRoot两个根分区的方式 来实现重启之后系统文件的更新 这样的方式与不可变Linux的升级方式差不多

## 一些可以玩的系统

- NixOS: 基于配置的可重现非FHS Linux系统
- Fedora Silverblue: 基于Fedora的Immutable Linux
- Vanilla OS: 现基于Ubuntu 将基于Debian Sid的带有Immutable特性的系统(ABRoot, Container-friendly)

## 修改文件的可变属性

`chattr/lsattr` in `e2fsprogs`(默认自带包)

更多见[3] ~~现在懒得翻译~~

## references

1. <https://kairos.io/blog/2023/03/22/understanding-immutable-linux-os-benefits-architecture-and-challenges/>
2. <https://linux.cn/article-15841-1.html>
3. <https://www.xmodulo.com/make-file-immutable-linux.html>
