---
title: "Hash"
date: 2022-05-23T22:11:59+08:00
description: 常见 hash 算法
categories: ["introduce"]
layout: search
tags: ["develop"]
---

# Hash

## [MD5](https://datatracker.ietf.org/doc/html/rfc1321)

[讲解](https://www.bilibili.com/video/BV1S541127qR)

> Message Digest

原始数据 ->512bit补齐(第一位补1 后续补0 最后64位存储原始数据长度(mode $2^64$)~~小端存储~~)-> 128bit

特点
1. 压缩性:任意长度的数据 算出的MD5值长度都是固定的
2. 容易计算:从原数据计算出MD5值很容易
3. 抗修改性:对原数据进行任何改动 哪怕只修改1个字节 所得到的MD5值都有很大区别
4. 抗弱碰撞:已知原数据和其MD5值 想找到一个具有相同MD5值的数据(即伪造数据)是非常困难的
5. 强抗碰撞:想找到两个不同的数据 使它们具有相同的MD5值 是非常困难的

### 问题

彩虹表: 一个存储常见数据md5值的词典

相同前缀碰撞
1. 保留相同前缀
2. 不断构造后缀

选择前缀碰撞
1. 自由选择前缀

### 加盐

> salt: 一个随机字符串 用于添加到数据中(位置可以灵活选择) 然后md5 hash计算

- 静态盐: 使用固定的盐
- 动态盐: 每次随机生成盐

## 安全要求

### 原像攻击

通过值找到任一原像

### 第二原像攻击

已知一个原像 能否找到第二个原像与已知原像值相同

### 抗碰撞性

有方法找到值相同的两个原像

## [SHA](https://zh.wikipedia.org/wiki/SHA%E5%AE%B6%E6%97%8F)

> Secure Hash Algorithm

- SHA-0:160(5x32)bit
- SHA-1:160(5x32)bit
> 原始数据 ->512bit补齐最后64位存储原始数据长度
- SHA-2(算法:输出长度(中继hash值长度)/block size)
  - SHA-224:224/512
  - SHA-256:256(8x32)bit/512
  - SHA-384:384/1024
  - SHA-512:512(8x64)bit/1024
- SHA-3

## Hash 算法与签名算法

Hash算法(指纹算法)计算出Hash值 是一个不可逆的过程 **是签名算法的一个组件**

签名算法对hash值进行非对称加密 从而保证可靠性 防止非法篡改
> 签名可以与数据一起存储 也可以分开存储

## 参考

- [MD5 B站视频讲解](https://www.bilibili.com/video/BV1S541127qR)
- [签名与Hash](https://blog.csdn.net/luo_boke/article/details/107128529)