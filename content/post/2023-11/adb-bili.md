---
title: "AdBili"
date: 2023-11-06T20:08:26+08:00
description: 基于 Bilibili 的音乐下载器方案
categories: ["misc"]
layout: search
tags: ["record"]
---

# AdBili

使用 adb 的基于 Bilibili 的音乐下载器方案

> 使用 Android10 及以下版本 可以直接 Termux 跑脚本

这里需要的一点前置知识:
- 对于Android基础目录结构的了解 知道怎么通过文件管理器找到不同软件非私有的数据 `/Android/data` 路径
- 大概知道adb是什么
- 知道手机怎么进入开发者模式

众所周知
1. B站是一个免费的UGC内容下载网站
2. B站的下载内容没有放入app 私有空间
3. B站现在的下载内容在存储时分为音频和视频

所以 现在有办法直接把B站当音乐下载器了

先简单一看 目录结构如下
- cache
- download
  - <avid>
    - <cid>
      - <video_quality>
        - audio.m4s <- 需要的音频文件
        - index.json
        - video.m4s
      - danmaku.xml
      - entry.json
- files

那么接下来的事情就简单了 找到下载的文件 然后重命名后复制到 Music 里

现在有两个方案
- 写 Shell 脚本 通过 `adb shell` 来执行脚本完成文件拷贝任务
- 写 Python 脚本 找找有没有 Python 的 adb 包来实现任务

现在 Google 官方库归档了 不过还有社区库 见这里: [JeffLIrion/adb_shell](https://github.com/JeffLIrion/adb_shell)

可用的Python代码见[此仓库](https://github.com/HUGHNew/adbili) 仓库还在更新中 后续会打包

## 注意事项

音频文件大小与视频清晰度正相关

某个视频的音频文件在不同清晰度下的文件大小
- 360P -> 617K
- 720P -> 2.23M