---
layout: search
headless: true
title:  "SSH usage & login security"
categories: ["tech", "security", "linux"]
tags: ["exploration"]
date: 2022-10-03T00:00:00+08:00
description: ssh的使用与登录方式的安全性问题探索
---
ssh的使用与登录方式的安全性问题探索

直接跳[结论](#tldr)

## fingerprint

ssh 连接的第一步需要手动确认服务器的指纹 这是防止中间人攻击和确保安全性的重要一环

查询服务器的指纹有两种方法:

在客户端上 需要先获取服务器公钥文件再计算指纹

```bash
$ ssh-keyscan __host__ # 获取所有公钥
$ ssh-keyscan -t ed25519 __host__ # 获取 ed25519 加密算法的公钥
$ ssh-keyscan -t ed25519 __host__|ssh-keygen -lf - # 获取 ed25519 公钥的 fingerprint
# 算法集合: rsa,dsa,ecdsa,ed25519
```

在服务器上 可以直接查看 公钥和私钥在`/etc/ssh`路径下

```bash
$ ssh-keygen -lf /etc/ssh/ssh_host_$algo_key.pub # 查看某种算法的公钥 fingerprint
# algos: rsa,dsa,ecdsa,ed25519
# 可以指定其他签名算法 `[-E md5|sha256|..] (默认使用 SHA256)
```
## 加密过程

基本与[TLS1.2][TLS]加密过程相同(经典的RSA密钥交换方案) 不过验证证书(服务器fingerprint)的工作交给了用户来完成

> **fingerprint** 是用于客户端辨别是否为真实服务器的根据 效果等同于 HTTPS 证书

## 算法

现在在使用的加密算法主要是下面四种
- ~~DSA~~ (属于是已经不被支持的淘汰算法了)
- RSA: 3072/4096bit长度是安全选项 长度低于2048比特的密钥已经被认为是不安全的
- ECDSA: 不太稳定 依赖于机器产生随机数的性能
- Ed25519: 目前最推荐 加密性能更好同时密钥长度还更短

```bash
# 查看当前所使用的密钥
for key in ~/.ssh/*.pub; do ssh-keygen -l -f "${key}"; done
```

使用 ed25519 算法生成密钥

```bash
ssh-keygen -t ed25519 [-C "your comment here"] [-f ~/.ssh/your_private_key_file]
# -C 添加备注内容(可选)
# -f 指定私钥文件名(可选) 默认私钥文件名为 id_ed25519
# 公钥文件名默认为 私钥文件名.pub
```

## ssh-copy-id

使用非对称加密需要把客户端的公钥拷贝到服务端上 一般会使用`ssh-copy-id`

这其实是个脚本文件 核心逻辑在于下面这段

```bash
[ "$DRY_RUN" ] || printf '%s\n' "$NEW_IDS" | \
  ssh "$@" "exec sh -c 'cd ; umask 077 ; mkdir -p .ssh && { [ -z "'`tail -1c .ssh/authorized_keys 2>/dev/null`'" ] || echo >> .ssh/authorized_keys ; } && cat >> .ssh/authorized_keys || exit 1 ; if type restorecon >/dev/null 2>&1 ; then restorecon -F .ssh .ssh/authorized_keys ; fi'" \
  || exit 1
```

效果约等于 `cat ~/.ssh/your_pub_key|ssh user@ip "cat >> .ssh/authorized_keys"`

详解:
- `tail -1c` 查看最后一个字节
- `{ [ -z ... ] || echo >> .ssh/authorized_keys ; }` 保证有个换行 `-z` 为判空
- `cat >> .ssh/authorized_keys` 此处将之前通过管道传入的公钥放入服务器`authorized_keys`中
- [`restorecon`][restore-context] 恢复(restore)文件上下文(context)

> 可以看出 这个脚本底层使用 ssh 它的安全性和使用密码登录ssh一致

## ssh config

SSH 客户端和服务器可以添加一些配置文件 客户端的默认配置文件为`/etc/ssh/ssh_config`和`~/.ssh/config`

> 完整的配置参考见[此](https://www.ssh.com/academy/ssh/config)

常用的配置为配置服务器的别名 配置一个服务器的别名的写法如下
```
Host nickname # 你想使用的别名
  User your_username # 真实的用户名
  HostName ip_or_host # 服务器 IP 或者域名
  IdentityFile ~/.ssh/private_key # 对应的私钥
  IdentitiesOnly yes # 只使用密钥登录
  Port 22 # 设置连接端口 默认为 22
```

配置一台需要中间跳板的服务器写法如下

```
Host rev_nick
  User your_username # 真实的用户名
  HostName ip_or_host # 服务器 IP 或者域名
  IdentityFile ~/.ssh/private_key # 对应的私钥
  IdentitiesOnly yes # 只使用密钥登录
  Port 22 # 设置连接端口 默认为 22
  ProxyJump nickname
```

`ProxyJump` 的值为一台服务器

如此配置之后

```bash
$ ssh nickname # 登录 nickname 服务器
$ ssh rev_nick # 登录 nickname 作为跳板的服务器
```

## 补充内容

### authentication

现在的授权方式有两种
- 密码登录
- 密钥登录(公钥私钥)

对比这两种方式 我个人更倾向于与密钥登录

| 方式 | 优点 | 缺点 |
| --- | --- | --- |
| 密码 | 使用简单<br/>一些ssh GUI工具提供记住密码功能 | 如果监听整个通信 密码可能会被获取并解密<br/>大多数人的密码通用且可能比较简单 |
| 密钥 | 密码相关数据不会出现在通信过程中 | 使用有一定的理解成本<br/>私钥安全性依赖于它的私密性 |

总体来说 偏好原因如下
- 使用**密钥**不会让密码多次在通信中反复出现 更安全一点
- 使用**密钥**对于命令行用户更友好(除非sshd没有设置密钥授权)

### Pubkey permission

首先先开启服务器的公钥登录

```bash
# in /etc/ssh/sshd_config
PubkeyAuthentication yes
```

用户目录权限
```bash
私钥 600 # 保证私钥其他用户没有权限
.ssh 700 # 保证 others 没有写权限
公钥 644 # 同上
.ssh/authorized_keys 644 # 同上
```

如果权限设置有问题 ssh 公钥登录将不启用

如果不是使用的默认公钥名 那么在使用 `user@ip` 登录时 需要指定私钥文件 `ssh -p _port_ -i private.file u@ip`

### tunnel

可以将 ssh 用作加密通信的中介: 端口转发

作用
- 加密数据传输
- 加密跳板 绕过防火墙

| 转发方式 | 使用场景 | 指令示例 | 使用示例 | 备注 |
| ------ | ------- | ------ | ------- | --- |
| 动态转发 | 用作代理服务器 | `ssh -ND local-port tunnel-host` | `curl -x socks5://localhost:local-port http://www.example.com` | 需要使用SOCKS5协议 |
| 本地转发 | 指定本地端口数据转发到跳板机端口 | `ssh -NL local-port:target-host:tunnel-port tunnel-host` | `curl http://localhost:local-port` | tunnel-host可达target-host(可以相同) |
| 远程转发 | 指定跳板机端口数据转发到本地端口 | `ssh -NR remote-port:target-host:target-port remote-host` | 

具体见 [WangDoc SSH port-forwarding][port-forwarding]

### rsync

> rsync: remote sync 远程同步工具 可以只传变动内容

远程传输时 rsync 会默认使用 ssh 协议

```bash
$ rsync remote-host:source dest
$ rsync -e 'ssh -p port' source remote-host:dest
```

具体使用见 [WangDoc rsync][rsync]

## tl;dr

> `ed25519` 算法比 `RSA` 更安全
> 
> 同时也更建议使用公钥的方式(同时**建议私钥设置密码**)

简单介绍一下使用吧

> 先需要服务器允许公钥登录 配置文件:`/etc/ssh/sshd_config`

```bash
# 生成公钥和私钥 中括号中的参数都是可选的
ssh-keygen [-t ed25519] [-C "your comment here"] [-f ~/.ssh/your_private_key_file]
# 默认加密算法为 RSA 建议使用 ed25519
# 默认私钥文件名: ~/.ssh/id_ed25519 (其实是 id_${加密算法}) 公钥: ~/.ssh/id_ed25519.pub

# 之后是确定密码 建议使用 不过偷懒的话 敲两下回车就好了

ssh-copy-id [-i ~/.ssh/your_private_key_file.pub] _user@_hostname

# 之后就可以用了
```

为了使用方便的话 一般会**设置别名**(可选)

在文件 `~/.ssh/config` 里面添加 下面一段内容

```
# 设置之后可以通过 `ssh nickname` 的方式快速登录
Host nickname # 你想使用的别名
  User your_username # 真实的用户名
  HostName ip_or_host # 服务器 IP 或者域名
  IdentityFile ~/.ssh/private_key # 对应的私钥
  IdentitiesOnly yes
  Port 22 # 设置端口 默认为 22
```

[restore-context]: https://man7.org/linux/man-pages/man8/restorecon.8.html
[medium-ed25519]: https://medium.com/risan/upgrade-your-ssh-key-to-ed25519-c6e8d60d3c54
[ssh-copy-id-security]: https://security.stackexchange.com/questions/106376/is-the-ssh-copy-id-command-secure
[key-is-better]: https://security.stackexchange.com/questions/3887/is-using-a-public-key-for-logging-in-to-ssh-any-better-than-saving-a-password
[passwd-vs-key]: https://thorntech.com/passwords-vs-ssh/
[TLS]: https://hughnew.github.io/feeds/handbook/network/TLS.html#tls1-2
[port-forwarding]: https://wangdoc.com/ssh/port-forwarding
[rsync]: https://wangdoc.com/ssh/rsync