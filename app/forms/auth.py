from wtforms import StringField, PasswordField, Form
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8,64), Email(
            message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(
        message='密码不可以为空，请输入你的密码'), Length(6,32)])
    nickname = StringField(validators=[DataRequired(), Length(
        2,10,message='昵称最少俩个字符，最多十个字符')])

    #validators为验证器
    #自定义的验证器不需要加入到validate数组中，会自动识别下划线之后要验证的东西
    def validate_email(self, field):
        #自定义验证器以validate开头. field是由wtform传入，是客户端传来的email参数
        if User.query.filter_by(email=field.data).first():
        #数据库遍历查询，比session更快.加data才能去到数据.
        # first触发查询操作，不管查询出来多少条，只返回一条
            raise ValidationError('电子邮件已被注册')  #wtform中特定异常提示

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')

class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])

class LoginForm(EmailForm):
    password = PasswordField(validators=[DataRequired(
        message='密码不可以为空，请输入你的密码'), Length(6,32)])

class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32, message='密码长度至少需要6到32个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
        #EqualTo对比
    password2 = PasswordField(validators=[
        DataRequired(), Length(6,32)])