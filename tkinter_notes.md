# Modern Tkinter for Busy Python Developers
zlibrary上下载的，棒
一开始还下错了书，有缺失，3.78MB的才是全的。过程中网站还下载不了了，发给邮箱（各种探索中的小发现~~）

```python
import tkinter
from tkinter import ttk

class FeetToMeters:

    def __init__(self, root) -> None:

        root.title("Feet to Meters")

        mainframe = ttk.Frame(root, padding='3 3 12 12')
        mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.feet = tkinter.StringVar()
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky=(tkinter.W, tkinter.E))

        self.meters = tkinter.StringVar()
        ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(tkinter.W, tkinter.E))

        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=tkinter.W)

        ttk.Label(mainframe, text='feet').grid(column=3, row=1, sticky=tkinter.W)
        ttk.Label(mainframe, text='is equivalent to').grid(column=1, row=2, sticky=tkinter.W)
        ttk.Label(mainframe, text='meters').grid(column=3, row=2, sticky=tkinter.W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Return>", self.calculate)

    def calculate(self,*args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass
    
root = tkinter.Tk()
FeetToMeters(root)
root.mainloop()
```
`tkinter`的组件排布完之后，不会自动显示，需要手动启动根窗口。

# 事件绑定
比如上面将在根窗口范围内按回车键与函数绑定，联系上下文，光标在输入框里，所以相当于填完数字按回车，就触发计算，等同于按`Calculate`按钮。
这里绑定的事件专门设了函数名，也可以是`lambda`匿名函数

# 窗口大小
显式指定时，可以加后缀，比如默认是像素，加c是厘米，加m是毫米，加i是英寸，加p是打印机点数（1/72inch）
几何图形管理器有最终决定权
两边间距
```python
f['padding'] = 5 # 5 pixels on all sides
f['padding'] = (5,10) # 5 on left and right, 10 on top and bottom
f['padding'] = (5,7,10,12) # left: 5, top: 7, right: 10, bottom: 12
```
# Label
动态显示变量：`textvariable`属性，赋一个`StringVar`类实例变量，`get`或`set`方法读取或赋值
显示图＋字：`compound`配置
改变字体、颜色等不像以前的Tk直接改，而是创建一个新的style，然后赋值给`style`属性。（lable组件还是可以直接改，但是不建议这样做，除非样式确定不复用。）
颜色可以赋值为名称或十六进制RGB值。
`wraplength`选项，在给定长度后自动换行，长度也像间距一样可带后缀
`justify`或`anchor`，`anchor`定位用于单行，但是如果是用了`grid`，就要变成在里面设置`sticky`
`Button`配置选项中有个`default`选项，如果设置为`active`，回车键会自动调用这个按钮，但不会自动创建事件绑定，还是要自己绑定事件。比如点击按钮调用一个函数，回车键默认，也不会触发这个函数的，还是要显式绑定函数到回车键上。但可以绑定按钮的`invoke()`方法，这样按钮绑定的事件变了会同步改，稍微便捷一点。
`disabled`标记，控制在某个阶段不允许用户点击（有用，避免重复执行之类的），接收的参数是数组
```python
b.state(['disabled']) # set the disabled flag
b.state(['!disabled']) # clear the disabled flag
b.instate(['disabled']) # true if disabled, else false
b.instate(['!disabled']) # true if not disabled, else false
b.instate(['!disabled'], cmd) # execute 'cmd' if not disabled
```

# Entry
`show`属性，比如输入密码的时候，配套的还有`validatecommand`
```python
from tkinter import *
from tkinter import ttk

root=Tk()

import re
errmsg = StringVar()
formatmsg = "Zip should be ##### or #####-####"

def check_zip(newval, op):
    errmsg.set('')
    valid = re.match('^[0-9]{5}(\-[0-9]{4})?$', newval) is not None
    btn.state(['!disabled'] if valid else ['disabled'])
    if op=='key':
        ok_so_far = re.match('^[0-9\-]*$', newval) is not None and len(newval) <= 10
        if not ok_so_far:
            errmsg.set(formatmsg)
        return ok_so_far
    elif op=='focusout':
        if not valid:
            errmsg.set(formatmsg)
    return valid
check_zip_wrapper = (root.register(check_zip), '%P', '%V')

zip = StringVar()
f = ttk.Frame(root)
f.grid(column=0, row=0)
ttk.Label(f, text='Name:').grid(column=0, row=0, padx=5, pady=5)
ttk.Entry(f).grid(column=1, row=0, padx=5, pady=5)
ttk.Label(f, text='Zip:').grid(column=0, row=1, padx=5, pady=5)
e = ttk.Entry(f, textvariable=zip, validate='all', validatecommand=check_zip_wrapper)
e.grid(column=1, row=1, padx=5, pady=5)
btn = ttk.Button(f, text="Process")
btn.grid(column=2, row=1, padx=5, pady=5)
btn.state(['disabled'])
msg = ttk.Label(f, font='TkSmallCaptionFont', foreground='red', textvariable=errmsg)
msg.grid(column=1, row=2, padx=5, pady=5, sticky='w')

root.mainloop()

```