#-*- coding:utf-8 -*-
__author__ = "Leo Luo"

import sqlite3
from datetime import datetime
import os
import collections

class InputError(Exception):pass

class Goal(object):
    def __init__(self, ID=None, Name=None, Date=None, Success=None, Failure=None, Total=None, Rate=None, Reward=None):
        super().__init__
        self.ID = ID
        self.Name = Name
        self.Date = Date
        self.Success = Success
        self.Failure = Failure
        self.Total = Total
        self.Rate = Rate
        self.Reward = Reward

    def __last_data(self, db_name):
        today_date = get_date()
    def write_to_db(self, date):pass

    def add(self, name):
        _name = name
        if not name.endswith(".db"):
            name += ".db"
        conn = sqlite3.connect(name)
        cur = conn.cursor()
        try:
            cur.execute("create table goal(ID interger primary key, Name varchar(10), Date varchar(10), Success interger, Failure interger, Total interger, Rate float, Reward float)")
        except sqlite3.OperationalError as err:
            print("goal表已存在")
        t = (1, _name, get_date(), 0, 0, 0, 0.1, 0)
        cur.execute("insert into goal values (?, ?, ?, ?, ?, ?, ?, ?)",t)
        conn.commit()
        conn.close()

    def show_all(self, db_name):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("select * from goal order by id desc")
        result_lis = cur.fetchall()
        print(result_lis[0])
        conn.commit()
        conn.close()


def get_input(msg, _type):
    if _type == "option":
        while  True:
            option = input(msg)
            option = int(option)
            try:
                if option not in range(1,10):
                    raise InputError()
            except InputError as err:
                print("Wrong input.")
                continue
            return option
    elif _type == "select_option":
        while True:
            select_option = input(msg)

def get_date():
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    day = str(datetime.now().day)
    date = year + "/" + month + "/" + day
    return date

def exist_db():
    db = collections.OrderedDict()
    _all = os.listdir('.')
    all_db = []
    for i in _all:
        if i.endswith('.db'):
            all_db.append(i)
    for lino, line in enumerate(all_db, start=1):
        db[lino] = line
    return db



def main():
    print("现有的数据库文件有: ")
    db = exist_db()
    for key, value in db.items():
        print("{0}   {1}".format(key,value))
    while True:
        option = get_input("请选择功能: 1.新建 2.删除 3.修改 4.查询", "option")
        goal = Goal()
        if option == 1:
            name = input("请输入名称: ")
            goal.add(name)
        elif option == 2:
            pass
        elif option == 3:
            pass
        elif option == 4:
            select_option = input("请输入要查询的序号: ")
            db_name = db[int(select_option)]
            print(db_name)
            goal.show_all(db_name)
if __name__ == "__main__":
    main()



