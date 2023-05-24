---
title: "Command Update"
date: 2023-05-13T01:38:19+08:00
categories: ["Linux", "operation", "introduction", "tools"]
layout: search
tags: ["develop"]
---

# Linux 常用工具大升级

让一部分工具先现代化起来 实现整体系统操作的现代化

## 升级表

升级一些标准工具

| 原始工具 | 推荐使用 | 安装方式 | 补充 |
| :----: | :-----: | :----: | -- |
| cat | [bat][bat] | apt/bin | Debian里面叫 batcat |
| ping | [prettyping][prettyping] | script | 一般好用 |
| man | [tldr][tldr] | apt/pip | 一键快速入门 |
| ls | [exa][exa] | apt/bin | 舒适翻倍 |
| top | [htop][htop] | apt/bin | 妈妈再不用担心你看不懂 top 的数据了 |
| find | [fd][fd] | apt/bin | 找不到文件的时候似乎比较少 |

上面可以直接用二进制的工具 除了 htop 都是Rust写的 所以可以直接 `cargo install`

apt 表示通过包管理进行下载或者只提供deb之类的系统包

## 补充表

补充一些可选工具

- `pv`(apt): 管道查看器 这下知道管子里的水什么时候流完了
- [`atuin`](https://github.com/ellie/atuin)(apt): shell历史数据库和反向搜索助手 还支持本地数据统计 **在WSL2中Bash中会有0.3s左右的额外用时 体感明显**
- [`frogmouth`](https://github.com/Textualize/frogmouth)(pip): 终端Markdown浏览器 摆脱颅内编译的好助手
- [`ctop`](https://github.com/bcicen/ctop)(apt/docker): container top
- [`sd`](https://github.com/chmln/sd)(apt/bin): 现代人更友好的`sed`
- [`fuck`](https://github.com/nvbn/thefuck)(pip): 命令自动修正 似乎不如手动快
- [`xonsh`](https://github.com/xonsh/xonsh)(pip): 年轻人的另一款基于Python的shell 支持直接执行Python 开箱即用 越不熟悉bash越好用
- [`helix`](https://github.com/helix-editor/helix)(bin): 年轻人现代化的vim 支持LSP 服务器上改Python有补全了
- [`gpustat`](https://github.com/wookayin/gpustat)(pip): 简洁彩色版`nvidia-smi`
- [`scmpuff`](https://github.com/mroth/scmpuff)(bin): 数值化`git add` 不过就几个文件的话 用处不大

## references

- <https://zhuanlan.zhihu.com/p/48076652>
- <https://linux.cn/article-14488-1.html>

[bat]: https://github.com/sharkdp/bat
[prettyping]: https://github.com/denilsonsa/prettyping
[tldr]: https://github.com/tldr-pages/tldr
[exa]: https://github.com/ogham/exa
[htop]: https://github.com/htop-dev/htop
[fd]: https://github.com/sharkdp/fd