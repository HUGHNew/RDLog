---
title: "Python CLI Toolkit"
description: Python CLI 工具哪家强
date: 2023-10-13T17:00:51+08:00
categories: ["Python",  "introduction", "terminal"]
layout: search
tags: ["develop"]
---

# arguement-parse

当使用 Python 写点 CLI 小脚本或者训练传参的时候 多需要通过命令行传递 那么除了原始的`argparse`之外 还有什么方便的途径

## global

> 最野蛮生长的一种方式

> 什么 你说参数类型? 自己定义和校验去吧

```python
global_vars = globals()
mode = eval(global_vars["mode"]) if "mode" in global_vars else 0 # default
```

一个详细的实现见[此](https://github.com/karpathy/nanoGPT/blob/master/configurator.py)

## [transformers.HfArgumentParser][hfap]

> 对于深度学习传参来说很不错 如果你需要使用 `transformers` 这个库的话

该方法的便利之处在于利用了 `dataclass` 提供了参数类型默认值和代码补全

```python
@dataclass
class ModelArguments:
    model_name_or_path: Optional[str] = field(default="facebook/opt-125m")


@dataclass
class DataArguments:
    data_path: str = field(default=None, metadata={"help": "Path to the training data."})

parser = transformers.HfArgumentParser((ModelArguments, DataArguments))
model_args, data_args = parser.parse_args_into_dataclasses()

model_args.model_name_or_path # 具有代码补全与类型提示
```

## [Typer][typer]

但对于一般的命令行脚本来说 上面三个选择都太麻烦了 最好是直接能够利用函数参数 所以可以有下面两个选择
- Typer
- Fire

下面两个示例可以基本展示 `Typer` 的用法 更多使用参见[此](https://typer.tiangolo.com/)

`Typer` 会根据类型提示来进行类型转换 当参数有默认值时 只能使用命名参数的形式赋值

```python
# pip install "typer[all]"
import typer


def main(name: list[str], suffix:str='!'):
    print(f"Hello {",".join(name)}{suffix}")


if __name__ == "__main__":
    typer.run(main)
```

在命令行执行脚本

```bash
$ python3 test.py name world name2 my name end --suffix '?'
Hello name,world,name2,my,name,end?
```

`Typer` 支持多指令(组)和链式命令调用 默认的命令为函数名

```python
import typer

# Init CLI
cli = typer.Typer(chain=True)

@cli.command() # the command name is `name` (Default: the function name)
def name(word:str):
    typer.echo(f"Chain 1: {word}")

@cli.command('name2')
def my_function_name(word:str):
    typer.echo(f"Chain 2: {word}")

if __name__ == "__main__":
    cli()
```

命令行调用如下

```bash
$ python3 test.py name world name2 my name end
Chain 1: world
Chain 2: my
Chain 1: end
```

## [Fire][fire]

相比于 `Typer` `Fire` 显得更灵活一些 完整的指导见[此](https://github.com/google/python-fire/blob/master/docs/guide.md)

`Fire` 好在解决了 `Typer` 只能使用位置参数或者命名参数一种方式 另外还可以使用短命令指定参数

`Fire` 会比 `Typer` 显得更简洁一点 比如多命令时

```python
# in test.py
import fire

def cmd0(): pass
def cmd1(): pass
def cmd2(): pass

fire.Fire()
```
命令行可以使用
```bash
python3 test.py cmd0
python3 test.py cmd1
python3 test.py cmd2
python3 test.py cmd0 cmd1 cmd2 cmd0 # chain call
```

对于带参数命令 `Fire` 可以使用位置参数和命名参数来赋值

```python
import fire
def main(
    serial: str = None,
    target: str = "",
    private: str = "",
    prompt: bool = True,
    app: str = None,
):
  pass


if __name__ == "__main__":
    fire.Fire(main)
```

`Fire` 会为没有冲突的变量生成首字母的短命名参数

```bash
python3 test.py -s 123 'target' --prompt False
```

从简洁性和便捷性来看 对于一般的命令行参数的要求 `Fire` 看上去更好用一些

[hfap]: https://huggingface.co/docs/transformers/internal/trainer_utils#transformers.HfArgumentParser
[typer]: https://github.com/tiangolo/typer
[fire]: https://github.com/google/python-fire