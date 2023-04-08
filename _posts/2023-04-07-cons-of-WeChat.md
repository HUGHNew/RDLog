# Stupid WeChat

先谈一点别的 目前我觉得微信正常IM功能并不是其重心 只是个最低限度可用的东西罢了 这方面的改动对于日活和用户量的提升几乎为零 但是什么小程序 第三方功能集成可就不一样了

> 如果可以的话 我更喜欢现在的微信拆分为IM+小程序+钱包+第三方工具的松散联邦 这样我就可以直接用支付宝当电子钱包了

之后主要从以下几点 简单说一下为什么我不喜欢微信

- 客户端平台支持
- 文件下载
- 数据清理
- 聊天体验

## 平台支持

> 腾讯就没想过做Linux客户端 毕竟是不挣钱又小众的玩意儿
>
> 我还是比较期待Electron WeChat

现在对于Linux 腾讯官方支持
- Deepin-WeChat 似乎一个版本是Wine 一个版本是Web版开放登录
- 支持[优麒麟WeChat][ukylin-wechat] 其实也是Wine 不过deb包 不够简陋得只剩了UI和文字聊天 连最近消息同步都没有

一些其他方案
- 虚拟机
- Wine
- [Wine-Appimage][Wine-AppImage]
- 偷吃Deepin-WeChat

QQ今年都等到了Electron封包Appimage 普惠Linux系统 目前3.1版本也差不多稳定 只是偶尔漏几条消息

## 文件下载

下载文件与多份存储

微信下载文件后在Android上默认存储在`Android/data/com.tencent.mm/MicroMsg/Download`路径下 不过这只是自动下载的文件 一般要用还需要手动存一份 但是它的逻辑又是在这个默认存储路径里面查找的 就导致一般文件大概率会存两份(这下双倍占用空间了)

上述问题似乎还好 但是发送的数据也会在存储聊天记录时多次储存就比较乐了

好消息是微信更新了 优化了大家能够直接看到和操作微信文件的问题 [来源][mm-data]

在以下两个版本
- Android 8.0.28
- Windows 3.9.0

Android是将文件放入了应用私有路径下 非ROOT用户不可见了

Windows是默认文件是只读文件 大大恶心了用户

类似问题iOS也存在 详见[科技老男孩视频][iOS-wc]

## 聊天体验

懒得写了 反正只是能用 期望微信改也是不可能的

## 其他

数据清理问题: WeChat本身的数据清理似乎只是一个摆设 [来源][mm-storage]

朋友圈时间稍微短一点的视频不显示进度条也不能暂停

语音消息不能拉进度条

[ukylin-wechat]: https://www.ubuntukylin.com/applications/106-cn.html
[Wine-AppImage]: https://github.com/Hackerl/Wine_Appimage
[iOS-wc]: https://www.bilibili.com/video/BV1UG411V7vm
[mm-data]: https://www.bilibili.com/video/BV1C84y1K7q2/
[mm-storage]: https://www.bilibili.com/video/BV1UG4y1a75w/
