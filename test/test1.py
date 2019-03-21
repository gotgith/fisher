#资源是稀缺的
#计算机资源  竞争计算机资源
#进程
#至少有1个进程
#进程是竞争计算机的基本单位

#单核CPU只能执行一个进程，但是可以在不同的应用程序之间切换
#在多核CPU中，存在进程调度 ，算法， 挂起 切换到另一个进程
#进程/线程 相互切换开销非常大；  上下文，程序的切换需要保存和重新运行


# 线程
# 线程是进程的一部分，可以有一个线程和多个线程
# CPU 进程粒度大，不能充分理由CPU的高性能，需要更小的单元管理CPU的单元
# 进程分配资源， 内存资源
# 线程是利用CPU执行代码
# 代码既是指令，需要CPU来执行  操作资源但不拥有资源
# 线程访问资源
#线程属于进程，线程访问线程的资源


#python不能充分利用多核CPU优势，因为有GIL
#GIL机制：全局解释器索 global interpreter lock
#锁：线程安全
#内存资源   一个进程有多个线程共享，这样会引起线程不安全
#
#细粒度锁 程序员主动加锁
#粗粒度 在解释器层面上加锁 GIL； 多核CPU 1个线程执行，一定程度上保证线程安全



#CPU密集型程序：线程严重依赖CPU计算
#IO密集型程序：查询数据库、请求网络资源、读写文件
