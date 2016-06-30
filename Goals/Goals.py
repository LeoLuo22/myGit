# -*- coding:utf-8 -*-
__author__: Leo Luo

from datetime import datetime
import re

class Goals(object):
    def __init__(self):
        super().__init__

    def set_new_goal(self,goal):
        new_goal_year = str(datetime.now().year)
        new_goal_month = str(datetime.now().month)
        new_goal_day = str(datetime.now().day)
        new_goal_date = new_goal_year + "/" + new_goal_month + "/" + new_goal_day
        reward = "初次奖励: 10"
        content = new_goal_date + "  " + goal + "    " + reward
        self.__write_content(goal, content)
        self.get_content(goal)

    def get_content(self, goal):#TODO
        file_object = open(goal,encoding='utf-8')
        file_content = []
        content = {}
        try:
            for line in file_object:
                chars = '/'
                line = line.strip().split(chars)
                file_content.append(line)
            print(file_content)
            for lists in file_content:
                content.setdefault(lists[0],lists[1])
                print(content)
            return content
        finally:
            file_object.close()


    def add_content_exist_goal(self, goal):pass


    def success_to_goal(self, goal):
        today = None#TODO
        content = str(today) + goal + "完成"
        with open(goal, 'w') as fh:
            fh.write(content)

    def failed_to_goal(self, goal):
        today = None#TODO
        content = str(today) + goal + "失败"
        with open(goal, 'w', encoding='utf-8') as fh:
            fh.write(content)

    def show_result(self, goal):
        with open(goal, 'r') as fh:
            fh.read()

    def __write_content(self, goal_name, content):
        with open(goal_name, 'w') as fh:
            fh.write(content)


class InputError(Exception):pass

def initial(goal_instance):
    while True:
        print("*******************请选择要使用的功能**********************")
        option = input("1.设置新目标   2.显示现有目标并打卡  3.删除目标")
        try:
            option = int(option)
        except ValueError as err:
            print(err)
            continue
        try:
            if option not in range(1,4):
                print("输入有误!")
                raise InputError
        except (InputError) as err:
            print("error")
            continue
        if option == 1:
            new_goal = input("请输入你的新目标: ")
            goal_instance.set_new_goal(new_goal)
            print("新目标 {0} 设置成功!".format(new_goal))
            continue

        elif option == 2:
            goal_instance.show_result()
            opt = input("请输入要打卡的目标: ")
            cfm = input("你完成了吗? (y/n)")
            if cfm == "y" or cfm == "Y":
                goal_instance.success_to_goal(opt)
            elif crm == "n" or crm == "N":
                goal_instance.failed_to_goal(opt)

        elif option == 3:
            seq_num = input("请输入要删除的目标: ")
            confirm = input("确定要删除 {0} (y/n)?".format(seq_num))
            if confirm == "y":
                goal_instance.delete_goal(seq_num)
                continue
            else:
                continue

def main():
    goal = Goals()
    initial(goal)

if __name__ == "__main__":
    main()
