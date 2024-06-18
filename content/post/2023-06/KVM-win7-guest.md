---
title: "KVM Win7 Guest"
description: KVM的Win7实操(不要折磨自己 还是用Win8.1+吧)
date: 2023-06-23T00:51:17+08:00
categories: ["Linux", "Windows", "introduction", "KVM"]
layout: search
tags: ["develop"]
---
# Why KVM

是 VMware Workstations 抬不动刀了还是 VirtualBox 闪到腰？ 为什么要选择 KVM 这种方式？

首先 VMware 挺好用的 不过对于 Win7 来说 需要打补丁 具体实践见[此](https://hughnew.github.io/feeds/blogs/Windows7-on-VMWare.html)

但是 VMware 的问题在于性能 在4核16G的条件下 Win7上只是运行一个输入法和微信就已经开始卡了

选择 KVM 主要是两个原因
- KVM属于与VMware ESXi 和 vSphere 同级别的***第1类***虚拟机监控程序 开销更小 性能更强
- KVM属于商用级别的**开源**方案 其功能受到Linux内核支持 在所有系统上通用

参考内容:
- <https://www.redhat.com/zh/topics/virtualization/what-is-a-virtual-machine>
- <https://www.redhat.com/zh/topics/virtualization/kvm-vs-vmware-comparison>

## KVM-Win7 尝试

KVM上面安装Win7主要有三个步骤
- 安装KVM
- 安装KVM Win7虚拟机并配置软件环境
- 配置Linux host与Win7 guest的共享

> 本文包含大量教程引用

## 安装

主要参考安装教程: <https://linux.cn/article-14661-1.html> ~~后面网络配置部分就不需要管了~~

Win7x64镜像可以通过 [Next, I tell you](https://next.itellyou.cn/) 进行下载 通过BT方式应该会快一点

> Win8.1 的官方镜像需要激活 需要重新打包

## 必备软件

- 微信 ~~没办法 你只能选择最新版本~~
- 搜狗输入法 ~~或者别的你喜欢的输入法~~ (Win10自带输入法)
- Yandex浏览器 ~~还有更小的吗？~~
- Office2016 ~~或者其他版本~~

## OpenGL

有些软件可能依赖于 OpenGL

安装过程如下(Win7可用性未知 Win10可用)
1. 下载[Mesa3D软件](https://github.com/pal1000/mesa-dist-win/releases)
2. 解压后执行`systemwidedeploy.cmd`脚本 并选择 `Core desktop OpenGL drivers`
3. 在[此处](https://www.geeks3d.com/dlz/) 找到并下载 GPU Caps Viewer用来验证
4. 下载后启动即可看见 OpenGL 版本

具体操作见回答 <https://askubuntu.com/a/1343984>

## 共享方案

### 共享文件夹

Win8以上方案: <https://www.debugpoint.com/kvm-share-folder-windows-guest/>

> virtio-win-guest-tools 只支持Win8以上系统

Win7选择 [WinSCP](https://winscp.net/eng/download.php) 或者 [LocalSend](https://github.com/localsend/localsend) ~~默认NAT网络测试没问题~~

### 共享剪切板

可以参考: <https://dausruddin.com/how-to-enable-clipboard-and-folder-sharing-in-qemu-kvm-on-windows-guest/#Solution_Clipboard_sharing>

设置之后可以共享剪切板(文本和截图)

### GPU passthrough

默认没有显卡(系统内看不到核显)

如果需要玩游戏 需要使用显卡透传

建议参考文章:
- 命令行操作: <https://github.com/lateralblast/kvm-nvidia-passthrough>
- 图形化操作: <https://juejin.cn/post/7091905870312767495>