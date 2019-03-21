"""
Created by JH on 2018/9/8
"""
from flask import Flask, make_response

app = Flask(__name__)
app.config.from_object('config')
print(app.config['DEBUG'])


@app.route('/hello')
#通过装饰器给hello函数定义一个路由，可以通过http请求访问到hello函数
# app.add_url_rule('/hello', view_func=hello) 另一种定义路由的方法，用于基于类的视图;route是这种方法的封装形式
def hello():
    #基于类的视图（即插视图）
    #视图函数除了返回字符串以外，还会返回附加信息。如1.status code 200,404,301等  2.content-type放置于http headers属性中
    #默认值content-type = text/html
    #视图函数会把内容返回成Response对象
    headers = {
        'content-type':'text/plain',
        #当视图工具的接口为小程序或APP提供数据，通常叫做API。API数据为json格式，改成application/json
        'location':'http://www.bing.com'
    }
    #response = make_response('<html></html>', 301)
    #response.headers = headers   不需要自己实现response,可以用下面的方式
    #return response
    return '<html></html>', 301, headers

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=81)
#0.0.0.0表示可以接受外网访问;config本身就是字典dict的一个子类


