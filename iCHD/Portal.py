# -*- coding:utf-8 -*-
__author__ = "Leo Luo"

import requests
import time
from bs4 import BeautifulSoup
import lxml
import collections
from PIL import Image
import string

HEAD  = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
BASE_URL = "http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F"#通过这个url获得lt
LOGIN_URL = "http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F"
AFFAIR_URL = "http://portal.chd.edu.cn/?.pn=p1143_p1144_p1131"#教务系统
TO_DO_URL = "http://portal.chd.edu.cn/pnull.portal?rar=&.pmn=view&.ia=false&action=informationAjax&.pen=information"
#captchaResponse:z8dc
session = requests.Session()

Flag = True

class Chd(object):

    def __init__(self, POST_DATA=None):
        super().__init__()
        POST_DATA = collections.OrderedDict()
        POST_DATA['username'] = ''
        POST_DATA['password'] = ''
        POST_DATA['btn'] = ''
        POST_DATA['lt'] = ''
        POST_DATA['dllt'] = 'userNamePasswordLogin'
        POST_DATA['execution'] = 'e1s1'
        POST_DATA['_eventId'] = 'submit'
        POST_DATA['rmShown'] = '1'
        self.__POST_DATA = POST_DATA

    @property
    def POST_DATA(self):
        return self.__POST_DATA

    @POST_DATA.setter
    def POST_DATA(self, value):
        self.__POST_DATA = value

    """**********************生成要发送的数据************************"""
    def create_post_data(self, username, password, flag):
        if flag == "no_captcha":
            r = session.get(BASE_URL)
            base = r.content.decode('utf-8')
            base_soup = BeautifulSoup(base,'lxml')
            lt = base_soup.find('input',attrs={'type':'hidden', 'name':'lt'})['value']#时间戳
            self.__POST_DATA['lt'] = lt
            self.__POST_DATA['username'] = username
            self.__POST_DATA['password'] = password
        elif flag == "captcha":
            r = session.get(BASE_URL)
            base = r.content.decode('utf-8')
            base_soup = BeautifulSoup(base,'lxml')
            lt = base_soup.find('input',attrs={'type':'hidden', 'name':'lt'})['value']
            payload = collections.OrderedDict()
            payload['username'] = username
            payload['_'] = lt
            self.get_captcha(payload)
            captcha = get_input("请输入验证码: ", "captcha")
            self.__POST_DATA['captcha'] = captcha
            self.__POST_DATA['lt'] = lt
            self.__POST_DATA['username'] = username
            self.__POST_DATA['password'] = password

        #print(self.POST_DATA)

    def get_captcha(self, payload):
        r = session.get("http://ids.chd.edu.cn/authserver/captcha.html", params=payload)
        captcha = r.content
        with open('captcha.png', 'wb') as fh:
            fh.write(captcha)
        im = Image.open('captcha.png')
        im.show()

    def login(self):
        contents = {}
        try:
            login = session.post(BASE_URL, params=self.POST_DATA, headers=HEAD)
        except requests.exceptions.TooManyRedirects as err:
            print("出现错误，请重新登录")
            Flag = False
            main()
            return 0
        login = login.content.decode('utf-8')
        contents["index"] = login
        """ FUCK
        soup = BeautifulSoup(login, 'lxml')
        soup = soup.find('a', attrs={'title':'最大化', 'class':'maximize'})['href']
        TO_DO_URL = "http://portal.chd.edu.cn/" + soup
        """
        r = session.get(TO_DO_URL, headers=HEAD)
        res = r.content.decode('utf-8')
        contents["to_do_info"] = res
        return contents

    def affair_login(self):
        affair_login = session.get(AFFAIR_URL)
        return affair_login.content.decode('utf-8')

    def show_user_img(self, user_img_url):
        img_raw = session.get(user_img_url, headers=HEAD)
        img = img_raw.content
        with open("1.jpg", "wb") as fh:
            fh.write(img)
        im = Image.open("1.jpg")
        im.show()

    def system_login(self):pass

