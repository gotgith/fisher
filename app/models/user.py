from math import floor
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import db, Base
from flask_login import UserMixin    #UserMixin里面定义了login的默认属性，可以继承来用
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook

class User(UserMixin, Base):
    #__tablename__ = ‘lala’ 更改表名
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)   #使存在数据库的名字为password
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property      #属性读取，把一个方法变成一个属性    一个属性的get
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):   #属性写入    一个属性的set
        self._password = generate_password_hash(raw)    #加密方式
        #可完成只读模式的操作，方法是;不进行赋值操作，并进行错误警告提醒

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False


    def check_password(self, raw):
        return check_password_hash(self._password, raw)
        #同时进行密码的加密和对数据库数据的对比

    # def get_id(self):
    #     return self.id1   如果用户识别名不一样，可以用同名函数来覆盖父类里面的相关函数

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':   #查看isbn号是否符合规范
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)    #查看符合规范的isbn是否存在
        if not yushu_book.first:
            return False
    #不允许一个用户同时赠送多本相同的图书
    #一个用户不可能同时成为赠送者和索要者
    #既不在赠送清单，也不在心愿清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    #功能1：记录用户的ID号， 2：需要经过加密
    def generate_token(self, expiration=600):#expiration保存时间
        s = Serializer(current_app.config['SECRET_KEY'], expiration)  #序列化器
        return s.dumps({'id':self.id}).decode('utf-8')
        #把数据写入序列化器中，转换成utf-8格式字符串

    #读取token里面的用户id
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:   #token过期或伪造的鉴定
            data = s.load(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)    #模板主键可以用get
            user.password = new_password
        return True

    @property
    def summary(self):   #用户简介信息
        return dict(
            nickname = self.nickname,
            beans = self.beans,
            email = self.email,
            send_receive = str(self.send_counter) + '/' + str(self.receive_counter)
        )

@login_manager.user_loader    #使login能调用此函数
def get_user(uid):   #一个独立的函数.返回用户的用户模型
    return User.query.get(int(uid))   #id使用户的主键，不需要用filter_by
