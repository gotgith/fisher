from threading import Thread

from flask import current_app, render_template, flash

from app import mail
from flask_mail import Message

def send_asyns_email(app, msg):
    with app.app.context():
        try:
            mail.send(msg)
        except Exception as e:
            pass

def send_mail(to, subject, template, **kwargs):
    #to用户邮件，bubject邮件标题，template模板名称，**kwargs是传入的template的一组参数
    # msg = Message('测试邮件', sender='598914360@qq.com', body='Test',
    #               recipients=['598914360@qq.com'])   #recipients发向的邮箱
    msg = Message('[鱼书]' + '' + subject, sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    app =current_app._get_current_object()  #取到真实核心对象app
    #current_app代理核心对象，受到线程id影响单线程。
    # app=flask()flask核心对象，多线程都可用
    thr = Thread(target=send_asyns_email, args=[app, msg])
    #加入另一个线程，使邮件异步发送,args是向另一个线程传递（一组）参数
    thr.start()

