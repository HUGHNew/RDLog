---
title: "Static Sites"
date: 2023-04-04T22:31:19+08:00
title: "CMS与静态网页生成器的选择"
categories: ["blog", "misc"]
tags: ["develop"]
description: 简述内容管理的选择和我遇到的问题
---

在需要构建自己博客的时候 使用开源的CMS或者静态网页生成器通常是最好的选择 尤其是对于不喜欢JS的用户而言

CMS: Content Management System 内容管理平台 一般会包含完整的前后端、权限管理和数据库整套的设施 但是只是写一点静态内容的用户来说 显得太臃肿了 而且不是基于文本的内容 不方便使用Git做版本管理 不过有兴趣的话 可以看看[这里的推荐][CMS]

那么优先排除掉了CMS 就进入了静态网页生成器的选择 同时因为对于Markdown的偏好 选出来了这份[不错的候选单][SWG]

在上面那份候选单之前 我曾使用过一个JS库来构建博客: [docsify](https://docsify.js.org/#/) 它的最大优势是不需要先生成静态网页 而是运行时构建网页的 方便早期不懂GitHub Action的时候 作为过渡选项

不过运行时构建的代价就是 首次打开特别慢 文件越多越明显

## VuePress

当我放弃 docsify 的时候 发现了 VuePress 它看上去不错 特别是刚好 VuePress@next (2.x-beta) 出了 可以用TS来写一些配置文件

VuePress的优势在于
- 默认的主题美观
- block级别的高亮拓展语法
- 可以直接引用代码文件

对于文档而言 它足够了

不过对于博客而言 它有点不对味

于是在内容多起来的时候 并不能直接发现新增了什么 这与博客放置新鲜内容的想法有些违背

## Jekyll

放弃 VuePress 的原因主要有两点
- VuePress 太像文档而不像博客 切换到一个类似博客的主题需要重构 代价太高
- 使用的 VuePress@next (2.x) 仍还是 beta 版本 blog timeline 风格插件不可用 只有VuePress1.x版本可以用 降版本就不能使用TS了

> 当时 VuePress 还有个问题就是 它的特性好用到我不好做迁移 所以在用 Jekyll 的时候 就直接没有迁移原来的内容

这个时期之后 便有了远离JS的想法 候选单上的就只剩下 Jekyll 和 Hugo

然后简单看了一下 Hugo 的文档 发现似乎整体比较复杂 就先选了简单一点的 Jekyll (正好当时Ubuntu20.04自带了Ruby 所以就用了)

Jekyll有自己的Liquid语法 能做一些比较复杂的事情 但我并不需要 我只需要简单的timeline

## Hugo

淘汰Jekyll的原因有点特别 产生这个想法是因为将Ubuntu升级到22.04之后 Ruby/Gem 的那台工具依赖出问题了 弄了半天还是不能本地build

其他的原因还有
- 不支持LaTeX公式
- 根据tags和categories作分类麻烦
- 摘要不可控

在我重装系统 使用Linux Mint之后 系统没有自带Ruby 同时下载的docker镜像用于build再次出错后 我将目光转向了Hugo

目前看来 Hugo 是一个不错的选择 对于上述的Jekyll问题能有不错的解决 能够满足我的初衷 而且从Jekyll迁移不过不算特别麻烦

### 从 Jekyll 迁移

> 发现官方有相关内容: <https://gohugo.io/tools/migrations/#jekyll> 看了一眼 似乎质量一般

建议先从主分支切分支出来操作 先删除Jekyll的特有文件 然后使用 `hugo new site . --force` 创建 Hugo 模板

最大的一个问题在于内容的迁移
- front matter 的改动 原有的layout不能用了 另外需要生成一下时间
- content 的改动 我这里主要是图片引用格式的变化

一点基础的改动可以使用 [migrate.py](https://github.com/HUGHNew/RDLog/blob/main/migrate.py)

其他对于 description 之类的改动只能手动操作或者手写脚本处理逻辑了

GitHub Action的部分 可以直接使用Hugo官方文档中的内容

整个一套从 Jekyll 迁移过来 大概用了2-3小时 不算太长 但还是有点折磨 最后是希望一开始就找到能够满足需要的工具 频繁的切换只是徒花时间

[CMS]: https://zhuanlan.zhihu.com/p/583806547
[SWG]: https://zhuanlan.zhihu.com/p/260957368

