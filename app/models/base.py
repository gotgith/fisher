from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer
from contextlib import contextmanager




class SQLAlchemy(_SQLAlchemy):
    @contextmanager    #中途跳转去执行其他代码，再回来执行下面代码
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            # 数据库回滚，防止前面程序出错后续程序也失败
            raise e

class Query(BaseQuery):
    def filter_by(self, **kwargs):   #kwargs字典，**kwargs解包字典
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query,self).filter_by(**kwargs)
        #调用基类被覆盖的里面原有的filter_by逻辑

db = SQLAlchemy(query_class=Query)
#替换原有的Query使用参数query_class


class Base(db.Model):   #基类模型，让子模型去继承
    __abstract__ = True    # 让sqlalchemy不是创建表
    create_time = Column('create_time', Integer)
    # 不能在此处记录时间，因为这是类变量生成的时间，发生在整个类创建的过程中
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())
        #对象实例化，timestamp时间戳

    def set_attrs(self, attrs_dict):
        for key,value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                #判断某个对象下面是否包含某个属性
                setattr(self, key, value)
                #动态赋值，1参数：对那个对象进行赋值，2：对那个属性进行赋值，3：赋值

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0
