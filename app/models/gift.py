from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, desc, func
from app.models.base import db, Base
from sqlalchemy.orm import relationship
from collections import namedtuple

from app.spider.yushu_book import YuShuBook

EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn']) #快速定义对象的方法

class Gift(Base):
    id = Column(Integer, primary_key=True)    #赠送的书籍
    user = relationship('User')         #赠送人
    uid = Column(Integer, ForeignKey('user.id'))    #ForeignKey外键,数据库术语。
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))     数据库没有保存书籍的数据，不同此方法进行关联
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        #根据传入的一组isbn，到Wish表中计算出某个礼物的Wish心愿数量
        count_list = db.session.query(
            func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,Wish.isbn.in_(
            isbn_list),Wish.status==1).group_by().all()
        #filter_by传入的是关键字参数，fliter需要接收一些条件表达式'=='
        #group_by和func一起用叫分组统计
        count_list = [{'count':w[0], 'isbn':w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    #对象代表一个具体的礼物
    #类代表礼物这个事物，是抽象的，不是具体的一个
    @classmethod
    def recent(cls):
        #链式调用
        #主体 Query
        #子函数filter_by等
        #first(),all()触发语句
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        #order_by排序, distinct 去重，去重前先用group_by分组
        return recent_gift


    # @classmethod
    # def get_wish_counts(cls):
    #     count_list =  db.session.query(
    #         func.count(Wish.id), Wish.isbn).filter(
    #         Wish.launched==False, Wish.isbn.in_(
    #         isbn_list), Wish.status==1).group_by(Wish.isbn).all()
    #     count_list = [EachGiftWishCount(w[0], w[1]) for w in count_list]
    #     return count_list
    #使用from collections import namedtuple方法快速创建对象