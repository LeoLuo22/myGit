# -*- coding:utf-8 -*-
__author__ = "Leo Luo"

import requests

session = requests.Session()
session.get("https://movie.douban.com/")
login  = "https://accounts.douban.com/login"
data = {'source':'movie',
'redir':'https://movie.douban.com/',
'form_email':'leoluo22@gmail.com',
'form_password':'vampire.Leo123',
'login':'登录'}

r = session.post(login, data=data)
print(r.text)
