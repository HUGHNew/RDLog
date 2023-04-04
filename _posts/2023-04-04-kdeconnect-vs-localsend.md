# KDEConnect vs. LocalSend

## [KDEConnect][kdeconnect]

背靠KDE 面向全平台(Linux/Windows/macOS/iOS/Android) 对于Gnome有特别支持:[GSConnect](https://extensions.gnome.org/extension/1319/gsconnect/)

主要功能
- 剪切板互传
- 文件传输
- 挂载手机文件系统
- 远程输入和控制
- ...

优势在于可以开机自启挂后台 可以几乎无感使用剪切板互传(PC->Mobile) 但是Mobile->PC还是需要自己点一下

其他一些问题主要是正常切换网络环境之后连接不稳定
- 文件传输的连接不稳定
- 文件系统挂载不稳定

似乎重启应用能解决

## [LocalSend][localsend]

基于Flutter的全平台应用 有类似苹果产品的AirDrop体验

可以传输文本和文件 但是需要打开软件手动点 显得稍微麻烦一点 不过好处在于连上就是稳定的 也方便控制内容的传输 比手动`adb pull/push`舒服

[kdeconnect]: https://kdeconnect.kde.org/
[localsend]: https://github.com/localsend/localsend