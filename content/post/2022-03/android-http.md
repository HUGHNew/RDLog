---
title: "Android Http"
date: 2022-03-13T22:05:40+08:00
description: Android 明文通讯
categories: ["Android"]
layout: search
tags: ["develop"]
---

# Android 使用HTTP明文通信

> 对于自己的测试用网站 弄个SSL证书也是比较麻烦 所以使用HTTP明文通信
> 
> 但 Android8.1 之后 默认关闭明文通信
> 
> Starting with Android 9 (API level 28), cleartext support is disabled by default.

## 创建 network_security_config 配置

创建文件 `res/xml/network_security_config.xml`

下列两个配置任选一个

### 指定通行域名

指定域名

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">api.example.com(to be adjusted)</domain>
    </domain-config>
</network-security-config>
```

### 全域通行

```xml
<network-security-config>
    <base-config cleartextTrafficPermitted="true">
    </base-config>
</network-security-config>
```

## 更改 AndroidManifest

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest android:targetSandboxVersion="1"
    ...>
    <uses-permission android:name="android.permission.INTERNET" />
    <application
        ...
        android:networkSecurityConfig="@xml/network_security_config"
        android:usesCleartextTraffic="true"
        ...>
        ...
    </application>
</manifest>
```

## 参考

- [Android8 允许HTTP明文](https://stackoverflow.com/questions/45940861/android-8-cleartext-http-traffic-not-permitted)
- [网络安全配置](https://developer.android.com/training/articles/security-config?hl=zh-cn#FileFormat)