#-*- coding:utf-8 -*-
__author__ = "Leo Luo"

import sqlite3
from datetime import datetime

class InputError(Exception):pass

class Goal(object):
    def __init__(self):
        super().__init__

    def write_to_db(self, date):pass

    def add(self, name):
        if not name.endswith(".db"):
            name += ".db"
        coon = sqlite3.connect(name)

def get_input(msg, _type):
    if _type == "option":
        while  True:
            option = input(msg)
            option = int(option)
            try:
                if option not in range(1,10):
                    raise InputError()
            except IndexError as err:
                print("Wrong input.")
                continue
            return option
def main():
    while True:
        option = get_input("请选择功能: 1.新建 2.删除 3.修改 4.查询", "option")
        goal = Goal()
        if option == 1:
            name = input("请输入名称: ")
            goal.add(name)

if __name__ == "__main__":
    main()



