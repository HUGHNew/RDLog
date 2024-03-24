---
title: "Win10(KVM) as Server"
date: 2024-03-24T15:54:37+08:00
description: Quick tour to make Windows in KVM run as a server
categories: ["Windows",  "introduction", "operation"]
layout: search
tags: ["develop"]
---

# Windows configure

1. 安装 KVM(host)
2. 安装 Windows(guest)
3. 配置 Windows(guest)
   1. 安装 openssh-server(guest)
   2. [opt]配置 PowerShell
   3. [opt]配置 Vim
   4. [opt]配置 WinGet
4. 配置端口转发(host)
5. 开放对应端口(guest)

## KVM installation

这部分不多做描述 主要就三点
1. KVM 仅用于 Linux 且需要BIOS打开虚拟化设置
2. 使用 KVM 原因可见[此处][why-kvm]
3. KVM 可以直接通过发行版的包管理进行一键式安装(如[Debian][kvm-install]) 桌面版多装一个`virt-manage`进行图形化操作

## Windows installation

镜像从 MSDN 或者 [MSDN, I tell you](https://msdn.itellyou.cn/)/[NEXT, I tell you](https://next.itellyou.cn/) 下一个最新的 Win10 镜像就好

~~或者试试[AtlasOS][atlas] 或者 [Tiny10][tiny10]~~

## Softwares for Windows

如果可以图形化远控就用远控软件好了 然后接下来跳到下一部分了

使用命令行的话
1. SSH: 这个很重要就没什么好说的了
2. PowerShell: 适当配置一下以增强使用体验
3. Vim: 命令行总得有一个命令行编辑器吧
4. WinGet: 网好的话可以用来下载 Vim 等工具

### SSH

看[官方教程][sshd]就好 支持PowerShell操作 可以脚本化

Windows 的 sshd 进来默认是管理员的cmd 可以修改登陆Shell 查看[此处][pwsh-in-ssh]

> Windows openssh-client 的反向端口转发在处理非22端口时有问题 (WSL与Cygwin正常)

### PowerShell

详细的 PowerShell 配置与体验优化见[此处][pwsh-conf]

Win10自带的 PowerShell 版本为 5.1 基本可用 一般是建议安装一个 `PSReadline` 模块来保证与 bash 相似的体验

```powershell
# 修改策略 保证能执行本地脚本 profile.ps1 <----> 与 .bashrc 作用类似
Set-ExecutionPolicy RemoteSigned

Install-Module -Name PSReadLine
# Install-Module -Name PSReadLine -Scope User
```

下面是 profile.ps1 文件的一些基础配置 主要是 Emacs 模式与 上下键查询历史
```powershell
# $HOME/Document/WindowsPowerShell/profile.ps1
Import-Module PSReadLine # Install-Module -Name PSReadLine

#-------------------------------  Set Hot-keys BEGIN
Set-PSReadlineKeyHandler -Key Tab -Function Complete
Set-PSReadLineOption -HistorySearchCursorMovesToEnd
Set-PSReadLineOption -EditMode Emacs
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
#-------------------------------  Set Hot-keys END
```

### Vim

Vim 可以从官网下 也可以通过 WinGet 下载

官网下载 手动安装后还需要配置环境变量 比较简单的方法就是在 profile.ps1 里面添加路径

比如安装的Vim9.1默认路径在 `${Env:ProgramFiles}/Vim/vim91`

```powershell
$Env:Path += ";${Env:ProgramFiles}/Vim/vim91"
```

### WinGet

老实说 国内一般环境下 `winget source update` 会因为网络原因中断 除非链路上配置了代理 不然没办法使用

一般配置一下手动更新就好了 更多设置点击[此处][winget-settings]

```powershell
$settingsContent = @'
{
  "$schema": "https://aka.ms/winget-settings.schema.json",
  "logging": {
    "level": "verbose"
  },
  "source": {
    "autoUpdateIntervalInMinutes": 0
  },
}
'@
$settingsContent | Out-File (Join-Path $env:LOCALAPPDATA 'Packages\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe\LocalState\settings.json') -Encoding ASCII
```

## Port forwarding

这个问题是使用默认NAT网络导致的 可以通过改用bridge网络来解决

不改的话也可使用其他端口转发方法 反正 **虚拟机NAT是可以正常访问主机的**

只是看起来端口转发会更稳定快速一些

具体操作可以使用 libvirt 的[hook方案][nat-forward]

## Firewall allow

最后一步就是在虚拟机中打开防火墙 放行所需端口

这条命令参考自 [SSH 配置][firewall]

```powershell
New-NetFirewallRule -Name '__storage_rule_name__' -DisplayName '__display_rule_name__' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort <Port> # port: 22 or 11451-11454
```

## Access Test

```bash
ssh __user__@GUEST_IP

curl GUEST_IP:GUEST_PORT/
```

[why-kvm]: https://hughnew.github.io/RDLog/post/2023-06/kvm-win7-guest
[kvm-install]: https://wiki.debian.org/KVM#Installation
[tiny10]: https://ntdev.blog/2024/01/08/the-complete-tiny10-and-tiny11-list/
[atlas]: https://docs.atlasos.net/getting-started/installation/
[opt-shared]: https://hughnew.github.io/RDLog/post/2023-06/kvm-win7-guest/#%E5%85%B1%E4%BA%AB%E6%96%B9%E6%A1%88
[winget-settings]: https://github.com/microsoft/winget-cli/blob/master/doc/Settings.md#source
[pwsh-conf]: https://hughnew.github.io/feeds/blogs/Friendly-PowerShell.html
[nat-forward]: https://wiki.libvirt.org/Networking.html#nat-forwarding-aka-virtual-networks
[sshd]: https://learn.microsoft.com/zh-cn/windows-server/administration/openssh/openssh_install_firstuse?tabs=gui
[firewall]: https://learn.microsoft.com/zh-cn/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell#install-openssh-for-windows
[pwsh-in-ssh]: https://learn.microsoft.com/zh-cn/windows-server/administration/openssh/openssh_server_configuration#configuring-the-default-shell-for-openssh-in-windows

