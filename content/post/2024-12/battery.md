---
title: "Battery Capacity"
date: 2024-12-20T14:00:13+08:00
description: Laptap Battery Capacity Lookup
categories: ["introduction", "operation"]
layout: search
tags: ["develop"]
---

## Linux

`upower` 应该是桌面环境自带的工具

```bash
upower -i /org/freedesktop/UPower/devices/battery_BAT0
# upower --dump # 能获得更多设备的信息
```

## Windows

在Windows10及以上 按 Winx+x i 快捷键 可以直接打开 PowerShell

输入下面指令后 可以直接打开电池报告

```pwsh
powercfg /BatteryReport /Output battery.html; explorer battery.html
```

## macOS

Mac 的设置中有关于电源的信息

路径为: System Settings -> Battery -> Battery Health


具体可以看下面的链接

- [Apple Support](https://support.apple.com/en-hk/guide/mac-help/mh20865/mac)
- [MacPaw](https://macpaw.com/how-to/check-mac-battery-health)