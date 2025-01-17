---
title: "Python Debug"
date: 2025-01-17T20:31:21+08:00
description: A tough Python debugging journey under standard stream redirection
categories: ["python"]
layout: search
tags: ["develop"]
---

事情的开始时 我希望屏蔽一些标准输出 毕竟别人的模块有些关不掉的冗余信息

## suppresser

于是我有了一个装饰器

```python
import sys, os
import functools

def suppress_output(stream="stdout", redir:str=None):
    if redir == None:
        redir = os.devnull
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            redir_fd = open(redir, 'w')
            if stream == "stdout":
                orig = sys.stdout
                sys.stdout = redir_fd
            elif stream == "stderr":
                orig = sys.stderr
                sys.stderr = redir_fd
            else:
                raise ValueError(f"Unknown stream: {stream}")
            result = func(*args, **kwargs)
            if stream == "stdout":
                sys.stdout = orig
            elif stream == "stderr":
                sys.stderr = orig
            redir_fd.close()
            return result
        return wrapper
    return decorator
```

经过简单的测试 确实可以屏蔽 Python 的 `stdout/stderr` 于是就正常开始使用了

## problem

但是在测试的时候 发现了一个问题 就是 `eval_metrics.py` 与 `update_metrics.py` 有一段相同的代码 但是前者会有部分计算结果缺失 而后者正常

主要的计算代码为
```python
buster = PoseBusters("dock").bust(gen_mol, ref_mol, protein)
```

跳转进去一看 发现主要问题在于 获取mol处的代码有问题 不能从文件获取分子

```python
if "mol_cond" in paths and paths["mol_cond"] is not None:
    mol_cond_load_params = self.config.get("loading", {}).get("mol_cond", {})
    mol_args["mol_cond"] = safe_load_mol(path=paths["mol_cond"], **mol_cond_load_params)
if "mol_true" in paths and paths["mol_true"] is not None:
    mol_true_load_params = self.config.get("loading", {}).get("mol_true", {})
    mol_args["mol_true"] = safe_load_mol(path=paths["mol_true"], **mol_true_load_params)
```

经过对比调试 发现对于同样的 `paths` 参数 `eval_metrics.py` 与 `update_metrics.py`在调试时的结果不同 前者获取不到分子

发现问题在于 `safe_load_mol`  eval时无法正常load 但是update时可以获取

此时 eval 拿到的报错信息是 `ValueError: I/O operation on closed file.`

```python
def safe_load_mol(path: Path, load_all: bool = False, **load_params) -> Mol | None:
    try:
        path = _check_path(path)
        with CaptureLogger():
            mol = _load_mol(path, load_all=load_all, **load_params)
        return mol
    except Exception as exception:
        logger.warning("Could not load molecule from %s with error: %s", path, exception)
    return None

# posebusters.tools.logging.py
class CaptureLogger(logging.Handler):
    """Helper class that captures Python logger output."""

    def __init__(self, module=None):
        """Initialize logger."""
        super().__init__(level=logging.NOTSET)
        self.logs = {}
        self.devnull = open(os.devnull, "w")
        rdkit.log_handler.setStream(self.devnull)
        rdkit.logger.addHandler(self)

    def __enter__(self):
        """Enter context manager."""
        return self.logs

    def __exit__(self, *args):
        """Exit context manager."""
        self.release()

    def handle(self, record):
        """Handle log record."""
        key = record.levelname
        val = self.format(record)
        self.logs[key] = self.logs.get(key, "") + val
        return False

    def release(self):
        """Release logger."""
        rdkit.log_handler.setStream(sys.stderr)
        rdkit.logger.removeHandler(self)
        self.devnull.close()
        return self.logs

# rdkit.__init__.py
log_handler = logging.StreamHandler(sys.stderr)
```

## chain

顺着调用链进去 进一步定位问题在于 `rdkit.log_handler.setStream(self.devnull)` 然后发现初始化的stream为 `sys.stderr`

到这里已经要进入标准库 估计错误就在这里 不会再深入了

但这里看不出来有什么问题 因为eval和update都是一样的调用方式 从错误信息看 应该是某个fd被提前关了

debug中发现 `self.devnull` 都是正常的 open 状态 不过有时候 `rdkit.log_handler.stream` 是关闭的 所以问题应该出在 `setStream` 上 这里需要先刷新旧的流 于是报错

于是考虑是否是对于`sys.stderr`的修改有影响 于是想到了之前的装饰器
1. 于是修改嵌套时的逻辑 发现标准流被修改后就不再修改了 但是发现没用
2. 去掉了一个 suppress stderr 再测试 程序终于正常了

## analyse

虽然代码能跑了 但是不是很清楚为什么之前不能跑 于是截取代码片段 逻辑如下

```python
import sys, os
import functools
import logging

logger = logging.getLogger("error")
log_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(log_handler)


class CaptureLogger(logging.Handler):
    """Helper class that captures Python logger output."""

    def __init__(self, module=None):
        """Initialize logger."""
        super().__init__(level=logging.NOTSET)
        self.logs = {}
        self.devnull = open(os.devnull, "w")
        log_handler.setStream(self.devnull)
        logger.addHandler(self)

    def __enter__(self):
        """Enter context manager."""
        return self.logs

    def __exit__(self, *args):
        """Exit context manager."""
        self.release()

    def handle(self, record):
        """Handle log record."""
        key = record.levelname
        val = self.format(record)
        self.logs[key] = self.logs.get(key, "") + val
        return False

    def release(self):
        """Release logger."""
        log_handler.setStream(sys.stderr)
        logger.removeHandler(self)
        self.devnull.close()
        return self.logs

@suppress_output("stderr")
def update():
    with CaptureLogger():
        pass


@suppress_output()
def eval():
    for _ in range(2):
        update()

if __name__ == "__main__":
    eval()
```

发现一个逻辑的问题在于 `log_handler` 是全局的 但是 `CaptureLogger` 这个context是局部的 所以会导致在context退出时 会用全局变量来恢复全局变量的设置

但是我的装饰器正好会修改全局变量 而且给到的临时值也是局部变量 会导致 `CaptureLogger` 恢复现场时 引用到修改过的全局变量 `sys.stderr` 导致了错误


## conclusion

对于全局变量的修改还是要注意控制粒度 不然容易导致与其他模块的冲突