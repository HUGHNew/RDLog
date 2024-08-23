---
title: "Linux Search"
date: 2022-07-27T21:57:59+08:00
description: Linux search command
categories: ["Linux", "operation"]
layout: search
tags: ["develop"]
---

# Linux 查找指令

| command  | `which`<br/>(builtin)    | `where`<br/>(builtin)              | `whereis`              | `whatis`              | `locate`<br/>需要下载               | `find`       |
| -------- | ------------------------ | ---------------------------------- | ---------------------- | --------------------- | ----------------------------------- | ------------ |
| 查询域   | 用户`PATH`               | `PATH`/alias/builtin               | binary/source/man      | man                   | 自建的索引                          | 整个文件系统 |
| 数据更新 |                          |                                    |                        |                       | 使用find定期更新/`updatedb`强制更新 |              |
| 结果     | 显示第一个(`-a`显示所有) | 显示所有查找结果(与`which -a`相似) | (可以通过参数设定类型) | 显示man手册的一行描述 |                                     |              |




## which/where

> 在用户的 `PATH` 中寻找 但其实跟`where`查找范围一样

````bash
$ which ls
ls: aliased to ls --color=auto
$ which -a ls
ls: aliased to ls --color=auto
/usr/bin/ls
/bin/ls
$ which where
where: shell built-in command

# where
$ where ls
ls: aliased to ls --color=auto
/usr/bin/ls
/bin/ls
````

## whereis

> 默认查找binary(`-b`) source(`-s`)和man pages(`-m`)

```bash
$ whereis ls
ls: /usr/bin/ls /usr/share/man/man1/ls.1.gz
$ whereis -b ls
ls: /usr/bin/ls
```

## whatis

> 显示man手册的一行描述

```bash
$ whatis whatis
whatis (1)           - display one-line manual pag...

# 显示完整的不受终端宽度影响的一行
$ whatis --long whatis
whatis (1)           - display one-line manual page descriptions
```

## find

> 文件系统查找文件

```bash
$ find /usr/bin -name ls
/usr/bin/ls
$ find /usr/bin -type f -name ls
/usr/bin/ls
```

`tldr` 描述

```
find
Find files or directories under the given directory tree, recursively.More information: https://manned.org/find.

 - Find files by extension:
   find {{root_path}} -name '{{*.ext}}'

 - Find files matching multiple path/name patterns:
   find {{root_path}} -path '{{**/path/**/*.ext}}' -or -name '{{*pattern*}}'

 - Find directories matching a given name, in case-insensitive mode:
   find {{root_path}} -type d -iname '{{*lib*}}'

 - Find files matching a given pattern, excluding specific paths:
   find {{root_path}} -name '{{*.py}}' -not -path '{{*/site-packages/*}}'

 - Find files matching a given size range:
   find {{root_path}} -size {{+500k}} -size {{-10M}}

 - Run a command for each file (use {} within the command to access the filename):
   find {{root_path}} -name '{{*.ext}}' -exec {{wc -l {} }}\;

 - Find files modified in the last 7 days and delete them:
   find {{root_path}} -daystart -mtime -{{7}} -delete

 - Find empty (0 byte) files and delete them:
   find {{root_path}} -type {{f}} -empty -delete
```

