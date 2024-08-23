---
title: "Adb Quickview"
date: 2022-08-04T21:53:42+08:00
description: 速通 ADB
categories: ["Linux", "operation", "Android"]
layout: search
tags: ["develop"]
---

# adb QuickView

> Android Debug Bridge  
> Android 交互的命令行工具 (C/S)

使用大全:[awesome-adb](https://github.com/mzlogin/awesome-adb)

adb 命令会从命令行调用客户端

服务器/adbd(daemon) 在**移动设备**上

## Installation

有两种安装方式
1. 通过 Android Studio 下载 Android SDK 后 `~/Library/Android/sdk/platform-tools/` 路径下 会有 adb 等工具 然后 `ln -s ~/Library/Android/sdk/platform-tools/adb /usr/bin/adb` 就可以使用 adb 了
2. 自行下载
   1. 在[此处](https://developer.android.com/studio/releases/platform-tools?hl=zh-cn)手动下载
   2. 使用系统包管理器下载
      1. Windows - winget
      2. macOS - homebrew
      3. Debian/Ubuntu - apt
      4. ...

**adb client/server 版本不匹配** 都可以控制客户端版本去解决问题 使用第一种方法也许能更好避免该问题的发生

## adb common

> `-s deviceId` 指定设备

- local: client
- remote: server

| category | cmd | example |
| :------: | :-: | ------- |
| package | install | `adb install /path/to/apk` |
|  | uninstall | `adb uninstall appId` |
| log | logcat | `adb logcat` |
| server | start-server | |
|  | stop-server | |
|  | devices | `adb devices [-a]` |
| files transfer | push | `adb push local remote`<br/>`adb push foo.txt /sdcard/foo.txt` |
|  | pull | `adb pull remote local` |
| port forward | forward | `adb forward tcp:6100 local:logd` |



## adb shell

执行设备上的 (remote)shell

> `adb shell` 单独使用即是进入 remote shell  
> 和其他子命令一起使用是 使用 shell 执行命令并退出

- [am][1] : activity manager
- [pm][2] : package manager
- screencap: `screencap /remote/path/to/save.png`
- screenrecord: `screenrecord /remote/path/to/save.mp4` ~~(无法同时录制音频和视频)~~
- sqlite3


### am

- start/startservice/broadcast *intent*
- force-stop/kill package
- kill-all

### intent usage

> `adb shell am start -a android.intent.action.VIEW`

| type | value | example |
| :--: | ----- | ------- |
| `-a` | **action** | android.intent.action.VIEW |
| `-d` | **data_uri** | |
| `-t` | **mime_type** | image/png |
| `-c` | **category** | android.intent.category.APP_CONTACTS |
| `-n` | **component** | com.example.app/.MainActivity |

### pm

主要命令
- list
  - packages [*filter*]
    - `-d`：进行过滤以仅显示已停用的软件包
    - `-e`：进行过滤以仅显示已启用的软件包
    - `-s`：进行过滤以仅显示系统软件包
    - `-3`：进行过滤以仅显示第三方软件包
    - `-i`：查看软件包的安装程序
    - `-u`：也包括已卸载的软件包
  - permissions/permission-groups
  - features
  - libraries
  - users
- install/uninstall
- enable/disable 启用/停用 软件包或组件
- `grant/revoke package permission`
- `path package` 包的APK路径

[1]: https://developer.android.com/studio/command-line/adb?hl=zh-cn#am
[2]: https://developer.android.com/studio/command-line/adb?hl=zh-cn#pm