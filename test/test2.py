# 线程隔离 原理 字典保存数据
# 操作数据
# werkzeug local Local 字典
# LocalStack、Local、字典的意义
# Local使用字典的方式实现线程隔离
# LocalStack封装了Local， 实现了线程隔离的栈结构

# 对象使保存状态的地方
# 使用线程隔离的意义在于：使当前线程能够正确引用到它自己创建的对象，而不是引用到其它线程所创建的对象。



# 以线程ID号作为key的字典 -> Local -> LocalStack
# AppContext RequestContext -> LocalStack
# Flask -> AppContext  Request -> RequestContext
# current_app -> (LocalStack.top = AppContext  top.app = Flask)
# curren_app指向LocalStack下面的一个属性（top.app，Flask的核心对象），栈顶元素就是应用山下文
# request -> (LocalStack.top = RquestContext  top.request = Request)
# request指向LocalStack栈顶元素的属性Request

