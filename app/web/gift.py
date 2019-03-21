from flask import current_app, flash, url_for, render_template
from werkzeug.utils import redirect
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.gift import MyGifts
from . import web
from flask_login import login_required, current_user

__author__ = 'JH'

@web.route('/my/gifts')
@login_required     #用户登录后才能使用的视图函数，还需要一个函数在user中
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyGifts(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.gifts)

@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # try:
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            #current_user是一个实例化的User模型，所以可以通过User取到当前用户的id，并赋给gift下的uid
            current_user.beans += current_app.config['BEANS_UPLOAD_BOOK']
            db.session.add(gift)
        #     db.session.commit()
        # except Exception as e:
        #     db.session.rollback()   #数据库回滚，防止前面程序出错后续程序也失败
        #     raise e
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    #撤销礼物
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(
        gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处在交易状态，请先前往鱼漂完成交易')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_BOOK']
            #赠送的鱼豆扣除
            gift.delete()
    return redirect(url_for('web.my_gifts'))




# from contextlib import contextmanager
# @contextmanager
# def book_mark():
#     print('《 ', end='')
#     yield
#     print(' 》', end='')
#
# with book_mark():
#     print('lalala',end='')    打印出来《lalala》



