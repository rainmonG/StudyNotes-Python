#!/usr/bin/env python
# coding=utf-8

"""
@author: guyumeng
@license: RACE
@file: try1.py
@date: 2024/2/5 9:05
@desc: 
"""
from tkinter import *

# https://blog.csdn.net/qq_48979387/article/details/125706562
# print(tk.TkVersion) -- 8.6
# 组件根据坐标被排列在容器中，窗口的界面是该窗口中最大的容器
# 坐标系和pygame的一样（屏幕式），左上角为起点，x轴向右延伸，y轴向下延伸。在窗口中，容器的左上角是(0, 0)，不包括窗口的标题栏和菜单栏。
# 不支持颜色RGB元组形式，但支持颜色名称和十六进制。特殊的颜色名称：SystemButtonFace，浅灰色，组件默认背景色（只能在tk中使用，其他模块不支持）

root = Tk()
root.title("my window")
root.geometry("600x300+20+50")  # geometry还有一些用法，在讲Wm类的时候会介绍
root.resizable(True, False)
img = PhotoImage(file="logo.png")
root.iconphoto(False, img)
root.config(bg="white")
root.mainloop()

# 组件有Label, Message, Button, Entry, Text, Canvas, Frame, LabelFrame, Menu, Menubutton, Checkbutton, Radiobutton,
# Listbox, Scrollbar, Scale, Spinbox, OptionMenu, OptionMenu, PanedWindow, Toplevel
# 标签用于在窗口上显示文本和图片，消息用于显示多行文本类似Label，按钮点击事件将会传递给设置的回调函数，文本输入框单行，多行，
# 画布可以显示基本图形文字图片，框架作为一个小容器相当于给组件分组，文字框架外部多了文本提示，菜单在窗口显示或定义弹出式，菜单按钮点击后弹出一个菜单，
# 多选、单选按钮，列表框显示一个字符串的列表，滚动条控制滚动，尺度条可以添加数字滑块滑动调数值，数字选值框可以输入数字也可按调节按钮，选项菜单下拉菜单选项，
# 分栏器比Frame功能设定更多比如可调大小，上层窗口可以定义某个窗口的子窗口，
# 子模块ttk, messagebox, colorchooser, filedialog等，ttk中组件的字体、颜色等功能不能直接修改，要用ttk.style修改，而tkinter主模块中可以直接指定组件样式，
# 如果在from tkinter import * 后继续导入 from tkinter.ttk import *，就会覆盖tkinter.ttk与tkinter主模块中相同的组件，导致改样式只能使用Style的形式。
# ttk扩展组件：
# Combobox 组合选择框，可以输入也可以下拉列表选择
# Notebook 笔记本，添加多个Frame选项卡，用户可以在不同选项卡之间切换
# Progressbar 加载时进度条
# Separator 分割线
# Treeview 树状图或表格
# Sizegrip 窗口尺寸的调整按钮