---
layout: search
headless: true
title:  "Linux Redirection"
categories: ["shell", "linux"]
tags: ["develop"]
date: 2022-11-23T00:00:00+08:00
description: 主要讲解重定向以及`-`和`--`在命令行中作为独自字段的使用
---
这里主要讲解重定向以及`-`和`--`在命令行中作为独自字段的使用

重定向和管道是 `*nix` 很使用的特性 其中管道比较简单 主要是匿名管道和具名管道两种 ~~从感觉上讲 也是重定向的一种应用~~

## pipe

```bash
#### unnamed pipe ####
cat /etc/passwd|grep root # 找到 root 的密码信息

####  named pipe  ####
mkfifo test.pipe # 创建一个 管道 文件
# no.1 terminal
echo hello > test.pipe
# no.2 terminal
cat test.pipe
```

## redirection

重定向三种简单的用法

```bash
# 重定向标准输出
cal > this_month # 将本月的日历输入到 this_month 文件(会覆盖原有内容)
cal >> months # 将本月的日历添加到 months 文件末尾

# 重定向标准输入
cat < this_month # 将 this_month 文件内容当输入给 cat 处理
```

### std[in/out/err]

四个特殊的文件
- `/dev/null`   抛弃掉所有内容
- `/dev/stdin`  标准输入(fd:0)
- `/dev/stdout` 标准输出(fd:1)
- `/dev/stderr` 标准错误(fd:2)

管道(`|`)的作用就是把 (`/dev/stdout`和`/dev/stderr`)变为`/dev/stdin`

> 这里的**标准**是相对的

```bash
$ echo hello > /dev/stdout # 这里的标准输出是 输出到屏幕
hello

$ echo hello|cp /dev/stdin /dev/stdout|tr '[a-z]' '[A-Z]' # 对于 cp 而言 标准输出是stdout stream
HELLO
```

上述的内容可以同时使用 下面是一些例子

```bash
$ cat < hello.txt > /dev/stdout # 将 hello.txt 的内容重定向到 标准输出
# cat < hello.txt 1> /dev/stdout # 等于该命令
$ ./prog 1>log 2>error.log # 执行prog程序 并将正常输出重定向到 log 错误信息重定向到 error.log
```

### misc

#### stream merge

输出流合并

```bash
$ python main.py > rt.log 2>&1 # 2>&1 表示将 stderr 合并到 stdout 中
# 1>&2 则表示将 stdout 合并到 stderr
# 后面流合并的部分跟前面重定向的部分无关
# python main.py 2> rt.log 1>&2 # 效果一致
# python main.py &> rt.log # 一种简化形式
```

输入流合并
```bash
cat 0<&3 # 合并入 stdin
```

### self-defined stream/fd

可以使用 `exec` 创建新的描述符 可以使用[3,8] 6个描述符

```bash
exec 3 > rt.log # 定义 fd:3 为rt.log的输出流
echo hello >&3 # 写入文件 rt.log
# exec 3 >> rt.log # 可在描述符关闭后使用

# 定义输入符
exec 3 < rt.log
exec 0<&3 # 定义合并流
read line # 读取变量

# 关闭描述符
exec 3>&-
```

#### here doc|str

此外特殊的输入流有两种
```bash
# (here doc) 使用自定义的结束符 直接输入一段文字当输入流
$ cat << _self_defined_eof
...
content
...
_self_defined_eof

... # output

# (here string) 直接输入一段文字当输入流
$ cat <<< "input stream"
input stream
```

## dash

在shell脚本中会看见两种短横线

- 单横线`-`  表示标准输入
- 双横线`--` 表示参数结束(unix的习俗)

```bash
$ cat - # 换行后按 ^D (输入EOF) 结束
# cat < /dev/stdin
# 上面两个命令效果相同

$ git checkout {{branch_name}} -- {{filename}}
# Replace a file in the current directory with the version of it committed in a given branch:
```

## 参考

linux关闭文件描述符及lsof命令: https://blog.51cto.com/u_4048786/3201751
Shell 输入/输出重定向: https://www.runoob.com/linux/linux-shell-io-redirections.html
Shell自定义输入输出文件描述符: https://www.jianshu.com/p/15239a00f56b