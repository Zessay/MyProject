# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 16:13:56 2018

@author: zhushuai
"""

import pandas as pd
import numpy as np
import copy
import random
import tkinter as tk
from tkinter import messagebox

# 事件处理函数的适配器
def handlerAdaptor(fun, **kwds):
    return lambda event, fun = fun, kwds=kwds:fun(event, **kwds)

# 关闭窗口处理函数的适配器
def handlerExit(fun, **kwds):
    return lambda fun = fun, kwds=kwds:fun(**kwds)

# 查找学生的ID
def search_id(E1, L2, stu_info):
    stu_id = E1.get()
    stu_id = str(stu_id).upper()
    id_num = list(np.where(stu_info == stu_id))
    if id_num[1] in range(4):
        name_num = copy.deepcopy(id_num)
        name_num[1] = 2
        name_num = tuple(name_num)
        id_num[1] = 3
        id_num = tuple(id_num)
        return id_num, name_num
    else:
        return [], []

# 保存文件
def save_file(stu, excel):
    print(stu)
    stu_info_new = pd.ExcelWriter(excel)
    stu.to_excel(stu_info_new)
    stu_info_new.save()

# 导入文件并补全其中的缺失值 
def load_file(excel):
    stu = pd.read_excel(excel)
    stu['考试题目'] = None  
    stu_info = stu.iloc[: , :].values
    stu_num = stu_info.shape[0]
    for i in range(1, stu_num):
        if str(stu_info[i][0]) == 'nan':
            stu_info[i][0] = stu_info[i-1][0]
    return stu, stu_info, stu_num

# 定义基本的组件
def base(root):
    tk.Label(root, text = " ").pack()
    L1 = tk.Label(root, text = '请输入你的学号: ',  font=('Arial 12 bold'))
    L1.pack()
    tk.Label(root, text = " ").pack()
    E1 = tk.Entry(root, bd=5)
    E1.pack()
    tk.Label(root, text = " ").pack()
    L2 = tk.Label(root, text = " ", font=('Arial 12 bold'))
    L2.pack()
    return L2, E1

# 输入的学号有错
def wrong_id(L2):
    L2.config(text="输入的学号有误，请重新输入！",fg="indigo")

# 显示并保存选课的信息
def changeTextA(event, L2, E1, stu_info):
    id_num, name_num = search_id(E1, L2, stu_info)
#    print(id_num)
    if id_num == []:
        wrong_id(L2)
    else:
        test_id = 'A' + str(random.randint(1,10))
        stu_info[id_num] = test_id
#        print(stu_info)
        L2.config(text= (stu_info[name_num] + " 的考试题目是："+ test_id)[0],fg="red")

def changeTextB(event, L2, E1, stu_info):
    id_num, name_num = search_id(E1, L2, stu_info)
    if id_num == []:
        wrong_id(L2)
    else:
        test_id = 'B' + str(random.randint(1,10))
        stu_info[id_num] = test_id
        L2.config(text= (stu_info[name_num] + " 的考试题目是："+ test_id)[0],fg="blue")

def changeTextC(event, L2, E1, stu_info):
    id_num, name_num = search_id(E1, L2, stu_info)
    if id_num == []:
        wrong_id(L2)
    else:
        test_id = 'C' + str(random.randint(1,10))
        stu_info[id_num] = test_id
        L2.config(text= (stu_info[name_num] + " 的考试题目是："+ test_id)[0],fg="orange")

def changeTextD(event, L2, E1, stu_info):
    id_num, name_num = search_id(E1, L2, stu_info)
    if id_num == []:
        wrong_id(L2)
    else:
        test_id = 'D' + str(random.randint(1,2))
        stu_info[id_num] = test_id
        L2.config(text= (stu_info[name_num] + " 的考试题目是："+ test_id)[0],fg="green")

# 定义关于按钮的函数
def set_button(root, L2, E1, stu_info):
    buttonA = tk.Button(root, text = "Choice A",fg="red")
    buttonB = tk.Button(root, text = "Choice B",fg="blue")
    buttonC = tk.Button(root, text = "Choice C",fg="orange")
    buttonD = tk.Button(root, text = "Choice D",fg="green")
    
    buttonA.bind("<Button-1>", handlerAdaptor(changeTextA, L2=L2, E1=E1, stu_info=stu_info))
    buttonB.bind("<Button-1>", handlerAdaptor(changeTextB, L2=L2, E1=E1, stu_info=stu_info))
    buttonC.bind("<Button-1>", handlerAdaptor(changeTextC, L2=L2, E1=E1, stu_info=stu_info))
    buttonD.bind("<Button-1>", handlerAdaptor(changeTextD, L2=L2, E1=E1, stu_info=stu_info))
    
    buttonA.pack(side=tk.LEFT,anchor=tk.CENTER, expand=tk.YES)
    buttonB.pack(side=tk.LEFT,anchor=tk.CENTER, expand=tk.YES)
    buttonC.pack(side=tk.LEFT,anchor=tk.CENTER, expand=tk.YES)
    buttonD.pack(side=tk.LEFT,anchor=tk.CENTER, expand=tk.YES)

# 关闭窗口时执行询问
def on_closing(root, stu, excel):
    if messagebox.askokcancel("保存并退出", "保存文件并退出窗口"):
        save_file(stu, excel)        
        root.destroy()

# 主函数 
def main():
    excel = 'stu_info_new.xlsx'
    stu, stu_info, stu_num = load_file(excel)       
    #print(stu_info)
    root = tk.Tk()
    root.title("考题选择工具")
    root.geometry('600x400')
    L2, E1 = base(root)
    set_button(root, L2, E1, stu_info)
    root.protocol("WM_DELETE_WINDOW", handlerExit(on_closing, root=root, stu = stu, excel = excel))
    root.mainloop()

if __name__ == '__main__':
    main()