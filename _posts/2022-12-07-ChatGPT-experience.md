---
layout: base
title:  "OpenAI ChatGPT 小玩"
categories: exploration
tags: GPT ML
---
ChatGPT 使用体验
<!--more-->

让ChatGPT对话模型去模拟一个终端现在仍然是可以的 有一定的可玩性。

这里先看两个比较正经的示例
- 复述生成
- few-shot 消极转积极的生成

## 复述生成

这里多种语句 包括一般的白话句、多重否定句和文言

除了“怀民亦未寝”这种节选半句 其他的效果都还可以 (红框标记为效果不太行)

![retell]({{site.baseurl}}/assets/images/ChatGPT-retell.png)

## 多轮对话

在隐含指代情况下的多轮对话 效果不好(这里的两轮对话效果不错)

![multi-phase-dialogue]({{site.baseurl}}/assets/images/ChatGPT-multi-diag.png)

## 消极句子转换为积极句子

在 few-shot 的情况下 测试了消极语句转换为积极语句的效果 整体还行

![positive-generate]({{site.baseurl}}/assets/images/ChatGPT-pos-gen.png)

## 反向终端模拟

一个简单代码改错的例子: 用模型模拟用户 我模拟终端 来逐步修改编译的报错

```cpp
// 最初的代码
int main() {
  cout<<"hello"
  return 0;
}
```

图中绿色内容为模型的输出 可以看到模型的理解能力很强 但同时也还是不能完全理解 没开停用词的话 会生成很多内容

![]({{site.baseurl}}/assets/images/ChatGPT-mock-shell0.png)
![]({{site.baseurl}}/assets/images/ChatGPT-mock-shell1.png)
![]({{site.baseurl}}/assets/images/ChatGPT-mock-shell2.png)
![]({{site.baseurl}}/assets/images/ChatGPT-mock-shell3.png)

## 推理

一个简单任务: 将 Cpp 代码转换为 Python 代码(多轮对话)

> 图中红色矩形部分为**模型生成内容**

能看出模型见过一些常用的Linux包管理器 但有印象的也只是 apt/yum 了

同时能看出 在多轮对话的情况下 也会忘掉刚才的错误(这里表现出推理能力可能不太够 包管理下不了包应该认为没有更新index)

![infer-ability]({{site.baseurl}}/assets/images/ChatGPT-CND-joke.png)

## 未联网

从一个点证实模型是独立的: 每次清空内容后问时间都是不一样的

![date]({{site.baseurl}}/assets/images/ChatGPT-date.png)