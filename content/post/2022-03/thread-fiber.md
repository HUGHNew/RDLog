---
title: "Thread Fiber"
date: 2022-02-14T22:09:33+08:00
description: X程
categories: ["Linux", "misc"]
layout: search
tags: ["develop"]
---

# X程

> 进程 线程 协程

> IO密集型一般使用多线程或者多进程 CPU密集型一般使用多进程 强调非阻塞异步并发的一般都是使用协程

| 进程                         | 线程                           | 协程       |
| ---------------------------- | ------------------------------ | ---------- |
| 分配和管理资源的基本单位     | 进程的一个执行单元 CPU调度单位 | 用户级线程 |
| 竞争计算机系统资源的基本单位 | 轻量级进程                     | 轻量级线程 |

> linux 用`task_struct`表示任务(process/thread) 每个thread对应一个`task_struct`对象

## 进程

一个进程就是一个正在执行程序的实例，包括程序计数器、寄存器和变量的当前值。

```
-----------
|Kernel(映射到虚拟内存)|最大地址
|argv environ|
|栈(stack)|
|(栈向下生长)|
|(堆向上生长)|
|堆(heap)|
|BSS(未初始化的全局变量)|
|数据段(.data)|
|文本段(.text)|0
--------------
```
内存中的进程

进程创建时分配的资源
- pid
- CPU时间
- 内存(虚拟内存)
- 文件
- IO设备...

上下文切换:
- PCB
- 内存交换(in/out)
  - 动态内存请求(`request_memory`/`release_memory`)

### PCB
进程控制块:操作系统内的进程表示
- 进程状态
- 程序计数器(PC)
- CPU寄存器
- CPU调度信息
  - 基地址
  - 页表
- 内存管理信息
- 记账信息(accounting info) CPU时间等信息
- IO信息

`task_struct` in `<linux/sched.h>`

### 页表
实现
- 一组专用寄存器 -- 小页表可用
- 内存+页表基地址寄存器(Page-Table Base Register, PTBR) -- 太慢
- 内存+PTBR+TLB(保存少量页表条目)

## 线程

线程有自己的寄存器和堆栈

多线程模型(用户线程与内核线程的关系)
- 多对一
- 一对一
- 多对多
  - 变种:Hybrid 多对多+一对一

### TLS(Thread Local Storage)
线程本地存储 在线程中可见(类似于线程的static)

局部变量仅在作用域可见

```cpp
#include<iostream>
#include<thread>
thread_local int count = 0;
void incr(const char*tag){
  ++count;
  std::cout<<"tag: "<<tag<<" count: "<<count<<std::endl;
}
int main(){
  std::thread([](const char*s){
    incr(s);
    incr(s);
    incr(s);
  },"thread-1").join();
  std::thread([](const char*s){
    incr(s);
    incr(s);
    incr(s);
  },"thread-2").join();
  return 0;
}
```
运行结果
```
tag: thread-1 count: 1
tag: thread-1 count: 2
tag: thread-1 count: 3
tag: thread-2 count: 1
tag: thread-2 count: 2
tag: thread-2 count: 3
```

## 进程与线程

|               | 进程                               | 线程                       |
| ------------- | ---------------------------------- | -------------------------- |
| 资源/地址空间 | 独立地址空间(系统分配资源:内存 IO) | 共享当前进程地址空间和资源 |
| 健壮性        | 进程间不会相互影响                 | 线程崩溃会导致进程崩溃     |
| 上下文切换    | 存储PCB 寄存器存储 换页(TLB)       | 存储TCB 寄存器存储         |

状态一样: 就绪 阻塞 运行(+ 创建 结束)


### 上下文切换

| 进程                         | 线程               | 协程                         |
| ---------------------------- | ------------------ | ---------------------------- |
| 存储PCB 寄存器存储 换页(TLB) | 存储TCB 寄存器存储 堆栈(比协程大) | 寄存器(栈 ~~无栈/有栈协程~~) 用户级线程(没id 没有`task_struct`内核对象) |


## 参考

- [协程切换](https://zhuanlan.zhihu.com/p/220025846)