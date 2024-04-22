---
title: "Nginx Location Trans"
date: 2024-04-22T12:49:52+08:00
description: Simple Nginx location guide. A translation from official docs
categories: ["nginx",  "introduction", "operation"]
layout: archives
tags: ["develop"]
---

# [location][location]

> 可以从 [nginx-playground][playground] 的报错看见真实的本地请求路径

```nginx
location [ = | ~ | ~* | ^~ ] uri { ... }
location @name { ... }
```

> 设置依赖的请求 URI
>
> 尾部有 `/` 表示目录 否则表示文件 获取失败可能会导致重定向

地址可以被定义为 **前缀字符串**(prefix string) 或者 **正则表达式**(regular expression)
- `~*` 大小写无关正则匹配 (case-insensitive)
- `~` 大小写相关正则匹配 (case-sensitive)

标准匹配
- `` (无符号)前缀匹配
- `=` 指定匹配
- `^~` 一般匹配路径

匹配逻辑
1. 首先检查前缀串
2. 然后检查正则项


## [root][root]

`root` 会将匹配到路径拼接到根下

```nginx
location /i/ {
  root /data/w3;
  # root /data/w3/; # <-- 这俩一样
}
```

`/i/top.gif` 会请求本地资源 `/data/w3/i/top.gif`

## [alias][alias]

`alias` 定义了匹配路径的替换项 如果匹配路径与最后一级实际路径相同 建议使用 `root`

```nginx
location /i/ {
  alias /data/w3/images/;
}
```

`/i/top.gif` 会请求 `/data/w3/images/top.gif`

> 注意最后的分隔符 `alias /data/w3/images;` 会匹配到 `/data/w3/imagestop.gif`

## [proxy_pass][proxy_pass]

```nginx
location /prefix {
  proxy_pass http://localhost:8080;
}

location /path/ {
  proxy_pass http://localhost:8081;
}

location /part {
  proxy_pass http://localhost:8082/;
}

location /part {
  proxy_pass http://localhost:8082/part; # <-- 类似于 alias
}

location /middle/ {
  proxy_pass http://localhost:8083/;
}

location /name {
  proxy_pass http://127.0.0.1:8084$request_uri;
}
```

在匹配时 路径与文件是有差异的

```
[0]: /prefix/a/s.xml -> http://127.0.0.1:8080/prefix/a/s.xml
[1]: /path/a/s.xml -> http://127.0.0.1:8081/path/a/s.xml
[2]: /part/a/s.xml -> http://127.0.0.1:8082//a/s.xml
[3]: /part/a/s.xml -> http://127.0.0.1:8082/part/a/s.xml
[4]: /middle/a/s.xml -> http://127.0.0.1:8083/a/s.xml
[5]: /name/a/s.xml -> http://127.0.0.1:8084/name/a/s.xml
```

在写 `proxy_pass` 指令时 当 proxy uri 不带路径时 会将整个请求路径添加到转发请求中

此外的话 其行为类似于 `alias` 将匹配剩余部分拼接到转发地址中

```
location /prefix { proxy_pass http://localhost:8080/a; }
  /prefix/a/s.xml -> :8080/a/a/s.xml
  接取匹配后剩余内容 /a/s.xml 拼接到 :8080/a 之后

location /middle/ { proxy_pass http://localhost:8083/a/; }
  /middle/a/s.xml -> :8083/a/a/s.xml
```

[location]: https://nginx.org/en/docs/http/ngx_http_core_module.html#location
[location-examples]: https://www.digitalocean.com/community/tutorials/nginx-location-directive
[location-zh]: https://zhuanlan.zhihu.com/p/130819099
[root]: https://nginx.org/en/docs/http/ngx_http_core_module.html#root
[alias]: https://nginx.org/en/docs/http/ngx_http_core_module.html#alias
[playground]: https://nginx-playground.wizardzines.com/
[proxy_pass]: https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass