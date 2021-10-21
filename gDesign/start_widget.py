# -*- coding: UTF-8 -*-
"""
@author:Janko
@file:start_widget.py
@time:2021/10/20
"""
import os.path
import sys,re

from PyQt5 import QtCore, QtGui, QtWidgets
from Client import Client


# 自定义tag展示下滑小页面
class MyWiget(QtWidgets.QListView):
    key_enter_signal = QtCore.pyqtSignal()
    def __init__(self,parent=None, list_str=[]):
        super(MyWiget, self).__init__(parent)
        self.resize(261,120)
        self.setMaximumWidth(261)
        self.setMinimumWidth(261)
        # 这只listview内容不可编辑
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.qlist = list_str

        self.slm = QtCore.QStringListModel()
        self.slm.setStringList(self.qlist)
        self.setModel(self.slm)

    def update_list_str(self,new_list):
        self.slm.setStringList(new_list)
        self.setModel(self.slm)
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        super(MyWiget, self).keyPressEvent(e)
        # 需要return和key_enter同时写，前者代表字母键的enter 、后者代表数字键的enter
        if e.key()==QtCore.Qt.Key_Return or e.key()==QtCore.Qt.Key_Enter:
            self.key_enter_signal.emit()
# 自定义tag对应的lineedit
class MyLineEdit(QtWidgets.QLineEdit):
    clicked_signal  = QtCore.pyqtSignal()
    keypress_signal = QtCore.pyqtSignal(int)
    def __init__(self,parent = None):
        super(MyLineEdit, self).__init__(parent)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.clicked_signal.emit()
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        super(MyLineEdit, self).keyPressEvent(a0)
        if a0.key() == QtCore.Qt.Key_Down:
            self.keypress_signal.emit(0)
        if a0.key() == QtCore.Qt.Key_Up:
            self.keypress_signal.emit(1)



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(730, 343)
        self.lin_1 = QtWidgets.QLineEdit(Form)
        self.lin_1.setGeometry(QtCore.QRect(60, 60, 520, 30))
        self.lin_1.setObjectName("lin_1")
        self.btn_1 = QtWidgets.QPushButton(Form)
        self.btn_1.setGeometry(QtCore.QRect(600, 60, 81, 30))
        self.btn_1.setObjectName("btn_1")
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setGeometry(QtCore.QRect(60, 120, 261, 31))
        self.label_1.setObjectName("label_1")
        self.lin_2 = MyLineEdit(Form)
        self.lin_2.setGeometry(QtCore.QRect(60, 180, 520, 30))
        self.lin_2.setObjectName("lin_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(60, 240, 261, 31))
        self.label_2.setObjectName("label_2")
        self.btn_2 = QtWidgets.QPushButton(Form)
        self.btn_2.setGeometry(QtCore.QRect(600, 180, 81, 30))
        self.btn_2.setObjectName("btn_2")

        self.rbt_1 = QtWidgets.QRadioButton('Select Whole Genome',Form)
        self.rbt_1.setGeometry(QtCore.QRect(60,140,260,31))
        self.rbt_1.setAutoExclusive(False)

        self.rbt_2 = QtWidgets.QRadioButton('Select Specific Genes',Form)
        self.rbt_2.setGeometry(QtCore.QRect(260, 140, 260, 31))
        self.rbt_2.setAutoExclusive(False)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "gDesign"))
        self.lin_1.setPlaceholderText(_translate("Form", "Escherichia coli strain DH5alpha"))
        self.lin_2.setPlaceholderText(_translate("Form", "carbonic anhydrase; DapA; GHR40_09205"))
        self.btn_1.setText(_translate("Form", "OK"))
        self.label_1.setText(_translate("Form", "Loading..."))
        self.label_2.setText(_translate("Form", "Loading..."))
        self.btn_2.setText(_translate("Form", "Start"))

