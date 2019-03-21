"""
Created by JH on 2018/9/8
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=81, threaded=True)
    #单进程，单线程；开启threaded为单进程，多线程
    #开启多进程 processes,默认为1



