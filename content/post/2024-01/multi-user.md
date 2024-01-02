---
title: "Multi-User.target"
date: 2024-01-02T16:00:12+08:00
description: Linux server into multi-user in short
categories: ["Linux", "operation"]
layout: search
tags: ["develop"]
---

# Linux 使用多用户模式

## 获取 runlevel

首先介绍一下 `runlevel`

| level | 模式说明 | 简介 |
| :---: | ------- | --- |
| 0 | 关机 | |
| 1 | 单用户 | 用于系统维护 禁止远程登录 |
| 2 | 多用户无网 | 没有NFS支持  |
| 3 | 多用户 | 标准运行模式 |
| 4 | 系统未使用 | |
| 5 | 图形化 | 登陆后进入GUI界面 |
| 6 | 重启 | |

可以通过下面三种方法来获取当前的 runlevel

```bash
runlevel
# N 5

who -r
# run-level 5  2023-12-31 13:16

systemctl get-default
# graphical.target
```

## 修改默认 runlevel

```bash
systemctl set-default multi-user.target
# multi-user.target 文件在 /lib/systemd/system/ 内
```

然后重启即可切换到新的 runlevel

## 直接切换 runlevel

`init 3` 不过有可能出问题 或者因为显示驱动(display driver)之类的问题导致连接在主机上的显示器有问题

reference:
[runlevel]: https://blog.csdn.net/weixin_45198978/article/details/127672033