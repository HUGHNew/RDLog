---
title: "Shared Conda"
description: 设置共享conda环境(不推荐)
date: 2023-07-30T20:41:42+08:00
categories: ["Linux", "operation", "introduction"]
layout: search
tags: ["develop"]
---

安装共享的conda并使用共享的conda环境(readonly) **该操作需要`sudo`权限**

> 只有一个好处: **减少磁盘消耗**

## 安装

下载`miniconda` 可以直接下载最新版本或者去官网选择需要的版本

```bash
# 下载最新版本
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# 安装conda
sudo bash Miniconda3-latest-Linux-x86_64.sh
# 在交互界面选择在公共路径下安装 conda 如 /opt/miniconda
# 下文用 __installation_location__ 来表示安装路径
```

安装完之后复制 `conda init` 部分的命令到 `.bashrc` 或者 `.zshrc` 中

## 多用户设置

设置多用户的conda环境可见[官方文档][miniconda-installation] 下方命令取自文档

```bash
# Create a new group 创建新的用户组来授权 conda 路径
sudo group add miniconda
# Change the group ownership to "miniconda" on the entire directory where CONDA is installed. Replace __installation_location__ with the actual path to your installed CONDA file. 将安装路径的组所有者改为新建的用户组
sudo chgrp -R miniconda __installation_location__
# Set read and write permission for the owner, root, and the miniconda only. Replace __installation_location__ with the actual path to your installed CONDA file. 修改安装路径的文件权限 允许所在组的用户使用
sudo chmod 770 -R __installation_location__
# Add (existing) users to a group. Replace USERNAME with the username of the user you are adding. 将使用 conda 的用户添加到组内
sudo adduser username miniconda
```

通过上方的命令 可以是所有人都可以使用 conda 命令

一般还会设置 conda 的镜像站以及其他内容 可以参考[下面配置][condarc-base]

```yaml
# __installation_location__/.condarc
auto_activate_base: false
channels:
  - https://mirrors.ustc.edu.cn/CONDA/cloud/conda-forge/
  - https://mirrors.ustc.edu.cn/CONDA/pkgs/main/
  - https://mirrors.ustc.edu.cn/CONDA/pkgs/free/
  - defaults
show_channel_urls: true
auto_stack: 0
pip_interop_enabled: true
auto_update_conda: false
envs_dirs:
  - __installation_location__/envs
pkgs_dirs:
  - __installation_location__/pkgs
```

其中比较重要的设置为 `envs_dirs` `pkgs_dirs` 这两项设置指定了[默认的 conda 环境下载位置][env-location]

另外如果需要手动指定环境位置 可以使用 `conda create --prefix __installation_location__/envs/__env_name__ python=3.10.9` 更多内容可参考[该博客][shared-conda-env]

## 权限问题

虽然安装路径的权限用户组内的用户都可以读写 但是用户的安装路径默认为`644` 其他用户可以读取 但是不能写入 可以手动 `chmod -R 777` 进行共享

[condarc-base]: https://github.com/HUGHNew/dotfiles/blob/mint/condarc
[miniconda-installation]: https://docs.CONDA.com/free/CONDA/install/multi-user/#multi-user-CONDA-installation-on-linux
[env-location]: https://conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html#specify-environment-directories-envs-dirs
[shared-conda-env]: https://rcpedia.stanford.edu/topicGuides/sharedCondaEnv.html