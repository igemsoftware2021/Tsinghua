from UI import *
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2 import QtCore
from PySide2 import QtGui
import os

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

app = QApplication([])
stats = Stats()
stats.window.show()

app.exec_()








#responce=requests.get(url)
#print(responce.text)
#soup=BeautifulSoup(responce.text,'html.parser')
#print(soup.pre)
#text=str(soup.pre)
#context=text[5:-6]
#print(context)

#myCodonBias=codonBias(context)
#myData.setCodonBias(myCodonBias)

#myData.CalculationP2N()
#print(myData.aaSequence)
# myREDict=RESiteDict()
# print(myREDict.getRestrictionSiteList(['BbsI','BsaI','EcoRI']))


'''
需求分析：
    接口：
        输入：
            1. DNA序列 or 氨基酸序列
            2. 物种种类【越精细越好！】
            3. 是否需要优化linker的重复序列
            4. 是否需要避免酶切位点
            5. 是否需要引入终止密码子
        输出：
            DNA序列
    
    输入模式：
        表格，然后直接submit，生成
    
    算法过程：
        输入物种种类 -> 爬虫爬取url -> 逻辑运算 -> 输出DNA序列
'''

  ##写好connect的跳转函数


