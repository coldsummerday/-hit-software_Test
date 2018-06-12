
## 使用说明

不确定windows系统能不能正常使用

只在mac跟linux下进行测试
要求电脑安装python3

在webDemo目录下开启终端

```
python3 -m http.server --cgi
```

浏览器输入:

```
http://localhost:8000/calendar.html
```

原理:

* 利用python-cgi,在web前端调用后台脚本
* jQuery的post异步请求渲染部分html元素实现按钮功能


