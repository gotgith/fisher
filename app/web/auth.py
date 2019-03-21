from flask import render_template, request, redirect, url_for, flash
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.base import db
from app.models.user import User
from . import web
from flask_login import login_user, logout_user

__author__ = 'JH'


@web.route('/register', methods=['GET', 'POST'])
#GET获得申请页面，POST传输用户申请数据到数据库
def register():
    form = RegisterForm(request.form)
    #request.form接收‘POST’传来的表单数据
    if request.method == 'POST' and form.validate():
        #验证信息通过，存入数据库
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
            #db.session.commit()    #使用ORM思想把数据写进数据库
        return redirect(url_for('web.login'))   #redirect重定向，切换页面
    return render_template('auth/register.html', form=form)
    #错误提示，输入重现都存在form中，故把form当成渲染的数据


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            #把用户的票据信息保存到cookie中.remember实现免登录，保存cookie
            next = request.args.get('next')
            #request.args可以获取？后面的查询参数
            #http://localhost:81/login?next=%2Fmy%2Fgifts
            # next后面记录的是要跳转回去的页面地址
            if not next or not next.startswith('/'):
                #next.startswith('/')判断next是否以/开头
                next = url_for('web.index')
            return redirect(next)    #redirect重定向
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)

@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email = account_email).first_or_404()
            #first_or_404,如果user不存在，后续代码就不会执行，返回一个NOTFOUND页面
            from app.libs.email import send_mail
            send_mail(form.email.data, '重置你的密码',
                      'email/reset_password.html',
                      user=user,token=user.generate_token())
            flash('一封邮件已发送到邮箱' + account_email + ', 请及时查收')
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('你的密码已更新，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
