from flask import Flask
from app.models.book import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

def create_app():   #插件注册
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)   #初始化login_manager
    login_manager.login_view = 'web.login'
    #把登陆页面的视图函数的endpoint返回给login_view，让flask_login插件找到登录的视图函数
    login_manager.login_message = '请先登录或注册'   #把提示信息改为中文

    mail.init_app(app)

    with app.app_context():
        db.create_all()  #让slqalchemy可以把所有的数据模型映射到数据库里去，不调用这句话就不会生成数据表
    return app

def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
