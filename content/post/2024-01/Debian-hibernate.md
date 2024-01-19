---
title: "Debian Hibernate"
date: 2024-01-19T20:09:38+08:00
description: Debian bookworm enable hibernate
categories: ["Linux", "operation"]
layout: search
tags: ["develop"]
---

# Debian 启用休眠功能

> 主要是方便双系统切换

睡眠: sleep/suspend 关闭显示器 进入低功耗模式

休眠: hibernate 将内存放入磁盘进行持久化 功耗更低 行为接近于关机

休眠命令: `systemctl hibernate`

> XFS 文件系统不能缩减

## 文件系统缩减

> ***数据无价 请先备份***

`systemD` 下的休眠需要 swap 空间大于 memory 不然会报错

所以需要一个比内存更大的 swap 分区

> 理论上 swap file 也是可行的 参考 [Debian-Wiki][swap-file] ~~但我没成功~~


这里缩减分区有多种情况
1. 有除了根分区以外的分区可以用来缩减
2. 只有根分区可以缩减
   1. 根分区使用LVM
   2. 根分区直接使用文件系统(如ext4等)

很多文件系统都是不支持在线缩减的 所以缩减前需要 `umount`

第一种情况很好处理 `umount` 分区之后 使用文件系统对应的工具进行缩减就行

```bash
# 例如设备为 /dev/sdb1
umount /dev/sdb1
# 对于 ext* 使用 resize2fs 缩减到 100G
resize2fs -p /dev/sdb1 100G
# -p 表示显示进度条
```

或者使用 GParted 进行图形化操作

### 根分区缩减

对根分区操作需要使用 LiveUSB

如果根分区直接使用 ext4 等文件系统 方法同上

如果根分区使用的 LVM 那么需要使用 [`lvreduce`][tutorial] 先对逻辑卷进行缩减 再压缩文件系统

> 操作详见[此处][lvreduce]

```bash
# 查看当前的逻辑卷
sudo lvs
# 缩减根分区 50G 同时处理实际的文件系统 (等同于之后的两条命令)
sudo lvreduce --resizefs --size -50G /dev/YOUR_VG/root
# sudo lvreduce --size -50G /dev/YOUR_VG/root
# resizefs /dev/YOUR_VG/root TARGET_SIZE
```

## 创建 swap

直接使用文件系统的话 可以通过 `fdisk` 或者 GParted 来创建新的分区

LVM 可以通过 `lvcreate YOUR_VG -n swap -L SIZE` 来创建一个名位 swap 的新逻辑卷分区

```bash
mkswap /dev/to/YOUR_PARTITION # 创建 swap 分区
echo "/dev/to/YOUR_PARTITION\tswap\tswap\tdefaults\t0\t0" >> /etc/fstab # 自动挂载
```

## 更新系统设置

根据 [Wiki][wiki] 的说明 进行最后的配置

```bash
sysctl -w vm.swappiness=1 # 让系统尽量不使用 swap 除非内存几乎耗尽 swappiness in [0,99]
echo "RESUME=/dev/to/YOUR_PARTITION" > /etc/initramfs-tools/conf.d/resume # 写入休眠恢复设置
update-initramfs -u # 更新 initramfs
```

好了 现在就可以开心的 `systemctl hibernate` 了

[swap-file]: https://wiki.debian.org/Hibernation/Hibernate_Without_Swap_Partition
[wiki]: https://wiki.debian.org/Hibernation
[lvreduce]: https://askubuntu.com/questions/124465/how-do-i-shrink-the-root-logical-volume-lv-on-lvm
[tutorial]: https://zhuanlan.zhihu.com/p/267497502