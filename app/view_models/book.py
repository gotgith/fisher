#gift,book,drift三种类模型，推荐book模型，清晰
#drift虽简单，但阅读性差
class BookViewModel:    #单本数据
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        self.author =  '、'.join(book['author'])
        self.price = book['price']
        self.isbn = book['isbn']
        self.summary = book['summary']
        self.image = book['image']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    #用使用属性的方式调用函数，省去（）；
    # 对象的俩个特性1，数据是用来描述特征，方法和函数用来描述行为
    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        # filter过滤器，存在则保留，不存在则提出
        return ' / '.join(intros)


class BookCollection:   #一组单本数据
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]

class _BookViewModel:
    #一个类变量要描述自己的特征（类变量、实例变量），其次还要有自己的行为（方法）
    #只有方法是面向过程，类是面对对象的基本单位， 函数是面对过程的基本单位
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books':[],
            'total':0,
            'keyword':keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
            return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
            return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title':data['title'],
            'publisher':data['publisher'],
            'pages':data['pages'] or '',
            'author':'、'.join(data['author']),
            'price':data['price'],
            'summary':data['summary'] or '',
            'image':data['image']
        }
        return book