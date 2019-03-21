"""
用于判断是isbn和关键字
"""
def is_isbn_or_key(word):
    # isbn  isbn13是由13个从0-9的数字组成；isbn10 是由10个从0-9的数字组成，但含有一些"_"
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():  # insdigit函数是判断是否全为数字
        isbn_or_key = 'isbn'
    short_word = word.replace('_', '')
    if '_' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key
