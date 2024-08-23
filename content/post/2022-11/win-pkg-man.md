---
title: "Windows Package Manager"
date: 2022-11-24T11:49:05+08:00
description: 探寻 Windows 下的包管理工具
categories: ["Windows", "operation", "introduction"]
layout: search
tags: ["develop"]
---

# Windows包管理器

## Scoop

> Scoop is an installer
>
> The goal of Scoop is to let you use Unix-y programs in a normal Windows environment
>
> (Scoop是一个让你在Windows上方便获取开源CLI工具的安装器)

> scoop 依赖于git/github 在无代理情况下很羸弱

### 下载/安装

~~如果没有代理的话，建议参考[这里](https://shenbo.github.io/2021/03/23/apps/%E4%BD%BF%E7%94%A8scoop%E5%AE%89%E8%A3%85%E7%AE%A1%E7%90%86windows%E8%BD%AF%E4%BB%B6(2)-github%E5%8A%A0%E9%80%9F/)~~

> 如果下载scoop的过程中断 那么必须先删除(`C:\Users<user>\scoop`)文件夹 再执行以上命令安装
>
> Scoop的bucket概念和`apt`的ppa概念相近

打开PowerShell

```powershell
iex (new-object net.webclient).downloadstring('https://get.scoop.sh')
```

如果报错 Policy 相关的 先执行下面这条再执行如上下载操作

```powershell
set-executionpolicy remotesigned -s cu 
```



> scoop软件默认下载路径为 `C:\Users\<User>\scoop\apps`

### 使用

可以考虑使用国内镜像版<https://gitee.com/squallliu/scoop>

```powershell
scoop install sudo
scoop install aria2
```

`aria2` 是下载加速用的 如果下载 `aria2` 后有下载问题 可以关掉试试 `scoop config aria2-enabled false`

### 添加 bucket

[介绍](https://sspai.com/post/52710)

查看官方维护仓库 : `scoop bucket known`

[社区第三方仓库](https://github.com/rasa/scoop-directory) 在线[网站](https://rasa.github.io/scoop-directory/)查询

安装官方库

```powershell
scoop bucket add extras
```

安装社区库

```
scoop bucket add dorado https://gitee.com/chawyehsu/dorado
scoop bucket add raresoft https://github.com/L-Trump/scoop-raresoft
```

### 卸载

删除bucket

```
scoop bucket rm raresoft
```

卸载软件

```
scoop uninstall __soft
```

卸载自己

```
scoop uninstall scoop
```

一些基本的参数

-g : 全局

-p : 移除配置文件

### 常见问题

unable to access `https://github.com/...`

这是 git 访问 GitHub 导致的问题 可以通过设置 git 代理解决

如在 `$profile` 文件中添加

```powershell
function start-proxy {
    git config --global http.proxy socks5://127.0.0.1:Port
    git config --global https.proxy socks5://127.0.0.1:Port
    echo "set git proxy"
}
function stop-proxy {
    git config --global --unset http.proxy
    git config --global --unset https.proxy
    echo "unset git proxy"
}
```
在使用命令前设置好git代理

### 参考链接

一些不错的文章

- https://www.iamzs.top/archives/scoop-guidebook.html
- https://sspai.com/post/65933
- https://sspai.com/post/52496

## [WinGet](https://docs.microsoft.com/zh-CN/windows/package-manager/winget/)

> winget 默认安装路径为 Program Files

### 下载

[Windows Store](https://www.microsoft.com/en-us/p/app-installer/9nblggh4nns1?activetab=pivot:overviewtab)下载 应用名为 App Installer

写此文时已有正式版

```powershell
 λ >  winget -v
v1.1.13405
```

### 命令

当前版本支持命令

- install
- show
- source : 管理包的源
- search
- list : 显示已安装的包
- upgrade
- uninstall
- hash
- validate
- settings
- features
- export
- import

```
 λ >  winget source list
Name    Argument
-----------------------------------------------------
msstore https://storeedgefd.dsx.mp.microsoft.com/v9.0
winget  https://winget.azureedge.net/cache
```

默认有MS Store和winget官方源

> `winget list` 很慢

## 原理

https://sspai.com/post/60592

