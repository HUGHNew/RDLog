---
layout: base
title:  "SSH usage & login security"
categories: exploration
tags: tech security linux
---
ssh的使用与登录方式的安全性问题探索

直接跳[结论](#tldr)
<!--more-->

## fingerprint

ssh 连接的第一步需要手动确认服务器的指纹

那么需要知道如何查询服务器的指纹: 在服务器端 `ssh-keygen -lf /etc/ssh/ssh_host_ecdsa_key.pub` (针对 ECDSA 算法 默认使用SHA256) 可以指定其他签名算法 `[-E md5|sha256|..]`

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

## 加密过程



## 算法

rsa

ed25519

## tl;dr

> `ed25519` 算法比 `RSA` 更安全
> 
> 同时也更建议使用公钥的方式(同时**建议私钥设置密码**)

简单介绍一下使用吧

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