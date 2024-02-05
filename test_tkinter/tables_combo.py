#!/usr/bin/env python
# coding=utf-8

"""
@author: guyumeng
@license: RACE
@file: tables_combo.py
@date: 2024/2/5 15:19
@desc: 
"""
import os
import functools
import time
import pandas as pd
import tkinter as tk
import tkinter.filedialog as tf


class DealFolder:
    """
    合并同名表格或合并一个文件夹内所有表格
    """

    def __init__(self, root):
        root.title('表格处理')
        root.geometry("600x300+20+50")
        mainframe = tk.Frame(root, width=500, height=300, padx=3, pady=3)
        mainframe.grid(column=0, row=0, sticky='nwse')
        # mainframe.grid_propagate(0)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.path = tk.StringVar()
        tk.Label(mainframe, text="目标路径").grid(column=0, row=0)
        tk.Label(mainframe, textvariable=self.path, width=60, relief='ridge').grid(column=1, row=0)
        self.b_choose = tk.Button(mainframe, text="路径选择", command=self.select_folder)
        self.b_choose.grid(column=2, row=0)
        self.mod = tk.IntVar(value=1)
        self.mod_choice1 = tk.Radiobutton(mainframe, text="合并文件夹内所有表格", variable=self.mod, value=1)
        self.mod_choice1.grid(column=1, row=1)
        self.mod_choice2 = tk.Radiobutton(mainframe, text="分开合并文件夹内所有同名表格", variable=self.mod, value=2)
        self.mod_choice2.grid(column=2, row=1)
        self.b_start = tk.Button(mainframe, text='开始处理', command=self.filewriter, width=4)
        self.b_start.grid(column=1, row=2, sticky='ew')
        tk.Button(mainframe, text='Quit', command=root.destroy, width=4).grid(column=2, row=2, sticky='ew')
        self.loglb = tk.StringVar()
        self.loglb.set("请选择要收集对端关系的数据文件夹路径，选定后点击开始处理")
        tk.Label(mainframe, textvariable=self.loglb).grid(column=0, columnspan=3, row=2)

    def select_folder(self):
        folder_name = tf.askdirectory()
        if folder_name:
            self.path.set(folder_name)
            self.loglb.set("您已选择{}".format(folder_name))
        else:
            self.loglb.set("您未选择文件夹")

    def log_execution_time(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            start = time.perf_counter()
            res = func(self, *args, **kwargs)
            end = time.perf_counter()
            self.loglb.set(self.loglb.get() + "\n处理耗时{}秒".format(end - start))
            self.b_start.state(['!disabled'])
            self.b_choose.state(['!disabled'])
            return res

        return wrapper

    @log_execution_time
    def filewriter(self):
        deal_path = self.path.get()
        if deal_path:
            self.b_start.state(['disabled'])
            self.b_choose.state(['disabled'])
            a = os.walk(deal_path)
            res = []
            log = []
            self.loglb.set('处理中')
            root.update()
            for fo_path, _, f_lists in a:
                for file in f_lists:
                    if file.endswith('.xlsx') or file.endswith('.xls'):
                        filepath = os.path.realpath(os.path.join(fo_path, file))
                        try:
                            with open(filepath, 'r', encoding='gb18030', errors='ignore') as f:
                                content = f.readlines()
                            start = 0
                            end = 0
                            for i in range(len(content)):
                                if content[i].startswith('Local Interface'):
                                    start = i + 2
                                if start:
                                    if content[i].startswith('<'):
                                        end = i
                                        break
                            if start * end:
                                table = content[start:end]
                                a = pd.DataFrame(table, columns=['source'])
                                a.loc[:, 'sourcePath'] = fo_path
                                a.loc[:, 'Local Device'] = file.strip('.txt').strip('.log')
                                res.append(a)
                                log.append([filepath, 'OK'])
                            else:
                                log.append([filepath, '未找到相应标识'])
                        except:
                            log.append([filepath, '未知错误，请人工确认'])
                            continue
            if res:
                df = pd.concat(res)
                df['intfind'] = df['source'].apply(startint)
                df = df[df['intfind'] >= 40]
                if not df.empty:
                    df1 = df['source'].apply(lambda s: s.strip('\n')).str.split(expand=True)
                    cols = ['Local Interface', 'Exptime(s)', 'Neighbor Interface', 'Neighbor Device']
                    df1.columns = cols
                    df1 = pd.concat([df[['sourcePath', 'Local Device']], df1], axis=1)
                    savename = '对端关系result_{}.csv'.format(time.strftime('%Y%m%d%H%M%S', time.localtime()))
                    df1.to_csv(os.path.join(deal_path, savename), encoding='gb18030', index=False)
                    self.loglb.set(self.loglb.get() + "\n处理完成，结果保存在{}".format(
                        os.path.realpath(os.path.join(deal_path, savename))))
                else:
                    self.loglb.set(self.loglb.get() + "\n处理完成，筛选后无40GE以上的设备对端信息")
            else:
                self.loglb.set(self.loglb.get() + "\n该文件夹中未找到符合设定的对端关系")
            if log:
                df = pd.DataFrame(log)
                logname = '对端程序日志_{}.csv'.format(time.strftime('%Y%m%d%H%M%S', time.localtime()))
                df.to_csv(os.path.join(deal_path, logname), encoding='gb18030', index=False,
                          header=['文件路径', '执行日志'])
                self.loglb.set(
                    self.loglb.get() + "\n执行日志记录在{}".format(os.path.realpath(os.path.join(deal_path, logname))))

        else:
            self.loglb.set('您未选择文件夹')


root = tk.Tk()
DealFolder(root)
root.mainloop()