#urllib
#requests   发送http请求

# from urllib import request
import requests

class HTTP():
    @staticmethod     #get为静态方法，把self去掉，加装饰器即可。classmethod也可表示静态方法
    def get(url, return_json = True):
        r = requests.get(url)
        #大部分网站restful 为jason格式
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text     #简介


        # if r.status_code == 200:    #直白写法
        #     if return_json:
        #        return r.json()
        #     else:
        #        return r.text
        # else:
        #    if return_json:
        #       return {}
        #    else:
        #         return ''


