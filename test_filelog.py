import os
import functools
import time
import pandas as pd
import tkinter
import tkinter.filedialog
from tkinter import ttk

class DealFolder:
    
    def __init__(self, root):
        root.title('accumulate info')
        mainframe = ttk.Frame(root, padding='3 3 12 12')
        mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.path = tkinter.StringVar()
        ttk.Label(mainframe, text="目标路径").grid(column=0, row=0)
        ttk.Entry(mainframe, textvariable= self.path).grid(column=1, row=0)
        ttk.Button(mainframe, text="路径选择",command=self.select_folder).grid(column=2, row=0)
        ttk.Button(mainframe, text='开始', command=self.filewriter, width=4).grid(column=1, row=1, sticky=(tkinter.W, tkinter.E))
        ttk.Button(mainframe, text='Quit', command=root.destroy, width=4).grid(column=2,row=1, sticky=(tkinter.W, tkinter.E))
        self.loglb = tkinter.StringVar()
        ttk.Label(mainframe,textvariable=self.loglb).grid(column=0,columnspan=3,row=2)
    
    def select_folder(self):
        foldername = tkinter.filedialog.askdirectory()
        if foldername != '':
            self.path.set(foldername)
        else:
            self.loglb.set("您未选择文件夹")

    def log_execution_time(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            start = time.perf_counter()
            res = func(self, *args, **kwargs)
            end = time.perf_counter()
            self.loglb.set("处理耗时{}秒\n处理完成".format(end-start))
            return res
        return wrapper

    @log_execution_time
    def filewriter(self):
        deal_path = self.path.get()
        if deal_path != '':
            a = os.walk(deal_path)
            res = []
            self.loglb.set('处理中')
            root.update()
            for fo_path, _ , f_lists in a:
                for file in f_lists:
                    res.append([fo_path, file])        
            df = pd.DataFrame(res)
            df.to_csv(os.path.join(deal_path,'log2.csv'),encoding='utf-8-sig',index=False,header=['folder','file'])
        else:
            self.loglb.set('您未选择文件夹')


root = tkinter.Tk()
DealFolder(root)
root.mainloop()