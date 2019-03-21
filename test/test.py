from flask import Flask, current_app, request, Request

app = Flask(__name__)
# 应用上下文 是对Flask的封装
# 请求上下文  是对Request的封装 ；在封装后提供了一些好用的方法；上下文就是一种封装
# Flask的核心对象存储在AppContext中
# Request   RequestContext
# 离线应用、单元测试需要手动推入Requestcontext。而在逻辑代码在视图函数中不需要，因为flask会帮助推入
# ctx = app.app_context()   #返回的是核心对象app
# ctx.push()   #入栈
# a = current_app
# d = current_app.confit['DEBUG']
# ctx.pop()   #出栈
# 用with语句代替上面代码。with语法糖，把push和pop放在了__enter__和__exit__中,返回AppContext
# 对一个实现了上下文协议的对象使用with
# 实现了上下文协议的对象叫做上下文管理器
# 上下文管理器通过对象实现__enter__和__exit__方法就是实现了上下文协议
# with语句后面是上下文表达式，上下文表达式必须要返回一个上下文管理器

with app.app_context():  # app_context返回的是AppContext
    a = current_app
    d = current_app.confit['DEBUG']


# 1.连接数据库
# 2.  sql语句
# 3.释放资源
# 把连接数据库的语句写进上下文管理器的__enter__中
# 把操作数据库的逻辑代码写进with中
# 释放资源的代码写进__exit__中

# 文件读写
# try:
#     f = open(r'D:\t.txt')
#     print(f.read())
# finally:
#     f.close()
# 用with语句改写
# with open(r'') as f:   上下文管理器的__enter__方法返回的值赋予f
#     print(f.read())


# class MyResource:
#     def __enter__(self):
#         print('connect to resource')
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print('close resource connection')
#         return Flase             返回只有Flase和True ，默认Flase.Flase还要在外部显示错误提示
#     def query(self):
#         print('query data')
#
#
# with MyResource() as resource:
#     1/0
#     resource.query()
