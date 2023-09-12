---
title: "Sudoer Tutorial"
date: 2023-09-12T19:58:22+08:00
categories: ["Linux", "operation", "introduction"]
layout: search
tags: ["develop"]
---

# 添加 sudo 权限

> 本文主要参考 [如何编辑sudoers文件][1]

让用户能够执行某些系统级别的操作或者命令最简单的方式就是把该用户添加到 `sudo` 组

但是可以有更细粒度的控制办法 那就是在 `/etc/sudoers` 文件中编辑权限

> 不要直接使用编辑器修改该文件 使用有权限的账户 `visudo`

```bash
# 如果希望使用指定的编辑器 有下面两种方式
# 修改 EDITOR 变量
EDITOR=$(which YOUR_WANTED_EDITOR) visudo

# 修改 editor 配置
sudo update-alternatives --config editor
visudo
```

## 了解 sudoer 文件

在 Debian 12 上 该文件的默认内容为

```conf
# /etc/sudoers without empty lines and comments
Defaults        env_reset # 重置终端环境 (删除用户变量)
Defaults        mail_badpass # 告诉系统将 sudo 密码错误尝试的通知 `mailto` 给配置的 mailto 用户 (一般是root 通过 `mail` 来查看邮件)
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" # 指定 sudo 指令的 PATH
Defaults        use_pty # 将命令置于伪终端(pseudo-terminal)执行 安全性更高
root    ALL=(ALL:ALL) ALL
%sudo   ALL=(ALL:ALL) ALL
@includedir /etc/sudoers.d
# 更多信息查看 `man 5 sudoers`
```

特权设置

```conf
root    ALL=(ALL:ALL) ALL
%sudo   ALL=(ALL:ALL) ALL
```
第一个字段表示用户或者用户组(以`%`开始)

**ALL** 的含义
1. 该规则适用于所有host
2. 可作为所有用户执行命令   使用 `sudo -u run_as_user command` 来指定命令执行用户
3. 可作为所有用户组执行命令 使用 `sudo -g run_as_group command` 来指定命令执行用户组
4. 该规则适用于所有命令

引入文件夹内所有文件 (不以 `~` 结束并且文件名不包含 `.` 的文件)

```
@includedir /etc/sudoers.d
```

如果编辑其他文件的话 使用 `visudo /etc/sudoers.d/new_config`

## 权限控制

最简单的办法就是把用户添加进 `sudo` 组 不过这样控制粒度太大了

还有另外细粒度的控制方法

```conf
%power ALL= /sbin/reboot, /sbin/shutdown
powerman ALL= NOPASSWD:/sbin/reboot, PASSWD:/usr/bin/systemctl disable, NOEXEC:/sbin/shutdown
```
上面更细粒度的控制修饰符
- PASSWD: 这是默认的行为 需要输入密码才能执行
- NOPASSWD: 不需要输入密码就能执行
- NOEXEC: 不允许执行该命令

## 别名

对于多用户或者多命令的管理 可以通过别名(alias)来增强文件的可读性

```conf
User_Alias GPO = albert, bob, carl
Runas_Alias WEB = www-data, apache
Cmnd_Alias POWER = /sbin/reboot, /sbin/shutdown
# 使用别名
GPO ALL = (WEB) POWER
```

[1]: https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file