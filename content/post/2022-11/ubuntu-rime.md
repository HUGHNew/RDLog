---
title: "Ubuntu Rime Ziran"
date: 2022-11-23T21:49:30+08:00
description: Ubuntu Rime 自然码双拼配置

---

# Ubuntu-Rime(ibus) 自然码配置

> 本方案主要用于 Ubuntu Rime(ibus)

> Ubuntu Rime 安装和使用
> 
> 自己百度或者知乎或者google
> 
> 切换 方案(schema)的默认键是 `F4`

## 下载依赖

> 自行下载 rime

```bash
# sudo apt install ibus-rime
sudo apt install librime-data-double-pinyin
```

## 配置

配置文件在 `~/.config/ibus/rime/` 目录下

输入法方案配置

```yml
# ~/.config/ibus/rime/default.custom.yaml
patch:
  schema_list:
    - schema: luna_pinyin_simp     # 朙月拼音 简体字模式
    - schema: double_pinyin        # 自然碼雙拼(默认繁体)
```

具体方案的配置在 `~/.config/ibus/rime/build` 目录下
```bash
# 查看现有的方案
ls ~/.config/ibus/rime/build|grep schema
```

对于双拼来说 配置文件就是 `double_pinyin.schema.yaml`

设置自然码默认简体
```yml
# ~/.config/ibus/rime/build/double_pinyin.schema.yaml
switches:
  - name: ascii_mode
    reset: 0
    states: ["中文", "西文"]
  - name: full_shape
    states: ["半角", "全角"]
  - name: simplification
    states: ["漢字", "汉字"]
  - name: ascii_punct
    states: ["。，", "．，"]
```
找到上面这部分

在 `simplification` 行下面添加 `reset: 1` 即默认使用简体 更改后如下

```yml
switches:
  - name: ascii_mode
    reset: 0
    states: ["中文", "西文"]
  - name: full_shape
    states: ["半角", "全角"]
  - name: simplification
    reset: 1
    states: ["漢字", "汉字"]
  - name: ascii_punct
    states: ["。，", "．，"]
```

## 使用

```bash
$ ibus-daemon -R # 先重启ibus
```

之后就可以正常用了

方案切换: 使用输入法时(切换当rime 然后打字时)按`F4` 可以呼出方案选单

[双拼练习](https://api.ihint.me/shuang/)

## Refs

- [RIME输入法配置双拼方案（Ubuntu下基于ibus）](https://blog.csdn.net/momo1938/article/details/107013949)
- [rime设置为默认简体](https://blog.csdn.net/chougu3652/article/details/100656237)
