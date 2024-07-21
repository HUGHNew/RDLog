---
title: "LVM Tutorial"
date: 2024-07-21T14:12:12+08:00
description: LVM(Logic Volumn Manager) tutorial
categories: ["Linux", "operation", "introduction", "LVM"]
layout: search
tags: ["develop"]
---

# Logic Volumn Manager

> LVM 是对**存储虚拟化**的技术

原始的磁盘利用方案(暂时不关RAID)为
- (分区) ~~不分区可能存在磁盘检测自动挂载出错的问题~~
- 文件系统格式化
- 挂载

主要的问题在于: 跨盘扩容

## terminology

![lvm-overview](images/lvm.png)

- PV(Physical Volume): 物理卷 处于LVM最底层 可以是物理硬盘或者分区
- VG(Volume Group): 卷组 一个到多个PV的集合 可以添加PV
- LV(Logical Volume): 逻辑卷 从VG中分配 相当于原来分区的概念 可以动态更新大小

## pre-LVM

`lsblk` 可以查看目前装上的磁盘

## basis

> 首先是下载 LVM 一般发行版都会自带 Debian系通过 `apt install lvm2` 下载和更新

相关命令的逻辑为 操作部分+具体操作 通用的操作有
- `display`
- `create`
- `remove` ***注意: 删除操作总是危险的 删除前确定自己知道会发生什么***
- `scan`
- `resize`

### PV

最基础的操作是创建和显示 PV
- `pvcreate /dev/sda` 将硬盘或者分区创建为物理卷
- `pvs`/`pvscan`/`pvdisplay` 这三者的功能一致 只是展示内容详细程度有区别

### VG

基础操作同上
- `vgcreate <VG_NAME> /dev/pv1 [/dev/sdb ...]` 用某些物理卷创建一个新的卷组
- `vgs`/`vgscan`/`vgdisplay`
- `vgextend <VG_NAME> /dev/sdc` 将新的PV加入到卷组

### LV

基础操作同上
- `lvcreate -L 100G -n <LV_NAME> <VG_NAME>` 从卷组创建逻辑卷
- `lvs`/`lvscan`/`lvdisplay`
- `lvextend --size 120G <LV_NAME>` 扩容逻辑卷

具体逻辑卷大小的设置可以查看 `tldr` 文档
- `lvcreate`
  - `-L 1T` 指定大小
  - `-l 60%VG` 按比例指定大小
- `lvextend`
  - `--size 200G` 指定拓展目标
  - `--size +40G` 指定拓展大小
  - `--size +20%FREE` 按比例指定拓展大小


创建逻辑卷之后 就是建立文件系统 可以选择喜欢的文件系统
- Btrfs: `mkfs.btrfs /dev/<VG_NAME>/<LV_NAME>`
- Ext4: `mkfs.ext4 /dev/<VG_NAME>/<LV_NAME>`

## operations

### 新增磁盘并拓展逻辑卷

例如新增磁盘 `/dev/sdf` 需要拓展的逻辑卷为 `/dev/svg/lvr`

我们的操作如下

```bash
# 忽略所有的 sudo
pvcreate /dev/sdf
vgextend svg /dev/sdf
lvextend --size +512G /dev/svg/lvr # 假设增加 512G
resize2fs /dev/svg/lvr # 自动热更新 Ext4 文件系统
df -h # 查看修改后的分区大小
```

### RAID

LVM 可以在逻辑卷(LV)层级创建软RAID (RAID级别见[此](https://hughnew.github.io/RDLog/post/2023-05/raid-tour/))

```
Create a raid LV (a specific raid level must be used, e.g. raid1).
lvcreate --type raid -L|--size Size[m|UNIT] VG
[ -l|--extents Number[PERCENT] ]
[ -i|--stripes Number ]
[ -m|--mirrors Number ]
[ COMMON_OPTIONS ]
[ PV ... ]
```

此外可以使用 `lvconvert` 对逻辑卷进行 RAID 级别转换
- linear -> raid1
- striped/raid0 -> raid4/5/6

`lvconvert --type RaidLevel LV [PVs]`

## post-LVM

`blkid` 可以查看分区的 UUID 方便修改 `/etc/fstab` 来实现自动挂载

可以看到在 `/dev/<VG_NAME>` 和 `/dev/mapper/` 路径下都能找到对应的逻辑卷 而且它们相同
```
/dev/debian-vg/:
Permissions Size User Date Modified Name
lrwxrwxrwx     7 root 19 Jul 15:15  root -> ../dm-0
lrwxrwxrwx     7 root 19 Jul 15:15  swap -> ../dm-1

/dev/mapper/:
Permissions   Size User Date Modified Name
crw-------  10,236 root 19 Jul 15:15  control
lrwxrwxrwx       7 root 19 Jul 15:15  debian--vg-root -> ../dm-0
lrwxrwxrwx       7 root 19 Jul 15:15  debian--vg-swap -> ../dm-1
```

## reference

[zh-lvm]: https://zhuanlan.zhihu.com/p/704221624
[lvm-aio]: https://henzelmoras.github.io/posts/linux-sys-admin/advanced-storage-managment/logical-volume-manager/
[lvm-raid]: https://manpages.ubuntu.com/manpages/bionic/man7/lvmraid.7.html
