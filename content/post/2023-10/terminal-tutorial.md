---
title: "Terminal Tutorial"
description: 选择你的Terminal 并开启你的Shell旅程
date: 2023-10-03T20:21:58+08:00
categories: ["Linux",  "introduction", "terminal"]
layout: search
tags: ["develop"]
---

# 一切的开始

开天之际 一切都有实体
- Terminal
- Console
- TTY(TeleTYper)
上述三者 都有对应的物理存在的设备

世界发展 虚实转换 原来的设备集成为一 只留下了名字
- TTY(Text Terminal)
- Pseudo TTY/PTS(一个登陆Shell对应一个pts设备)
- Terminal Emulator

参考链接:
- <https://www.zhihu.com/question/65280843/answer/420064483>
- <https://thevaluable.dev/guide-terminal-shell-console>
- <https://www.baeldung.com/linux/pty-vs-tty>

但 Shell 一直是一个概念/软件 是介于硬件和终端的中间层 用户与系统/硬件交互的工具

现在主要的一些Shell有
- sh: ~~与世长存~~
- ash: Alpine甄选
- bash: 经典之作
- pwsh(PowerShell): 巨硬(!POSIX)
- fish
- zsh
- xonsh: 不能设置为默认shell

## 伪终端

GNOME 有默认的 gnome-terminal KDE 有默认的 Konsole

但是不如试试新鲜玩意儿
1. [Terminator][tt] 单页多开 不用切换tab

![Term-multi](https://gnome-terminator.org/assets/images/terminator-light-man-asquiiquarium.png)

2. [Cool-Retro-Term][retro] 阴极管风格 给你不一样的体验

![Retro-Term](https://camo.githubusercontent.com/26bae23283b3b91bf2409aae0de2a032408a50e97ca79aa62513b471626b5c3b/68747470733a2f2f692e696d6775722e636f6d2f544e756d6b446e2e706e67)

## CLI travel

- MacBook Air/Pro 没有 Home/End/Delete 怎么办?
- Shell 里面想删一两个词怎么办?

看看下面的Emacs快捷键就好了 居家出行 上工摸鱼 全解决

| 修饰键 | 其他键 | 作用 |
| :---: | :---: | --- |
| Ctrl  | A | 移动到行首 |
| | E | 移动到行末 |
| |  U | 删除到行首 |
| |  K | 删除到行末 |
| |  W | 向前删除一个单词 |
| |  D | 向后删除一个字符 |
| Alt | B | 向后(back)移动一个单词 |
| | F | 向前(forward)移动一个单词 |
| | D | 向后删除一个单词 |

[retro]: https://github.com/Swordfish90/cool-retro-term
[tt]: https://github.com/gnome-terminator/terminator