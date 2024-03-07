---
title: "Disk4Server"
description: 简单的服务器分区方案
date: 2023-10-25T14:18:06+08:00
categories: ["Linux",  "introduction", "operation"]
layout: search
tags: ["develop"]
---

# Disk Partition

> **EFI 需要在磁盘分区**(例如/dev/sda1) 在LVM中设置的话 可能需要将该LVM盘设置为boot盘

为了实现各个分区的拓展所有分区的都基于 **LVM** (不考虑 **Btrfs** 的情况下)

基于逻辑分区/分卷的好处在于 加盘的时候方便很多

基于 LVM 的软 RAID 根据实际的硬盘情况和需求进行配置

一个用于深度学习的服务器根据磁盘占用情况可以分为如下几块

| mount | usage | content | disk |
| :---: | ----- | ------- | :--: |
| /     | 系统根路径 | 包含 /boot /usr /etc 等系统必要的文件和系统工具 | ~256GB |
| /home | 用户家目录 | 主要内存占用在于 `.cache` `.local` 可以将资源通过软链接方式拉回到家目录 但所有的资源应该在 /data 下面 | 512GB-1T |
| /data/tool/ | 用户环境路径 | conda 环境与 docker 镜像  | 512GB-1T |
| /data/code/ | 用户代码数据路径 | 可以在该部分进行进一步划分 | ? |

初始分区挂载方式需要重点考虑物理磁盘数量 避免多个分区同时分散在多块磁盘

/data 挂载树状图 挂载点已加粗
- /data
  - **/tool**:
    - /conda
      - 不建议使用 shared-conda 可能在安装包时会有冲突
      - 另外 conda envs_dir 配置有问题 可能会导致 环境在 `~/.conda` 内
    - /docker
      - 定义 docker/daemon.json 里面的 `data-root` 值 [详细步骤](https://tienbm90.medium.com/how-to-change-docker-root-data-directory-89a39be1a70b)
  - **/code**: 
    - /for-each-user
    - /share 如果共享资源较多的话 也可以考虑设置独立挂载点
      - /binary
      - /model
      - /dataset
