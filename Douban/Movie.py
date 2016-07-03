# -*- coding:utf-8 -*-
__author__ = "Leo Luo"

from bs4 import BeautifulSoup
import requests

BASE_URL = "https://movie.douban.com/"
LOGIN_URL = "https://accounts.douban.com/login"
LOGIN_DATA = { 'source':'movie',
                                'redir':'https://movie.douban.com/',
                                'form_email':'*******************',
                                'form_password':'*********************',
                                'login':'登录'}

session = requests.Session()
session.get(BASE_URL)

class Douban(object):
    def __init__(self):
        super().__init__()

    def login(self):
        r = session.post(LOGIN_URL, data=LOGIN_DATA)
        print(r.request.headers)
        print(r.text)

def main():
    d = Douban()
    d.login()

if __name__ == "__main__":
    main()
