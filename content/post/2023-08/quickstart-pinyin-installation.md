---
title: "Quickstart Pinyin Installation"
date: 2023-08-18T16:00:53+08:00
categories: ["Linux", "GNOME", "introduction", "IME", "tool"]
layout: search
tags: ["develop"]
---

一个一般的桌面环境一般都会有一个输入法框架/平台 iBus/Fcitx

Ubuntu LTS 的 Gnome 默认是 iBus 我装过iBus-Rime 然后慢慢配置

Linux Mint 的 Cinnamon 默认是 Fcitx 安装搜狗也得弄半天

现在发现最快捷的使用中文的方式是直接安装智能拼音

```sh
sudo apt install ibus-libpinyin
sudo apt install fcitx-libpinyin
```

安装之后 即可在输入法设置界面选择中文了

![lib-pinyin](images/IME/ibus.png)