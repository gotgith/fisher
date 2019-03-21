#放一些数据库配置类似的机密配置，不可放置到git上面。开发和生产不同
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@localhost:3306/fisher'   #cymysql数据库操作驱动
SECRET_KEY = "jianghao123/jianghao123/jianghao1233"

#Email配置
MAIL_SERVER = 'smtp.qq.com'   #电子邮箱服务器地址
MAIL_PORT = 465    #qq的端口
MAIL_USE_SSL = True   #使用SSL协议
MAIL_USE_TSL = False
MAIL_USERNAME = '598914360@qq.com'
MAIL_PASSWORD = 'xkqxxjirigdobbih'   #不是qq密码  ，是账户配置的授权码
MAIL_SUBJECT_PREFIX = '[鱼书]'
MAIL_SENDER = '鱼书 <hello@yushu.im>'    #邮件发送，一般设置为企业邮箱