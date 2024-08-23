---
title: "Pretty Powershell"
date: 2022-02-25T22:02:50+08:00
description: 更实用的 PowerShell
categories: ["Windows", "operation"]
layout: search
tags: ["develop"]
---

# Windows如何获得好用的PowerShell

> 下述所有安装步骤速度视网络环境~~和代理情况~~而定

准备
1. Microsoft Store 下载 `Windows Terminal` 或者 `winget install --id Microsoft.WindowsTerminal`
2. 下载并安装 [PowerShell7](https://docs.microsoft.com/zh-cn/powershell/scripting/install/installing-powershell-on-windows?WT.mc_id=THOMASMAURER-blog-thmaure&view=powershell-7.2#msi)
3. 安装一个更友好的字体 比如 [FiraCode Nerd Font](https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/FiraCode.zip) 也可以选择其你喜欢的支持Unicode的字体<https://www.nerdfonts.com/font-downloads>
4. 在 Windows Terminal 中使用该字体

## 安装组件

在 PowerShell7 中逐行输入

```powershell
Install-Module -Name PSReadLine  -Scope CurrentUser
Install-Module oh-my-posh -Scope CurrentUser
```

[oh-my-posh](https://ohmyposh.dev/)官网 可获取详细配置信息

## 添加设置

在 PowerShell7 中编辑 `$profile`

```powershell
# 先修改执行权限再编辑内容
Set-ExecutionPolicy RemoteSigned
notepad $profile
```

使用任何你喜欢的编辑器都行

```powershell
#------------------------   Import BEGIN    ---------------------------#
Import-Module PSReadLine
Import-Module oh-my-posh

Set-PoshPrompt -Theme schema
# -Theme 后面的参数表示主题名
#------------------------   Import END    -----------------------------#
#------------------------   Hot-Keys BEGIN    -------------------------#
# 设置预测文本来源为历史记录
Set-PSReadLineOption -PredictionSource History

# 每次回溯输入历史，光标定位于输入内容末尾
Set-PSReadLineOption -HistorySearchCursorMovesToEnd

# 设置 Tab 为菜单补全和 Intellisense
Set-PSReadLineKeyHandler -Key "Tab" -Function MenuComplete

# 设置 Ctrl+z 为撤销
Set-PSReadLineKeyHandler -Key "Ctrl+z" -Function Undo

# 设置向上键为后向搜索历史记录
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward

# 设置向下键为前向搜索历史纪录
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
#------------------------   Hot-Keys END    ---------------------------#
```


### 添加新主题

在 PowerShell7 中输入下列命令可以查看现有主题

```powershell
Get-PoshThemes
```

主题显示完之后 你会看见主题的保存路径 一般是 Documents/PowerShell/Modules/oh-my-posh/themes
![themes-path](images/pretty-pwsh.png)

可以通过修改一个现有的主题或者新建一个主题文件来自定义 Prompt(命令行提示符) 样式

文件的默认后缀是 .omp.json 格式为 json

## 参考

- https://github.com/HUGHNew/Posh-Prompt/
- https://zhuanlan.zhihu.com/p/137595941 这里的第5、6步可以不管