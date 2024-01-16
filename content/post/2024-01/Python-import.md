---
title: "Python Import"
date: 2024-01-16T18:52:12+08:00
description: Python 模块导入路径
categories: ["Python"]
layout: search
tags: ["develop"]
---

# Python module import

一般的 Python 正常模块导入这里就不赘述了 本文从模块导入路径起手讲一讲相对路径的模块导入

## module path

首先看看模块的搜索路径 这是脚本执行时寻找所有模块的路径

```python
import sys
print(sys.path)
# sys.path[0] == os.path.dirname(__file__)
```

## relative import

Python 脚本有两种调用方式
- 直接执行文件
- 作用模块执行

两者的区别在于 `sys.path` 中添加的模块搜索路径不一样

前者为执行文件的路径(`dirname /path/to/script.py`) 后者为执行命令的路径(`pwd`)


### simple case

相对导入的相对关系


```
.
└── modules
    ├── mds
    │   ├── hello.py
    │   └── __init__.py
    ├── main.py
    └── pkgs
        ├── a
        │   ├── helper.py
        │   └── main.py
        └── b
            ├── fa.py
            ├── fb.py
            └── __init__.py
```
```python
# main.py
import sys
from mds.hello import pkg_a
import sys
import pkgs.b.fa
import pkgs.a.hp
```

```python
# mds/hello.py
from pkgs.a.hp import pkg_a
```

```python
# pkgs/a/helper.py
def hp():
    import sys
    print("in pkg.a.helper", sys.path[0])

# pkgs/a/hp.py
from .helper import hp

pkg_a = 13

import sys
print("in pkg.a.hp", sys.path[0])
```

```python
# pkgs/b/fa.py
from .fb import utils

import sys
print("in pkg.b.fa", sys.path[0])


# pkgs/b/fb.py
utils = "utils"
```

### run as script

最基础的用法为直接执行脚本

```bash
$ python3 modules/main.py # OK

# 不管在哪一级路径下都不行
$ python3 modules/mds/hello.py # Error
$ cd modules;python3 mds/hello.py # Error
ModuleNotFoundError: No module named 'pkgs'
# 此时 sys.path[0] == modules/mds 自然找不到 pkgs

# 下面两种带有相对导入的方式错误是相同的 
$ python3 modules/pkgs/a/hp.py # Error
# 此时 sys.path[0] == modules/a
$ python3 modules/pkgs/b/fa.py # Error
# 此时 sys.path[0] == modules/b
ImportError: attempted relative import with no known parent package
# 这样的相对应用只能在模块内使用
```

### run as module

稍有不同的执行方式是将文件作为模块来执行 这样的好处是可以直接执行子文件夹的文件

```bash
$ python3 -m modules.main # Error
# 此时 sys.path[0] == .

$ cd modules
# 此时 sys.path[0] == modules
$ python3 -m mds.hello # OK
# 可以在该路经找到 pkgs 模块
$ python3 -m pkgs.a.hp # OK
$ python3 -m pkgs.b.fa # OK
# a b 各为一个子模块 使用相对路径import时能够找到父级模块
```

## sys.prefix

第三方模块在经过pip下载之后 都放在 site-packages 目录下

了解类似conda等Pyhon环境管理工具对于Python寻找模块的影响 可以通过 `sys.prefix` 来猜测

```python
import site
# 查看部分第三方模块的路径
print(site.getsitepackages())
```

影响 Python 模块搜索路径的方式有好几种
- `PYTHONPATH` 设置该环境变量
- `python --prefix` 指定路径前缀

不过 conda 看上去与上述两种方法不同

conda 会在用户`PATH`中加入包含 Python 的 `bin` 路径 然后通过 Python 可执行程序的路径来更优雅实现不同模块环境的隔离

下面两个变量的关系为观察结果

```python
sys.prefix:str # site-packages 的前缀路径
sys.executable:str # Python 执行文件的路径
# 两者之间的大概关系
sys.prefix = '/'.join(sys.executable.split('/')[:-2])
# sys.executable=/usr/bin/python3
# sys.prefix <- /usr

# sys.executable=$HOME/conda/envs/ENV_NAME/bin/python3
# sys.prefix <- $HOME/conda/envs/ENV_NAME
```

本文主要参考[此处](https://sinhub.cn/2019/05/python-import-machinery-part-one/)
