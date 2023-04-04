---
layout: search
headless: true
title:  "常用的Emacs快捷键"
categories: ["shortcut", "Linux"]
tags: ["develop"]
date: 2023-04-03T00:00:00+08:00
description: Emacs的一些基础快捷键 这些快捷键在受到了 GNU Readline 库的支持(所以在终端中可以使用)
---
Emacs的一些基础快捷键 这些快捷键在受到了 GNU Readline 库的支持(所以在终端中可以使用)

> `Tab`: 自动补全！

下面快捷键中 `C-a` 表示 Ctrl+a `M-a` 表示 Alt+a

## 移动快捷键

| 快捷键 | 作用             | 等价操作 |
| :---:  | ---              | -------- |
| `C-a`  | 移动到行首       | `Home`   |
| `C-e`  | 移动到行末       | `End`    |
| `C-b`  | 移动到前一个字符 | 左方向键 |
| `C-f`  | 移动到后一个字符 | 右方向键 |
| `C-p`  | 翻到上一条指令   | 上方向键 |
| `C-n`  | 翻到下一条指令   | 下方向键 |
| `M-b`  | 移动到上一个单词 | `C-左`   |
| `M-f`  | 移动到下一个单词 | `C-右`   |

## 删除与插入


| 快捷键 | 作用                         |
| :----: | --------------               |
| `C-k`  | 删除到行末(保存到剪切板)     |
| `C-u`  | 删除到行首(保存到剪切板)     |
| `C-y`  | 粘贴剪切板内容               |
| `M-d`  | 删除下一个单词               |

more: <https://en.wikipedia.org/wiki/GNU_Readline#Emacs_keyboard_shortcuts>
