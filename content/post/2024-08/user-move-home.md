---
title: "Conda Move Home"
date: 2024-08-09T19:23:28+08:00
description: Move conda's installcation path
categories: ["Linux",  "operation", "conda"]
layout: search
tags: ["develop"]
---

# 移动conda安装目录

如果 conda 路径在用户家目录 那么移动用户家目录时 这是必须要解决的问题

conda 已知硬编码路径的地方有 (~~mamba也差不多~~)
- shell rc 文件
- conda/etc/profile.d/conda.sh
- conda/bin/ 中脚本的 `#!`
- conda/envs/*/bin 各环境脚本的 `#!`

此外还有一些情况处理不了 比如 shell 脚本或者 Perl 脚本中设置的 `prefix` 变量

## .*shrc

首先修改 shell 启动脚本中的 conda 初始化代码

```bash
__conda_setup="$('/home/alice/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/alice/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/alice/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/alice/miniconda3/bin:$PATH"
    fi
fi
```

建议硬编码的根路径用变量表示
```bash
__CONDA_ROOT="__NEW_HOME__"
__conda_setup="$($__CONDA_ROOT/miniconda3/bin/conda 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "$__CONDA_ROOT/miniconda3/etc/profile.d/conda.sh" ]; then
        . "$__CONDA_ROOT/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="$__CONDA_ROOT/miniconda3/bin:$PATH"
    fi
fi
```

## conda.sh

第二步是修改 conda/etc/profile.d/conda.sh 中的变量

```bash
export CONDA_EXE='/home/alice/miniconda3/bin/conda'
export _CE_M=''
export _CE_CONDA=''
export CONDA_PYTHON_EXE='/home/alice/miniconda3/bin/python'
```
修改该文件中的前四行的 `conda` 和 base环境的`python` 路径

## base.bin

第三步是修改 base 环境下 bin 目录中脚本的 `#!` 路径

下面为 `$HOME/miniconda3/bin/pip3` 的代码

```python
#!/home/alice/miniconda3/bin/python

# -*- coding: utf-8 -*-
import re
import sys

from pip._internal.cli.main import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```

需要把前面一部分 `/home/alice` 替换为目标路径

此外 bin 目录下还有一些二进制文件和shell脚本不需要修改 跳过就好

> 可以通过 [`magic`](https://github.com/ahupp/python-magic) 库来判断 跟 `file` 差不多的效果

## env.bin

最后是环境的 bin 修改 跟修改 base 的 bin 是一样的操作

## auto

后续两步的操作可以用下面脚本来完成

```python
import os
import os.path as osp
import shutil

def replace_shebang(folder: str, path:str, file_only: bool = True, force: bool = False):
    assert osp.isdir(folder), f"{folder} is not a folder"
    assert path.count(" ") == 0, f"space in path name:{path} is disallowd"
    for file in os.listdir(folder):
        bfs = osp.join(folder, file)
        if file_only and not osp.isfile(bfs):
            continue

        with (
            open(bfs) as reader,
        ):
            try:
                content = reader.readlines()
                if not content[0].startswith("#!/"):
                    continue
                parts = content[0][2:].split("/")
                if not force:
                    assert "envs" in parts, f"{bfs} does not contain 'envs' in shebang"
                    # index = parts.index("envs")
                else:
                    if "python" not in parts[-1]:
                        continue # skip non-python file
                content[0] = f"#!{path}\n"

                writer = open(bfs+".temp", "w")
                writer.writelines(content)
                writer.close()
                print(f"mv {bfs+'.temp'} {bfs}")
                shutil.move(bfs+".temp", bfs)
                os.chmod(bfs, 0o755)
            except UnicodeDecodeError:
                print(f"{bfs} may be a binary file")
            except ValueError:
                # #!/bin/sh or something else who is irrelative with Python
                continue
            except:
                breakpoint()

def replace_with_conda_root(root:str, new_home:str):
    """
    1. root/bin -> new_home/`dirname root`/bin
    2. root/envs/*/bin

    root: the root path of conda like $HOME/miniconda3
    new_home: the new home path to replace the old one
    """
    # replace root/bin
    if root.endswith("/"):
        root = root[:-1]
    root_parts = root.split("/")
    # #!/home/alice/miniconda3/bin/python
    root_home = osp.join(new_home, root_parts[-1])
    replace_shebang(osp.join(root, "bin"), osp.join(root_home, "bin", "python"), force=True)

    # replace root/envs/*/bin
    # #!/home/alice/miniconda3/envs/myenv/bin/python
    for env in os.listdir(osp.join(root, "envs")):
        replace_shebang(osp.join(root, "envs", env, "bin"), osp.join(root_home, "envs", env, "bin", "python"))
```