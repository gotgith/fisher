from flask import Blueprint, render_template

web = Blueprint('web', __name__)

@web.app_errorhandler(404)   #自定义404返回结果
def not_found(e):
    #AOP面向切面编程
    return render_template('404.html'), 404
    #也可以直接输入文本renturn '文本'

from app.web import book   #把导入放到web上面会出错
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
# from app.web import user   #有多少视图模块函数，都需要导入，否则不会执行