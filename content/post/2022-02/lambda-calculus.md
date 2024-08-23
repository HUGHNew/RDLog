---
title: "Lambda Calculus"
date: 2022-02-08T22:00:00+08:00
description: lambda 演算基础
categories: ["misc"]
layout: search
tags: ["develop"]
---

# $\lambda$

## 概念

[三种 lambda 项](https://zh.wikipedia.org/wiki/%CE%9B%E6%BC%94%E7%AE%97)

> 函数的应用（application）是[左结合](https://zh.wikipedia.org/wiki/结合律#不可結合性)的

| 语法           | 名称   |
| -------------- | ------ |
| x              | 变量   |
| ($\lambda$x.M) | 抽象化 |
| (M N)          | 应用   |

### 两种变换

- $\alpha$ 等价 : 变量替换
- $\beta$ 规约 : 代值 如($\lambda$x.t)s 可化简为 t[$x$:= s]

捕获记法

> 假设 t， s 和 r 是 lambda 项，而 x 和 y 是变量。如果写成 t[x:=r] 是一种避免被捕获的记法方式，表示在 t 这个 lambda 项中，以 r 来替换 x 变量的值。

[具体定义](https://en.wikipedia.org/wiki/Lambda_calculus#Capture-avoiding_substitutions)

### $\eta$变换

lambda 等价的规则

> 对于任一给定的参数，当且仅当两个函数得到的结果都一致，则它们将被视同为一个函数

## church numerals

```lisp
0 = λf.λx.x
1 = λf.λx.f x
2 = λf.λx.f (f x)
3 = λf.λx.f (f (f x))
```

这里的问题是 0 的定义方法

使用高阶函数是为了与其他数字定义形式形同

f : 后继函数

x : 当前值/定义的 0 值

```lisp
-- 加法定义
PLUS = λm.λn.λf.λx.m f (n f x)
-- 乘法定义
MULT = λm.λn.λf.m (n f)
```

## bool

```scheme
TRUE  = λx.λy.x
FALSE = λx.λy.y -- 与 0 形式相同
```

这样的定义形式方便 if-else 之类二元形式的定义

```scheme
AND = λp q.p q FALSE
OR  = λp q.p TRUE q
NOT = λp.p FALSE TRUE
IFTHENELSE = λp x y.p x y
```

逻辑运算的理解

可以带入运算  走走流程

```
AND TRUE FALSE
≡(λp q.p q FALSE) TRUE FALSE =beta> TRUE FALSE FALSE
≡(λx y.x) FALSE FALSE =beta> FALSE
```

也可以理解为 每个变量的都是含两个参数的lambda 然后进行短路求值

## Y 组合子

### 引入

> lambda calculus 中 不能定义包含自身的函数

利用不动点性质来实现递归

`f=g(f)` g 的不动点

被表示为 **Y**

```
Y = λg.(λx.g(x x))(λx.g(x x))
```

> Y g 是 g 的不动点 `Y g=g(Y g)` ~~可以用代值证明~~

>  所有递归定义的函数都可以看作某个其他适当的函数的不动点，因此，使用`Y`所有递归定义的函数都可以表达为lambda表达式

[标准化的组合子](https://zh.wikipedia.org/wiki/%CE%9B%E6%BC%94%E7%AE%97#%E6%A8%99%E6%BA%96%E5%8C%96%E7%9A%84%E7%B5%84%E5%90%88%E5%AD%90%E5%90%8D%E7%A8%B1)

`(Y Y)=Y(Y Y)`

## SKI组合子演算

> 可以将 lambda 演算中的表达式转换为 SKI 组合子演算中的表达式

### SKI

**I** = λ*x*.*x*

**K** = λ*x*.λ*y*.*x* `<=>` λx.c = **K**c

**S** = λ*x*.λ*y*.λ*z*.*xz* (*yz*) `<=>` λx.(y z) = **S** (λx.y) (λx.z)

### SK

> **I** = **SKK**

```
I I = I
K K I = K
S K S K = K
```


$$
{\rm{I}} = \lambda x.x\\
= \lambda x.{\rm K} x \_\\
=> \lambda x.{\rm K} x ({\rm K}x)\\
= \lambda x.{\rm SKK}x\\
= SKK
$$


### iota

$\iota\,=\lambda$f.((f S) K)

```
I = ιι
K = ι(ιI) = ι(ι(ιι))
S = ι(K) = ι(ι(ι(ιι)))
```



## 引用

- [wiki lambda  演算](https://zh.wikipedia.org/wiki/%CE%9B%E6%BC%94%E7%AE%97)
- [Learn LC in y minutes](https://learnxinyminutes.com/docs/zh-cn/lambda-calculus-cn/)
- [Good Math/Bad Math 中译 cgnail](http://cgnail.github.io/academic/lambda-index/)

