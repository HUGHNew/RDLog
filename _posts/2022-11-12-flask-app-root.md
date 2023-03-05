---
layout: base
title:  "app root path for flask"
categories: develop
tags: flask python nginx
---

本文介绍简单的 `Flask` 应用通过 `Blueprint` 给整个应用设置应用根目录的方法

主要是通过 `Blueprint` 的 `url_prefix` 和 Flask app 的 `static_url_path` 来完成设置的

<!--more-->
## static prefix

在默认的情况下 Flask 应用的使用的**本地静态路径**为应用目录下的`static` **远程路径**(通过HTTP访问)为`/static`

Flask 应用可以通过两个变量 `static_folder`(static) 和 `static_url_path`(/static) 来分别设置本地和远端的路径 前面括号内为变量的默认值

例如

```python
""" 目录结构
.
├── app.py
├── 2.jpg
"""
app = Flask(__name__, static_url_path="/base/static", static_folder="./")
```

访问 `127.0.0.1:5000/base/static/2.jpg` 就能获得 `./2.jpg` 这张图片

## API prefix

静态资源的问题解决了 剩下的就是 API 调用的问题了

`app.config["APPLICATION_ROOT"] = prefix` 似乎没有用 所以不想给全部API手动写的话 就需要使用 `Blueprint` 了

```python
from flask import Blueprint, Flask

bp = Blueprint("bp_name", __name__, url_prefix="/base")

@bp.route('/',methods=['GET','POST']) # 注意这里不是 app.route
def index():
  return "hello"

app = Flask(__name__)
app.register_blueprint(bp)
```

`Blueprint` 的简单使用如上 可以直接写在 app.py 中

之后访问 `127.0.0.1/base` 就能获得 hello 了

### render_template 中使用

不过在 render_template 中使用的时候需要注意

```html
<a href="{{ url_for('bp_name.index')}}">About</a>
```
例如之前使用的`Blueprint`名为 `bp_name` 如果使用的template的话 需要在 `url_for` 里面添加 blueprint 名(如果嵌套的话就顺序使用 如`parent.child.index`)

## 示例

```
.
├── app.py
├── blue.py
├── static
│   └── 2.jpg
└── templates
    ├── base.html
    └── index.html
```

`blue.py` 是蓝图的具体代码 可以单独放在一个文件里面

```python
from flask import Flask
from blue import bp

app = Flask(__name__, static_url_path="/base/static", static_folder="/static")
app.register_blueprint(bp)
if __name__=="__main__":
    app.run("127.0.0.1", 8080, True)
```

```python
# blue.py
from flask import Blueprint, render_template

bp = Blueprint("bp", __name__, url_prefix="/base")

@bp.route('/',methods=['GET','POST'])
def index():
    return render_template("index.html")
@bp.route('/base')
def test_base():
    return "base path"
```
下面只截取了相关的代码

{% highlight html %}
<!--templates/base.html-->
<a class="navbar-brand" href="{ { url_for('bp.index') } }">About</a>
<!-- Jekyll Liquid 语法问题 忽略双大括号之间的间隔  -->
{% endhighlight %}

{% highlight html %}
<!--templates/index.html--->
<img src="{ {url_for('static', filename='2.jpg')} }" >
<!-- Jekyll Liquid 语法问题 忽略双大括号之间的间隔  -->
{% endhighlight %}

> 访问 127.0.0.1/base 可以访问到index.html 并且正常获取图片

> 访问 127.0.0.1/base/base 可以得到 "base path"