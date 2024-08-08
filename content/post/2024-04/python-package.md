---
title: "Python Package"
date: 2024-04-11T09:54:32+08:00
description: A simple Python packaging tutorial with poetry and twine
categories: ["python",  "introduction", "package"]
layout: search
tags: ["develop"]
---

## prerequisites

> 标准的流程可以参考 [官方文档][off-pkg]

需要安装的pip包有
- [poetry][poetry-inst]
- twine

```bash
pip install poetry twine
```

另外需要在 [PyPI][pypi] 上注册账号

poetry 的便利之处是可以
- 通过 `poetry new` 创建项目脚手架
- 通过 `poetry init` 初始化当前项目

## extras

对于一个简单的项目 比较有趣的事情是添加可选项配置与添加命令行命令

一个简单的项目如下

```tree
.
├── demo
│   ├── cli.py
│   └── __init__.py
├── pyproject.toml
├── README.md
└── tests
    └── __init__.py
```

```python
# cli.py
def entry():
    print("Hello, world!")
```
可以在`pyproject.toml`中配置
```toml
[tool.poetry.extras]
np = ["numpy"]

[tool.poetry.scripts]
demo = "demo.cli:entry" # 最后目标是一个 callable
```

安装这个包之后 可以在命令行调用

```bash
$ demo
Hello, world!
```

## package

```bash
poetry build
```

build 之后就能在 dist 目录下看到对应的打包产物了

## upload

上传到 PyPI 需要 API token 点击[这里][api-token]可以新增token

```bash
# username 就是 __token__ 这个字符串
# YOUR_API_TOKEN 就是新增的token对应的值
cat << EOF > ~/.pypirc
[pypi]
  username = __token__
  password = <YOUR_API_TOKEN>
EOF
```

`poerty publish` 在我使用过程中有点问题 所以只能使用传统方案 `twine`

`python3 -m twine upload --repository testpypi dist/*`


[off-pkg]: https://packaging.python.org/en/latest/tutorials/packaging-projects/
[poetry-inst]: https://python-poetry.org/docs/#installing-with-pipx
[pypi]: https://pypi.org/
[api-token]: https://pypi.org/manage/account/token/