# -*- coding:utf-8 -*-
#__author__: Leo Luo

import requests
from bs4 import BeautifulSoup
import lxml
import collections
import os

BASE_URL = "http://wiscom.chd.edu.cn:8080/opac/item.php"

class Books():
    def __init__(self, header=None, filename=None):
        self.__header = header
        self.filename = filename

    def generate_payload(self):
        payload = collections.defaultdict()
        value = "0000198282"
        key  = "marc_no"
        payload[key] = value
        return payload

    def get_filename_and_url(self):
        result = []
        payload = self.generate_payload()
        filename_session = requests.Session()
        r = filename_session.get(BASE_URL, params=payload)
        base_soup = r.content.decode('utf-8')
        soup = BeautifulSoup(base_soup, 'lxml')
        test  = soup.find('dd')
        title = test.a.string
        test.a.decompose()
        name  = test.string.replace("/", "_")
        filename = title + name
        result.append(filename)
        douban_url = soup.find_all('a',attrs={'target':'_blank'})
        for url in douban_url:
            d_u = url.get('href')
            if not d_u.endswith('/'):
                continue
            douban = d_u
        d = requests.get(douban)
        d_soup = d.content.decode('utf-8')
        douban_soup = BeautifulSoup(d_soup, 'lxml')
        pic_url = douban_soup.find('a', attrs={'class':'nbg'})['href']
        result.append(pic_url)
        return result

    def get_img(self,result):
        print(result)
        douban = result[1]
        filename = result[0]
        douban_session = requests.Session()
        d = douban_session.get(douban)
        content = d.content
        now_path = os.path.abspath('.')
        save_path  = now_path + "/book/"
        filename = "{0}{1}".format(filename,".jpg")
        try:
            with open(filename, 'wb') as fh:
                fh.write(content)
        except FileNotFoundError as err:
            print(err)

def main():
    book = Books()
    result = book.get_filename_and_url()
    fina = book.get_img(result)
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in '%s': %s" % (cwd, files))
    print()


if __name__ == "__main__":
    main()
