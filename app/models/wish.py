from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, desc, func
from app.models.base import db, Base
from sqlalchemy.orm import relationship

from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)    #赠送的书籍
    user = relationship('User')         #赠送人
    uid = Column(Integer, ForeignKey('user.id'))    #ForeignKey外键,数据库术语。
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))     数据库没有保存书籍的数据，不同此方法进行关联
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        withes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return withes

    @classmethod
    def get_gifts_count(cls, isbn_list):
        from app.models.gift import Gift
        # 根据传入的一组isbn，到Wish表中计算出某个礼物的Wish心愿数量
        count_list = db.session.query(
            func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False, Gift.isbn.in_(
                isbn_list), Gift.status == 1).group_by().all()
        # filter_by传入的是关键字参数，fliter需要接收一些条件表达式'=='
        # group_by和func一起用叫分组统计
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first


