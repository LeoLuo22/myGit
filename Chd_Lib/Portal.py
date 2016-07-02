# -*- coding:utf-8 -*-
#__author__: Leo Luo

import requests
import time

HEAD  = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
BASE_URL = "http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F"
LOGIN_URL = "http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F"
DATA = {'username':'201324020211',
                'password':'vampire.Leo123',
                'btn':'',
                'lt':'LT-94934-dCxGwve0H0XRGe53AicAb7RoBGn16C1467425811376-vfDM-cas',#一部分由时间戳构成
                'dllt':'userNamePasswordLogin',
                'execution':'e1s1',
                '_eventId':'submit',
                'rmShown':'1'
                }

class Chd(object):

    def __init__(self, session=None):
        super().__init__()
        self.session = session

    def create_session(self):
        session = requests.Session()
        session.get(BASE_URL)
        self.session = session

    def login(self):
        self.create_session()
        r = self.session.post(BASE_URL, params=DATA, headers=HEAD)
        print(r.request.headers)
        print(r.headers)
        #print(r.text)

def main():
    a = Chd()
    a.login()

if __name__ == "__main__":
    #main()
    print(str(int(round(time.time() * 1000))))
    print(len(str(int(round(time.time() * 1000)))) == len("1467425811376"))

