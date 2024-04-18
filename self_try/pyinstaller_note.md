# 问题
直接用pyinstaller打包exe的话，所有第三方库的包都会装进去，生成的exe太大
# 方案
目前查找的实用方案是虚拟环境打包
[Python 打包成 exe，太大了该怎么解决？](https://www.zhihu.com/question/281858271/answer/887007175)
### 注意点
1. 虚拟环境
其实也有别的虚拟环境吧，但是没有比较过，平时也不喜欢虚拟环境，所以就参考答主的推荐，装了这个
``` shell
pip install virtualenv
```
在要装虚拟环境的地方直接
```shell
virtualenv ***
```
就会创建一个文件夹，会有虚拟环境需要的一切
```shell
./***/scripts/activate
```
激活，`deactivate`就退出，加不加后缀`.bat`都没关系
删除的话就`rm`删除文件夹就好了

2. 虚拟环境装包
**一定要装pyinstaller**~~~不然又会去本地的Python第三方库里打包
还要注意代码里有没有因为自动补全，过程中不小心加进去的库，比如不小心从哪里揪进去个`test`、`matplotlib`什么的
如果用了pandas写excel文件，要把openpyxl也装上
pip freeze可以看到已安装的包和版本

1. 打包
```shell
pyinstaller --clean --onefile -F ***.py
```
我自己试，这样是可以省略掉spec再打包那一步的
**有界面的时候要加个`-w`**
```shell
pyinstaller -F -w --clean --onefile .\2022-10-05\test_filelog.py
```

4. 做界面
据说如果是`pyqt5`的话打包也贼大，小玩意儿就用`tkinter`代替了，所以速学一下~
pyqt都到6了~~

5. Python解释器
虚拟环境退出，vscode的终端或者jupyter可能还没有反应过来-_-||，所以`ctrl`+`shift`+`p`，`interpreter`搜一下就可以选解释器了，选回去~

替代：`nuitka`~~待研究