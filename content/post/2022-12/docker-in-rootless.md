---
layout: search
headless: true
title:  "rootless docker"
categories: ["linux", "container"]
tags: ["develop"]
date: 2023-02-08T00:00:00+08:00
description: 概括性介绍docker的安装以及rootless docker的使用和镜像文件的迁移
---
概括性介绍docker的安装以及rootless docker的使用和镜像文件的迁移

## Installation

官方文档 [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

官方脚本一键化操作 **(推荐)**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
# sudo sh ./get-docker.sh --dry-run # 只是看看将执行的操作
```

手动操作和官方脚本的大致逻辑
1. 卸载系统自带的老旧版本(如果有)
2. 下载必要工具(如gnupg等)
3. 添加docker gpg公钥
4. 添加docker源
5. 下载docker

## Rootless docker

[官方文档](https://docs.docker.com/engine/security/rootless/)

先暂停 docker: `sudo systemctl disable --now docker.service docker.socket`

```bash
/usr/bin/dockerd-rootless-setuptool.sh install # 安装 rootless docker
# 如果这个文件找不到的话 apt install docker-ce-rootless-extras

# 设置必要的值
export DOCKER_HOST=unix:///run/user/$(id -u)/docker.sock # 这行代码顺便放入 .bashrc 中
# 设置开机自启
systemctl --user enable docker
sudo loginctl enable-linger $(whoami)

# 手动启动 docker
systemctl --user start docker

# 之后就正常使用了
```

Ubuntu 可能会缺少 `uidmap` 使用`sudo apt install uidmap`就好

## Migrate to rootless

不过从 root 的 docker 切换到 rootless 的 docker 后 镜像(images)是不会共享的

因为不同模式下 docker 的文件读取和存储路径不同

```shell
$ docker info
...
Docker Root Dir: ~/.local/share/docker
...

$ sudo docker info
...
Docker Root Dir: /var/lib/docker
...
```

同步镜像 `sudo rsync -aqx --chown=$(whoami) /var/lib/docker/ ~/.local/share/docker/`
> `--chown=user[:group]`是用来改同步后文件的权限的

> 也可以直接 `mv` 或者 `cp`

如果同步前 rootless docker 服务正在运行的话 重启一下(`systemctl --user restart docker`) 就可以看见同步过来的镜像了