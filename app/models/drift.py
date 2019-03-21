from app.libs.enums import PendingStatus
from app.models.base import Base
from sqlalchemy import Column, SmallInteger, Integer, String, Boolean, ForeignKey, desc, func


class Drift(Base):
    """
        一次具体的交易信息
    """
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))
    # 模型中有关联：每次查询时，关联的模型的信息都是最新的
    # 缺点1：没有忠实记录交易时的状态
    # 缺点2：关联查询需要查询多张表，查询速度慢
    # 模型中无关联：存在数据冗余
    # 可以合理的利用数据的冗余
    # 数据的不一致，减少查询次数
    # 比如淘宝购物：保存购物记录

    _pending = Column('pending', SmallInteger, default=1)

    @property   #数字类型转为枚举类型
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter  #枚举类型转为数字类型
    def pending(self, status):
        self._pending = status.value

    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')

