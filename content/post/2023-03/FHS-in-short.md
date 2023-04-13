---
layout: search
headless: true
title:  "FHS in short"
categories: ["linux", "filesystem"]
tags: ["develop"]
date: 2023-03-02T00:00:00+08:00
description: 简单叙述 [FHS][FHS-link] (Filesystem Hierarchy Standard) 不同路径的使用规范
---
简单叙述 [FHS][FHS-link] (Filesystem Hierarchy Standard) 不同路径的使用规范

# FHS

> 观前提示: `executable commands`和 `commands`等用于在本文都称为 **命令**

FHS 制定了一个文件存放规范来方便大家对文件的存储位置有个预期

最基础的 Root 下 一般包含

| Directory | Description |
| :-- | --- |
| bin |	Essential command binaries |
| boot |	Static files of the boot loader (用于系统启动) |
| dev |	Device files (存放所有设备文件和特殊文件) |
| etc |	Host-specific system configuration |
| lib |	Essential shared libraries and kernel modules |
| media |	Mount point for removeable media |
| mnt |	Mount point for mounting a filesystem temporarily |
| opt |	Add-on application software packages |
| sbin |	Essential system binaries |
| srv |	Data for services provided by this system |
| tmp |	Temporary files |
| usr |	Secondary hierarchy |
| var |	Variable data |

其他的可选项

- /home
- /lib\<qual> (比如 lib64)
- /root

## Root 下的结构

### /bin

> 包含了所有用户可用的命令

用户二进制目录 单层目录

### /sbin

> 系统二进制 (System BINaries) 用于系统**启动恢复和修复**等操作

### /etc

> 包含静态(只有管理员能改)配置文件 同时肯定不能有执行权限

- /etc/opt 是 /opt 的配置文件

### /lib

> 包含启动系统和在根文件系统执行命令的动态库

### /media /mnt

> 传统用 `/mnt` 作为挂载点 现在 `/media` 用得更多 (Ubuntu Desktop 默认挂载 `/media`)

### /opt

> 用于附加软件 (libreoffice 和 wemeet 会在这里)

## /usr 结构

这是第二个文件系统的主要部分

> 早期指用户路径 现在是 Unix/User/Universal System Resources

这个目录包含共享但只读的数据

必要的结构:

| Directory |	Description |
| --- | --- |
| bin |	Most user commands |
| include |	Header files included by C programs |
| lib |	Libraries |
| local |	Local hierarchy (empty after main installation) |
| sbin |	Non-vital system binaries |
| share |	Architecture-independent data |

### /usr/bin

> 存放系统命令的主要路径

### /usr/include

C 语言通用头文件

### /usr/lib

> Libraries for programming and packages

非用户直接使用的库

### /usr/local

用于管理员安装本地软件

通常拥有与 /usr 相同的层次结构

### /usr/sbin

非必要的标准系统命令

## /var

存放可变的数据文件
- spool 路径
- 管理和登录数据
- 临时文件

常规结构:

| Directory |	Description |
| --- | --- |
| cache |	Application cache data |
| lib |	Variable state information |
| local |	Variable data for /usr/local |
| lock |	Lock files |
| log |	Log files and directories |
| opt |	Variable data for /opt |
| run |	Data relevant to running processes |
| spool |	Application spool data |
| tmp |	Temporary files preserved between system reboots |

## /proc in Linux

> 内核与进程信息虚拟文件系统

Linux 事实(de-facto)上获取进程和系统信息的标准方法

[FHS-link]: https://www.pathname.com/fhs/pub/fhs-2.3.html