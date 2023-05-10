# 浏览器和搜索引擎

> 为防止QQ把我内容干了 下文所有网址把 . 替换为 |

浏览器决定了网页使用的体验

搜索引擎决定了网页检索的效率

## 浏览器

现在来看(2023/05) 随着NewBing和Bard的放开 Edge在两三年前已经并入chromium阵营

现在桌面端的通用浏览器 似乎只有Edge和Chrome可选了 (Android还能用用Via这些轻量级浏览器)

这里的通用浏览器指没有特殊需求情况下 可以日常使用的浏览器

chromium的优势在于差不多已经成为了新的事实上的标准 一些老旧网站直接从IE转向了Chrome 基于chromium内核 似乎成为了必选

Edge的优势在于NewBing 现在也正在与NewBing进行深度集成 在尝试下放功能让NewBing直接调用 见Twitter@bing的新动向 不过Edge在Windows10下有时候会整个黑掉然后重新绘制UI 不如Chrome稳定 所以我选择Chrome

Chrome就属于老牌浏览器了 登录Google账号 密码同步和标签页同步 想去哪儿就去哪儿

其他一些选择就是开源的Firefox 在Linux上占点份额 最大的优势就是开源

或者选择Tor 使用更难追踪的匿名网络

或者轻量的Yandex

## 搜索引擎

主流搜索引擎不算太多

在NewBing之前 我主要还是用Bing cn|bing|com在大多数时候的搜索结果还可以 同时在不使用任何插件的情况下 没有那么多广告

不过现在NewBing上线 微软更积极收集用户数据 对于Bing的每条结果都增加了www|bing|com/ck/a 同时隐藏了原网址 此外Bing的重定向还可能很慢 需要手动点击跳转

这个东西现阶段还不能关 那么就不要再使用Bing 除了NewBing

淘汰掉此前的中间选项Bing 那么内有百度 外有Google AI搜索上NewBing 开源有DuckDuckGo 搜索引擎的选择 似乎结束了

不过还有一小点内容
- 优化百度体验
- Chrome上使用NewBing
- 快捷使用多个搜索引擎

### 百度优化

1. 安装 Tampermonkey
2. GreasyFork上搜索 AC-baidu-重定向 插件并安装
3. 恭喜你获得了更好的百度体验

### NewBing in Chrome

1. 安装 User-Agent Switcher and Manager
2. 对于 www|bing|com 添加 Edge的UA
3. enjoy your own NewBing
4. (美国的NewBing可以画图)

### Search engines

1. Chrome 设置 -> 搜索引擎
2. 添加NewBing: 快捷键使用`b` 网址为`www|bing|com/search/?q=%s&showconv=1`
3. NewBing有概率不直接将搜索内容作为第一条发送的内容
4. 无所谓 在search和chat之间切换一下 你就能找到之前搜索的内容了
5. 添加其他搜索引擎的方法一样