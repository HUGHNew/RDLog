---
layout: base
title:  "Word Embedding vs. word2vec"
categories: research
tags: nlp representation
---

Word Embedding 是一种文本表示的技术 表现的是一种 **将单词转化为实数向量** 的思想

word2vec 是这种技术的具体实现

<!--more-->

## Embedding

text representation
- one-hot
- integer encode
- word embedding(Distributed representation)
  - word2vec
    - Skip-Gram
    - CBOW
  - GloVe



one-hot 与 整数编码 的区别在于一个是向量表示 一个是下标表示

embedding 在数学上表示[单射函数][embedding-zhihu]

word embedding 指就是 `(word) -> vector<float>` 的方法

## word2vec

这种技术有两种具体方法
- Skip-Gram: 中心词预测周围词
- Coutinuous Bag of Word: 周围词预测中心词

[embedding-zhihu]: https://www.zhihu.com/question/32275069/answer/80188672