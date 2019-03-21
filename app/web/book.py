"""
 Created by JH on 2018-10-9.
"""
from flask import jsonify, request, current_app, url_for, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
import json

from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo
from . import web

__author__ = 'JH'


@web.route('/book/search')
def search():
    """
        q :普通关键字 isbn
        page
        ?q=金庸&page=1
    """

    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts =False
    has_in_wishs = False

    #取数据详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:   #用户必须登录，赠送和心愿清单处理，is_..=True是登录状态
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishs = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishs = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_wishs_model = TradeInfo(trade_wishs)
    trade_gifts_model = TradeInfo(trade_gifts)
    return render_template('book_detail.html',
                           book=book, wishes=trade_wishs_model,gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_wishs=has_in_wishs)
    #数据渲染，填充html模板




# @web.route('/test')
# def test():
#     r = {
#         'name': None,
#         'age': 18
#     }
#     # data['age']
#     r1 = {
#
#     }
#     flash('hello,qiyue', category='error')
#     flash('hello, jiuyue', category='warning')
#     # 模板 html
#     return render_template('test.html', data=r, data1=r1)

# @web.route('/test1')
# def test1():
#     print(id(current_app))
#     from flask import request
#     from app.libs.none_local import n
#     print(n.v)
#     n.v = 2
#     print('-----------------')
#     print(getattr(request, 'v', None))
#     setattr(request, 'v', 2)
#     print('-----------------')
#     return ''
