---
title: "Git Worktree"
date: 2024-08-23T20:42:46+08:00
description: Quickview on git-worktree
categories: ["Linux", "operation", "git"]
layout: search
tags: ["develop"]
---

# Git Worktree

还在为频繁切换分支而烦恼吗 还在为stash暂存命名而挠头吗 那就看看 `git worktree` 吧

> `git worktree` 2015年就有了 所以不要担心自己的 git 版本问题

它的主要作用为: 仅需维护一个 repo 就可以同时在多个 branch 上工作 互不影响

> `git init/clone` 创建的仓库默认是只有一个 worktree 的

[命令速览][inspiration]
```bash
usage: git worktree add [-f] [--detach] [--checkout] [--lock [--reason <string>]]
                        [-b <new-branch>] <path> [<commit-ish>]
   or: git worktree list [-v | --porcelain [-z]]
   or: git worktree lock [--reason <string>] <worktree>
   or: git worktree move <worktree> <new-path>
   or: git worktree prune [-n] [-v] [--expire <expire>]
   or: git worktree remove [-f] <worktree>
   or: git worktree repair [<path>...]
   or: git worktree unlock <worktree>
```

## showcase

下面主要用一个实例来演示如何使用

```bash
# 可以创建在 ignore 路径 或者 上级路径
git worktree add _drafts misc
git worktree list # 能看见两个分支的 worktree 所在路径和目前 commit hash
# git worktree move _drafts ../parent_misc # move 的 source 需要是一个 worktree
cd _drafts
git log # 看到的是 misc 分支的 log 信息
cd ..
# 修改完之后可以删除 worktree
git worktree remove _drafts
```

感觉比较适合用于 dotfiles 的更新 当前的 dotfiles 依赖于某个分支 然后主要使用软链接 然后更新其他分支的时候通过 worktree 进行

[inspiration]: https://fev.al/posts/git-worktree/