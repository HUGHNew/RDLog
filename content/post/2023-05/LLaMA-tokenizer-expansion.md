---
title: "LLaMA Tokenizer Expansion"
date: 2023-05-29T16:33:47+08:00
categories: ["NLP", "LLaMA", "tokenizer", "sentencepiece"]
layout: search
tags: ["research"]
---

# LLaMA 词表扩充

> LLaMA tokenizer 是一个 byte-level BPE(BBPE) 模型
> 
> BPE 的参数使用 [sentencepiece](https://github.com/google/sentencepiece) 库训练得到

对于 LLaMA 词表的扩充 可以使用同样的库进行新数据上的参数训练 然后手动合并去重

## 词表扩充原因和用途

LLaMA 词表仅有32K 而且主要在拉丁和西里尔数据上进行训练 对于其他语言编码效率低

虽然从 byte-level 的实现逻辑上来讲 模型本身可以支持任意字符 但会存在编码效率、字符限制和生成效率等问题

在扩充词表后在进行预训练 可以得到更好的效果[#304](https://github.com/ymcui/Chinese-LLaMA-Alpaca/issues/304)

## 基于sentencepiece的 LLaMA 词表扩充

sentencepiece的API支持多个tokenizer模型的合并 所以可以根据自己的数据训练一个词表模型之后 合并词表

训练新的词表模型

```python
import sentencepiece as spm
spm.SentencePieceTrainer.Train(
    input='YOUR_FILE_HERE',
    model_prefix='MODEL_NAME', # -> MODEL_NAME.model MODEL_NAME.vocab
    vocab_size=1000,
    model_type="bpe",
    byte_fallback=True, # 对没见过的词进行 byte-level 处理
)
```

合并词表代码可见 [merge_tokenizers.py](https://github.com/ymcui/Chinese-LLaMA-Alpaca/blob/main/scripts/merge_tokenizers.py)

合并词表后 词表大小和模型输出的Embedding大小不一致 所以需要调整 LLaMA Embedding 的大小 代码如下

> 不调整的报错信息: `Assertion srcIndex < srcSelectDimSize failed....RuntimeError: CUDA error: device-side assert triggered`

```python
# https://github.com/ymcui/Chinese-LLaMA-Alpaca/blob/main/scripts/inference_hf.py#LL70-L77
model_vocab_size = base_model.get_input_embeddings().weight.size(0)
tokenzier_vocab_size = len(tokenizer)
print(f"Vocab of the base model: {model_vocab_size}")
print(f"Vocab of the tokenizer: {tokenzier_vocab_size}")
if model_vocab_size!=tokenzier_vocab_size:
    assert tokenzier_vocab_size > model_vocab_size
    print("Resize model embeddings to fit tokenizer")
    base_model.resize_token_embeddings(tokenzier_vocab_size)
```

## references

参考项目: <https://github.com/ymcui/Chinese-LLaMA-Alpaca/>

相关的issue
- 词表合并问题[#128](https://github.com/ymcui/Chinese-LLaMA-Alpaca/issues/128)
- 词表扩充 + 预训练代码[#150](https://github.com/ymcui/Chinese-LLaMA-Alpaca/issues/150)
- Vocabulary expansion pre-training code for Chinese language[#161](https://github.com/ymcui/Chinese-LLaMA-Alpaca/issues/161)

另外的相关库: [LianjiaTech/BELLE](https://github.com/LianjiaTech/BELLE)

扩充词表的相关代码: [merge_tokenizers.py](https://github.com/LianjiaTech/BELLE/blob/main/train/scripts/merge_tokenizers.py)

扩充BERT词表的方法: <https://medium.com/@pierre_guillou/nlp-how-to-add-a-domain-specific-vocabulary-new-tokens-to-a-subword-tokenizer-already-trained-33ab15613a41>