#模型层，mvc中m
from sqlalchemy import Column, Integer, String
from app.models.base import db, Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))   #精装还是平装
    publisher = Column(String(50)) #出版社
    price = Column(String(20))
    pages = Column(Integer)   #页数
    puddate = Column(String(20)) #出版日期
    isbn = Column(String(15), nullable=False, unique=True)   #unique使isdn唯一
    summary = Column(String(1000))  #书籍简介
    image = Column(String(50))


    def sample(self):
        pass