class StartWidget(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super(StartWidget, self).__init__()

        self.label_main = QtWidgets.QLabel(self)
        self.label_main.resize(730,343)
        ico_patn = Resources.get_url("sw_icon.ico")
        self.setWindowIcon(QtGui.QIcon(ico_patn))

        back_png = Resources.get_url("back-3.png")
        self.label_main.setStyleSheet('image:url('+back_png+');')

        self.label_scn = QtWidgets.QLabel(self)
        self.label_scn.resize(70, 70)
        logo_png = Resources.get_url("logo-4.png")
        self.label_scn.setStyleSheet('image:url('+logo_png+');')

        self.lab_1_1 = QtWidgets.QLabel(self)
        self.lab_1_1.setGeometry(QtCore.QRect(60, 40, 350, 20))
        self.lab_1_1.setText("<span style='font-size:10px;'>Please enter and select the strain name:</span>")
        # self.lab_1_1.setStyleSheet('background-color:red;')

        self.lab_2_2 = QtWidgets.QLabel(self)
        self.lab_2_2.setGeometry(QtCore.QRect(60, 160, 280, 20))
        self.lab_2_2.setText("<span style='font-size:10px;'>Please enter and select genes:</span>")
        # self.lab_2_2.setStyleSheet('background-color:red;')

        self.btn_3 = QtWidgets.QPushButton('Clear',self)
        self.btn_3.resize(80,30)
        self.btn_3.move(325,280)

        self.setupUi(self)
        self.client =Client()
        self.dict_pro = {}
        self.new_list = []

        self.geneobj_w = MyWiget(self)
        self.geneobj_w.hide()
        # self.geneobj_w.show()
        self.geneobj_w.move(60,210)


        # lab-time-1
        self.time1 = 1
        self.time_load1 = QtCore.QTimer(self)
        self.time_load1.timeout.connect(self.time_load1_out)
        # lab-time-2
        self.time_load2 = QtCore.QTimer(self)
        self.time_load2.timeout.connect(self.time_load2_out)

        self.lin_2.setEnabled(False)
        self.btn_2.setEnabled(False)
        self.btn_1.setEnabled(False)
        self.label_2.setText('')
        self.label_1.setText('')
        self.rbt_1.setEnabled(False)
        self.rbt_2.setEnabled(False)

        # 初始化设置model
        self.slm_line_1 = QtCore.QStringListModel()
        self.slm_line_1.setStringList([])
        self.lin_1_completer = QtWidgets.QCompleter(self.slm_line_1)
        self.lin_1.setCompleter(self.lin_1_completer)
        self.lin_1_completer.setMaxVisibleItems(10)
        self.lin_1_completer.setCompletionMode(1)


        # 槽函数
        self.lin_1.textEdited.connect(self.lin_1_edit)
        self.btn_1.clicked.connect(self.btn_1_clicked)

        self.lin_2.textEdited.connect(self.lin_2_edit)
        self.lin_2.clicked_signal.connect(self.lin_2_clicked)


        self.geneobj_w.key_enter_signal.connect(self.lin_2_enter)
        self.geneobj_w.clicked.connect(self.clicked_item)

        self.btn_2.clicked.connect(self.btn_2_clicked)

        self.btn_3.clicked.connect(self.btn_3_clicked)

        self.rbt_1.clicked.connect(self.rbt_1_clicked)
        self.rbt_2.clicked.connect(self.rbt_2_clicked)

    def rbt_1_clicked(self):
        self.rbt_2.setEnabled(False)
        self.rbt_1.setEnabled(False)

        t = self.client.gene_something(self.client.strain.genelist)
        if t ==0:
            QtWidgets.QMessageBox.information(self, 'error', 'Unknown base detected, please check whether any other character except for ATCG exists.', QtWidgets.QMessageBox.Yes)
        elif t ==1:
            QtWidgets.QMessageBox.information(self, 'error',
                                              'No start codon ATG or TTG detected, please check the input.',
                                              QtWidgets.QMessageBox.Yes)

        elif t ==2:
            QtWidgets.QMessageBox.information(self, 'error',
                                              'No stop codon detected, please check the input.',
                                              QtWidgets.QMessageBox.Yes)

        elif t == 3:
            QtWidgets.QMessageBox.information(self, 'error',
                                              'A pre-exist stop codon detected, please check the input.',
                                              QtWidgets.QMessageBox.Yes)
        else:
            name, ok = QtWidgets.QInputDialog.getText(self, '保存的文件名', '请输入名称', text="Null")
            if ok:
                file_path = QtWidgets.QFileDialog.getExistingDirectory(self, '选择结果文本文件保存路径', '/')
                self.label_2.setText('Loading...')

                #
                self.time_load2.start(80)
                #
                # print(file_path)
                abs_file_path = os.path.join(file_path, name + '.txt')
                # 判断文件是否已经存在
                if os.path.exists(abs_file_path):
                    recoder = QtWidgets.QMessageBox.information(self, '存在同名文件', '是否替换文件？',
                                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    if recoder == 65536:
                        return
                # 线程2--保存文件
                self.t_2 = WriteThread(abs_file_path, t)
                self.t_2.w_over_signal.connect(self.write_over)
                self.t_2.start()

    def rbt_2_clicked(self):
        self.rbt_2.setEnabled(False)
        self.rbt_1.setEnabled(False)
        self.lin_2.setEnabled(True)



    def btn_3_clicked(self):
        self.lin_2.setText('')
        self.lin_1.setText('')
        self.lin_2.setEnabled(False)
        self.btn_2.setEnabled(False)
        self.lin_1.setEnabled(True)
        self.btn_1.setEnabled(True)
        self.btn_1.setEnabled(False)
        self.rbt_1.setEnabled(True)
        self.rbt_2.setEnabled(True)
        self.rbt_1.setChecked(False)
        self.rbt_2.setChecked(False)
        self.rbt_1.setEnabled(False)
        self.rbt_2.setEnabled(False)

        self.label_1.setText('')
        self.label_2.setText('')

    def update_comleter_lin1(self,new_list):
        self.slm_line_1.setStringList(new_list)
        self.lin_1_completer.setModel(self.slm_line_1)

    def lin_1_edit(self):
        # 每次修改都调用search

        t = self.client.search(self.lin_1.text())
        # print(len(t))
        # print(t[0].Species,t[0].Accession,t[0].FTP)
        self.new_list = []
        for i in t:
            self.new_list.append(i.Species+i.Accession)
        # print(self.new_list)
        if self.new_list:
            self.update_comleter_lin1(self.new_list)
            self.btn_1.setEnabled(True)
        else:
            self.update_comleter_lin1([])
            self.btn_1.setEnabled(False)

    def btn_1_clicked(self):
        # 检查lin1是否有数据
        text =self.lin_1.text()
        row = self.lin_1_completer.currentIndex().row()

        if text !='':
            # 线程1--用于下载
            # print('开始下载：',self.client.result_dict[text])
            # self.client.dwonload_genome(self.client.result_dict[text])
            # print('ok')
            self.t_1 = DownloadThread(self.client,self.client.resultList[row])
            self.t_1.over_signal.connect(self.download_over)
            self.t_1.start()
            #
            self.time1 = 1
            self.time_load1.start(80)
            #
            # self.label_1.setText('Loading...')
    def time_load1_out(self):
        if self.time1 == 100:
            self.time1 = 0
        self.time1 = self.time1%3
        if self.time1 == 1:
            self.label_1.setText('Loading.')
        elif self.time1 == 2:
            self.label_1.setText('Loading..')
        elif self.time1 == 0:
            self.label_1.setText('Loading...')
        self.time1+=1

    def download_over(self):
        self.label_1.setText('')
        self.time_load1.stop()

        self.t_1.deleteLater()
        self.lin_1.setEnabled(False)
        self.btn_1.setEnabled(False)
        # self.btn_2.setEnabled(True)
        # self.lin_2.setEnabled(True)
        self.rbt_1.setEnabled(True)
        self.rbt_2.setEnabled(True)

    def lin_2_clicked(self):
        self.geneobj_w.hide()
        self.lin_2_edit()

    def lin_2_enter(self):
        str_index = self.geneobj_w.slm.itemData(self.geneobj_w.currentIndex())[0]
        # print(str_index)
        self.put_in_str(str_index)

    # 在line2中放入一个str
    def put_in_str(self,str_index):
        if self.lin_2.text():
            text_list = re.split(r"[;；]",self.lin_2.text())
            text_list[-1] = str_index
            index_str = ";".join(text_list)
            self.lin_2.setText(index_str)
        else:
            self.lin_2.setText(str_index)
        self.geneobj_w.hide()
        self.lin_2.setFocus()

    def clicked_item(self,index):
        # print(index)
        text_index = self.geneobj_w.slm.itemData(index)[0]
        self.put_in_str(text_index)

    def lin_2_edit(self):
        # 获取lin2 中的内容
        text_list = re.split(r"[;；]",self.lin_2.text())
        text = text_list[-1]
        self.new_list_pro = []

        if text:
            search_list = self.client.strain.search(text)
            if search_list:
                self.btn_2.setEnabled(True)
                for search_item in search_list:
                    # 如果gene == no name，那么不显示
                    if search_item.gene == 'No name':
                        self.new_list_pro.append(search_item.Locus_tag)
                        self.dict_pro.update({search_item.Locus_tag: search_item})
                    else:
                        self.new_list_pro.append(search_item.gene+search_item.Locus_tag)
                        self.dict_pro.update({search_item.gene+search_item.Locus_tag:search_item})
                # reasearch界面显示
                self.geneobj_w.update_list_str(self.new_list_pro)
                self.geneobj_w.show()
            else:
                if text not in self.dict_pro.keys():
                    self.btn_2.setEnabled(False)
                self.geneobj_w.hide()
        else:
            self.geneobj_w.hide()


    def btn_2_clicked(self):
        text_list = re.split(r"[;；]",self.lin_2.text())
        objs = []
        for text in text_list:
            objs.append(self.dict_pro[text])
        # print(objs)
        str_list = self.client.gene_something(objs)

        name,ok = QtWidgets.QInputDialog.getText(self,'保存的文件名','请输入名称',text = "Null")
        if ok:
            file_path = QtWidgets.QFileDialog.getExistingDirectory(self,'选择结果文本文件保存路径','/')
            self.label_2.setText('Loading...')

            #
            self.time_load2.start(80)
            #
            # print(file_path)
            abs_file_path = os.path.join(file_path,name+'.txt')
            # 判断文件是否已经存在
            if os.path.exists(abs_file_path):
                recoder = QtWidgets.QMessageBox.information(self, '存在同名文件', '是否替换文件？', QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
                if recoder == 65536:
                    return
            # 线程2--保存文件
            self.t_2 = WriteThread(abs_file_path,str_list)
            self.t_2.w_over_signal.connect(self.write_over)
            self.t_2.start()

    def time_load2_out(self):
        if self.time1 == 100:
            self.time1 = 0
        self.time1 = self.time1%3
        if self.time1 == 1:
            self.label_2.setText('Loading.')
        elif self.time1 == 2:
            self.label_2.setText('Loading..')
        elif self.time1 == 0:
            self.label_2.setText('Loading...')
        self.time1+=1

    def write_over(self):
        self.label_2.setText('')
        self.time_load2.stop()
        QtWidgets.QMessageBox.information(self, '信息提示对话框', '保存完成', QtWidgets.QMessageBox.Yes)
        self.t_2.deleteLater()




class DownloadThread(QtCore.QThread):
    over_signal = QtCore.pyqtSignal()
    def __init__(self,client,Ecoli):
        super(DownloadThread, self).__init__()
        self.client = client
        self.Ecoli = Ecoli
        # print(self.Ecoli)
    def run(self) -> None:
        self.client.dwonload_genome(self.Ecoli)
        self.over_signal.emit()
        # strain = Genome(self.Ecoli)
        # print(strain,strain.genelist)

class WriteThread(QtCore.QThread):
    w_over_signal = QtCore.pyqtSignal()
    def __init__(self,abs_file_path,str_list):
        super(WriteThread, self).__init__()
        self.abs_file_path = abs_file_path
        self.str_list = str_list
    def run(self) -> None:
        with open(self.abs_file_path, 'w')as f:
            for value in self.str_list:
                f.write(str(value)+'\n')
        self.w_over_signal.emit()

class Resources(object):
 @staticmethod
 def get_url(resource_name):
     if getattr(sys, 'frozen', False):  # 是否Bundle Resource
         base_path = sys._MEIPASS
         url_path = os.path.join(base_path,"resource\\{}".format(resource_name))
         value_t = url_path.replace('\\','/')
         # print(value_t)
         return value_t
     else:
         return "{}".format(resource_name)

class QssTool():
    @staticmethod
    def setQssToObj(file_path,obj):
        with open(file_path,'r') as f:
            content = f.read()
            obj.setStyleSheet(content)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    qss_path = Resources.get_url('Ubuntu.qss')
    QssTool.setQssToObj(qss_path,app)


    win = StartWidget()

    win.show()



    sys.exit(app.exec_())