"""
    def parse(self):
        def get_user_img(self):
            index = self.login()
            index_soup = BeautifulSoup(index, 'lxml')
            user_img_para = index_soup.find('img', attrs={"onerror":"this.src=\'images/defaultFace.jpg\'"})
            print(user_img_para)
"""
"""***********************************数据处理类****************************************"""
class Parse(object):

    def __init__(self, parse_content, user_info=None):
        self.parse_content = BeautifulSoup(parse_content, 'lxml')
        user_info = {}
        self.user_info = user_info

    @property
    def user_info(self):
        return self.__user_info

    @user_info.setter
    def user_info(self, value):
        self.__user_info = value

    def get_user_img_url(self):
        index_soup = self.parse_content
        try:
            user_img_para = index_soup.find('img', attrs={"onerror":"this.src=\'images/defaultFace.jpg\'"})["src"]
        except TypeError as err:
            print("出现错误, 请重新登录")
            main()
            return 0
        user_img_para = str(user_img_para).replace("amp;","")
        user_img_url = "http://portal.chd.edu.cn/" + user_img_para
        return user_img_url

    def get_user_info(self):
        whitespace = string.whitespace
        user_info_soup = self.parse_content
        #print(user_info_soup)
        _money = user_info_soup.find_all('span', attrs={'class':'msgTitle1 desc'})
        print(_money)
        try:
            name = user_info_soup.find('span', attrs={'style':'margin-bottom:5px;display:block;'}).string.split()
        except AttributeError as err:
            print("出现错误, 请重新登录")
            main()
            return 0
        department = user_info_soup.find('span',attrs={'style':'display:block;'}).string.strip(whitespace)
        department = department.replace("部门：","")
        self.__user_info["name"] = name[0]
        self.__user_info["department"] = department
        #print(name)

    def get_other_info(self):
        other_soup = self.parse_content
        all_info = other_soup.find_all('span', attrs={'class':'info-detail'})
        _money_raw = all_info[2]
        _money = _money_raw.find('font').string
        self.user_info['money'] = _money



def get_input(msg,  _type):
    if _type == 'username':
        while  True:
            username = input(msg)
            if len(username) != 12 or  not username.isdigit():
                print("输入有误， 请重新输入")
                continue
            break
        return username

    elif _type == "password":
        password = input(msg)
        return password

    elif _type == "seq_num":
        while True:
            seq_num = input(msg)
            if len(seq_num) == 0:
                return None
            seq_num = int(seq_num)
            if seq_num not in range(0,5):
                print("输入有误")
                continue
            break
        return seq_num

    elif _type == "captcha":
        while True:
            captcha = input(msg)
            if len(captcha) != 4 or len(captcha) == 0:
                print("输入有误，请重新输入")
            else:
                return captcha

def init():
    Flag = not Flag


def main():
    if Flag == True:
        user = Chd()
        username = get_input("请输入用户名: ","username")
        password = get_input("请输入密码: ","password")
        user.create_post_data(username, password, "no_captcha")
        #user.get_captcha()
        contents  = user.login()
        parser = Parse(contents['index'])
        #user_img_url = parser.get_user_img_url()
        #print(user_img_url)
        #option = input("请选择是否显示头像: (y/n)")
        """
        if option == 'y' or option == "Y":
            user.show_user_img(user_img_url)
        else:
            pass
            """
        parser.get_user_info()
        other = Parse(contents["to_do_info"])
        other.get_other_info()
        print("你当前校园卡的余额为: {0}".format(other.user_info['money']))
    else:
        user = Chd()
        username = get_input("请输入用户名: ","username")
        password = get_input("请输入密码: ","password")
        user.create_post_data(username, password, "captcha")
        #user.get_captcha()
        contents  = user.login()
        parser = Parse(contents['index'])
        #user_img_url = parser.get_user_img_url()
        #print(user_img_url)
        #option = input("请选择是否显示头像: (y/n)")
        """
        if option == 'y' or option == "Y":
            user.show_user_img(user_img_url)
        else:
            pass
            """
        parser.get_user_info()
        other = Parse(contents["to_do_info"])
        other.get_other_info()
        print("你当前校园卡的余额为: {0}".format(other.user_info['money']))

if __name__ == "__main__":
    main()
