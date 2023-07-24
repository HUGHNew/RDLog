---
title: "Windows 设置默认路径的显示"
date: 2023-07-24T20:10:42+08:00
categories: ["misc"]
layout: search
tags: ["record"]
---

## 意外

Windows Explorer 上的目录本来都是很正常得显示中文 直到我下载了迅雷 于是它变成了这样

![after-thunder](images/windows-path/mixture.png)

从“下载”变成了“Downloads” 要都是英文或者中文也就无所谓 反正是协调的 但是一个突兀的 “Downloads” 就显得很难看了

经过简单的搜索 从[这里][desktop-ini]发现控制这些默认路径名显示的是路径下的`desktop.ini`文件 不过这个文件是隐藏的

于是进入 Downloads 路径下查看该文件 于是发现

![after-thunder](images/windows-path/thunder-download.png)

果然是迅雷搞的

本来想直接改了或者删了了事 结果提醒我没有权限 于是去看了一下原文件的属性

> 在文件管理器中的 查看(顶上) -> 选项(最右边位置) -> 查看 -> 取消勾选"隐藏受保护的操作系统文件" 如下图 然后点击应用

![show desktop.ini](images/windows-path/show-hidden-files.png)

发现迅雷还把文件设置为了只读

## 修复

从[这篇博客][desktop-ini]可以知道 “下载” 路径下正常的内容应该是

```ini
[.ShellClassInfo]
LocalizedResourceName=@%SystemRoot%\system32\shell32.dll,-21798
IconResource=%SystemRoot%\system32\imageres.dll,-184
```

指示显示本地化名称的是第二行的内容 将其删除或者注释掉的话 就会显示英文路径名

```ini
; 这是注释的效果
[.ShellClassInfo]
;LocalizedResourceName=@%SystemRoot%\system32\shell32.dll,-21798
IconResource=%SystemRoot%\system32\imageres.dll,-184
```

修改完之后保存 然后重启文件管理器 就能看见更改的效果了

当在“视频”“图片”等多个文件夹下修改之后 效果如下图
![current-explorer](images/windows-path/current.png)

[desktop-ini]: https://p3terx.com/archives/windows-system-default-folder-name-changed-to-english-solution.html
[localization]: https://superuser.com/questions/788555/is-there-a-way-to-disable-localizedresourcename-desktop-ini-globally
[windows-doc]:  https://learn.microsoft.com/en-us/windows/win32/shell/how-to-customize-folders-with-desktop-ini