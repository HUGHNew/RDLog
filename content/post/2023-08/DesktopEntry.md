---
title: "DesktopEntry"
description: (为你下载的二进制或者脚本)手动添加 Linux 桌面图标
date: 2023-08-18T14:26:21+08:00
categories: ["Linux", "GNOME", "introduction", "desktop"]
layout: search
tags: ["develop"]
---

主题内容参考[这里](https://hughnew.github.io/feeds/blogs/Desktop-Entry-in-Gnome.html)

本文主要补充的内容是相同配置在于不同系统下失效的问题

这是一个简单的 QQ desktop 文件

`qq` 是下载的 AppImage 版本 之前的路径是在 `~/.local/bin` 现在在 `~/.local/app`

```ini
[Desktop Entry]
Name=Linux QQ
Comment=Electron QQ
Exec=qq
Icon=/home/$USER/Pictures/AppImageIcons/qq.png
Version=1.0
Type=Application
Categories=Office;
Terminal=false
```

这个配置文件格式没有问题 即 `desktop-file-validate qq.desktop` 是正常的 但是无法添加到系统条目中

后来通过在桌面路径手动尝试添加条目发现 DE无法找到 `qq` 的路径

于是猜测 `~/.local/bin` 是DE的默认PATH的一部分 但DE不会获取用户的PATH变量 所以改写执行路径为完整路径 问题解决

```ini
[Desktop Entry]
Name=Linux QQ
Comment=Electron QQ
Exec=/home/$USER/.local/app/qq
Icon=/home/$USER/Pictures/AppImageIcons/qq.png
Version=1.0
Type=Application
Categories=Office;
Terminal=false
```
