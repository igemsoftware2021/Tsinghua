import requests
from bs4 import BeautifulSoup
import pandas as pd
from RESiteDict import *
import urllib
from DataPackage import *
from codonBias import *
from RESiteDict import *
from Downloader import *
import sys, os
import PySide2
import datetime

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


def isDNA(seq):
    for q in seq:
        if q == 'a' or q == 'A' or q == 't' or q == 'T' or q == 'c' or q == 'C' or q == 'g' or q == 'G':
            continue
        else:
            return False
    return True

def isAA(seq):
    for q in seq:
        if q == 'b' or q == 'B' or q == 'j' or q == 'J' or q == 'O' or q == 'o' or q == 'U' or q == 'u' or q == 'X' or q == 'x' or q == 'z' or q == 'Z':
            return False
        else:
            continue
    return True

class Stats:

    def __init__(self):
        self.window = QMainWindow()
        desktop = QApplication.desktop()
        self.screenWidth = desktop.width()
        self.screenHeight = desktop.height()
        self.window.resize(int(self.screenWidth * 0.5), int(self.screenHeight * 0.6))
        qRect = self.window.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.window.move(qRect.topLeft())
        #self.window.move(300, 400)
        self.window.setWindowTitle('P2N')


        palette = QPalette()
        brush1 = QBrush(QColor(170, 170, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        brush2 = QBrush(QColor(240, 240, 240, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush2)

        palette1 = QPalette()
        brush3 = QBrush(QColor(170, 170, 255, 100))
        brush3.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush3)
        brush4 = QBrush(QColor(240, 240, 240, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush4)

        font = QFont()
        font.setBold(True)
        font.setWeight(75)

        self.imageLabel = QLabel(self.window)
        self.PixMap = QPixmap("./igem.png")
        self.imageLabel.setPixmap(self.PixMap)
        self.imageLabel.move(int(100 * self.screenWidth / 3000), int(100 * self.screenHeight / 2000))
        self.imageLabel.resize(int(800 * self.screenWidth / 3000), int(800 * self.screenHeight / 2000))
        self.imageLabel.show()

        self.lineEdit = QLineEdit(self.window)
        self.lineEdit.setPlaceholderText("Please enter the species' name")
        self.lineEdit.move(int(150*self.screenWidth/3000), int(150*self.screenHeight/2000))
        self.lineEdit.resize(int(550*self.screenWidth/3000), int(60*self.screenHeight/2000))
        self.lineEdit.setFont(font)


        self.comboBox = QComboBox(self.window)
        self.comboBox.move(int(800*self.screenWidth/3000), int(150*self.screenHeight/2000))
        self.comboBox.resize(int(550*self.screenWidth/3000), int(60*self.screenHeight/2000))
        #self.comboBox.setObjectName(u"comboBox")

        self.pushButton = QPushButton("Search",self.window)
        self.pushButton.move(int(1280*self.screenWidth/3000), int(1000*self.screenHeight/2000))
        self.pushButton.resize(int(120*self.screenWidth/3000), int(60*self.screenHeight/2000))

        self.pushButton2 = QPushButton("Add Rows",self.window)
        self.pushButton2.move(int(1150*self.screenWidth/3000), int(1000*self.screenHeight/2000))
        self.pushButton2.resize(int(120*self.screenWidth/3000), int(60*self.screenHeight/2000))

        self.label1 = QLineEdit(self.window)
        self.label1.move(int(150*self.screenWidth/3000), int(380*self.screenHeight/2000))
        self.label1.resize(int(400*self.screenWidth/3000), int(70*self.screenHeight/2000))
        self.label1.setText("       Sequences (DNA/AA)")
        self.label1.setReadOnly(True)
        self.label1.setPalette(palette)
        self.label1.setFont(font)

        self.label2 = QLineEdit(self.window)
        self.label2.move(int(700*self.screenWidth/3000), int(380*self.screenHeight/2000))
        self.label2.resize(int(400*self.screenWidth/3000), int(70*self.screenHeight/2000))
        self.label2.setText("Avoid restriction enzyme sites")
        self.label2.setReadOnly(True)
        self.label2.setPalette(palette)
        self.label2.setFont(font)

        self.label3 = QLineEdit(self.window)
        self.label3.move(int(550*self.screenWidth/3000), int(380*self.screenHeight/2000))
        self.label3.resize(int(150*self.screenWidth/3000), int(70*self.screenHeight/2000))
        self.label3.setText("  Seq Type")
        self.label3.setReadOnly(True)
        self.label3.setPalette(palette)
        self.label3.setFont(font)




        self.d = RESiteDict()
        self.tableline1 = []
        self.tableline2 = []
        self.enzymeBox = []
        self.deleteEnz = []
        self.seqChoice = []
        self.tableRow = []
        for i in range(0,5):
            row = Rows(i)
            line1 = QLineEdit(self.window)
            line2 = QLineEdit(self.window)
            line3 = QLineEdit(self.window)
            line2.setText('')
            line1.setPalette(palette1)
            line2.setPalette(palette1)
            line3.setPalette(palette1)
            box = QComboBox(self.window)
            box.setPalette(palette1)
            seq = QButtonGroup(self.window)
            seq1 = QRadioButton(self.window)
            seq2 = QRadioButton(self.window)
            seq.addButton(seq1,1)
            seq.addButton(seq2,2)
            seq1.setText('DNA')
            seq2.setText('AA')
            delete = QPushButton(self.window)
            line1.move(int(150*self.screenWidth/3000), int((450+70*i)*self.screenHeight/2000))
            line1.resize(int(400*self.screenWidth/3000), int(70*self.screenHeight/2000))
            line2.move(int(700*self.screenWidth/3000), int((450+70*i)*self.screenHeight/2000))
            line2.resize(int(200*self.screenWidth/3000), int(70*self.screenHeight/2000))
            line3.move(int(550 * self.screenWidth / 3000), int((450 + 70 * i) * self.screenHeight / 2000))
            line3.resize(int(150 * self.screenWidth / 3000), int(70 * self.screenHeight / 2000))
            box.move(int(900*self.screenWidth/3000), int((450+70*i)*self.screenHeight/2000))
            box.resize(int(150*self.screenWidth/3000), int(70*self.screenHeight/2000))
            seq1.move(int(550*self.screenWidth/3000), int((450+70*i)*self.screenHeight/2000))
            seq1.resize(int(200*self.screenWidth/3000), int(70*self.screenHeight/2000))
            seq2.move(int(630*self.screenWidth/3000), int((450+70*i)*self.screenHeight/2000))
            seq2.resize(int(200*self.screenWidth/3000), int(70*self.screenHeight/2000))
            delete.move(int(1050*self.screenWidth/3000), int((450+70*i)*self.screenHeight/2000))
            delete.resize(int(50*self.screenWidth/3000), int(70*self.screenHeight/2000))
            delete.setText('Del')
            for key in self.d.myDict.keys():
                box.addItem(key)
            self.tableline1.append(line1)
            self.tableline2.append(line2)
            self.enzymeBox.append(box)
            self.seqChoice.append(seq)
            self.deleteEnz.append(delete)
            self.tableRow.append(row)

        self.lineEdit.textChanged.connect(self.handleTextChange)
        self.pushButton.clicked.connect(self.handleCalc)
        self.pushButton.clicked.connect(self.main)
        self.pushButton2.clicked.connect(self.insertRow)
        self.comboBox.activated.connect(self.convey1)
        self.x = 4
        self.enzymeBox[0].activated.connect(lambda:self.convey2(0))
        self.enzymeBox[1].activated.connect(lambda:self.convey2(1))
        self.enzymeBox[2].activated.connect(lambda:self.convey2(2))
        self.enzymeBox[3].activated.connect(lambda:self.convey2(3))
        self.enzymeBox[4].activated.connect(lambda:self.convey2(4))
        self.deleteEnz[0].clicked.connect(lambda:self.delete(0))
        self.deleteEnz[1].clicked.connect(lambda: self.delete(1))
        self.deleteEnz[2].clicked.connect(lambda: self.delete(2))
        self.deleteEnz[3].clicked.connect(lambda: self.delete(3))
        self.deleteEnz[4].clicked.connect(lambda: self.delete(4))
        self.species = None
        self.seq = {}
        self.enzyme = None
        self.avoidREList = []
        self.result = []
        self.REPrint = []
        self.palette = palette
        self.palette1 = palette1
        self.font = font

    def convey1(self):
        self.lineEdit.setText(self.comboBox.currentText())

    def convey2(self,id):
        if self.enzymeBox[id].currentText() in self.tableline2[id].text().split(','):
            pass
        else:
            self.tableline2[id].setText(self.tableline2[id].text() + self.enzymeBox[id].currentText() + ',')

    def delete(self,id):
        x = self.tableline2[id].text()
        y = x.split(',')
        text = ''
        if len(y) > 1:
            for i in y[0 : len(y)-2]:
                text = text + i + ','
            self.tableline2[id].setText(text)
        else:
            self.tableline2[id].setText('')

    def handleTextChange(self):
        self.comboBox.clear()
        self.species = self.lineEdit.text()
        S = Search(self.species)
        if S.species_getter() != []:
            for species in S.species_getter():
                self.comboBox.addItem(species)
        else:
            self.comboBox.addItem('(None)')

    def handleCalc(self):
        self.species = self.comboBox.currentText()
        for i in range(0,self.x):
            if self.tableline1[i].text() != '':
                if self.seqChoice[i].checkedId() == 1:
                    if isDNA(self.tableline1[i].text()):
                        self.seq['DNA{}'.format(i)] = self.tableline1[i].text()
                    else:
                        QMessageBox.warning(self.window, 'Error Warning!', 'The DNA sequence on line {} is wrong!'.format(i))
                elif self.seqChoice[i].checkedId() == 2:
                    if isAA(self.tableline1[i].text()):
                        self.seq['AA{}'.format(i)] = self.tableline1[i].text()
                    else:
                        QMessageBox.warning(self.window, 'Error Warning!',
                                            'The AA sequence on line {} is wrong!'.format(i))
                else:
                    QMessageBox.warning(self.window, 'Error Warning!', 'Please choose the seq type!')
                self.avoidREList.append(self.tableline2[i].text().split(',')[0:len(self.tableline2[i].text().split(','))-1])
                text = ''
                for element in self.tableline2[i].text().split(',')[0:len(self.tableline2[i].text().split(','))-1]:
                    text = text + element + ','
                self.REPrint.append(text[0:len(text)-1])


    def insertRow(self):
        if self.tableline1[self.x].text() != '':
            self.x += 1
            row = Rows(self.x)
            line1 = QLineEdit(self.window)
            line2 = QLineEdit(self.window)
            line3 = QLineEdit(self.window)
            line1.setPalette(self.palette1)
            line2.setPalette(self.palette1)
            line3.setPalette(self.palette1)
            box = QComboBox(self.window)
            seq = QButtonGroup(self.window)
            seq1 = QRadioButton(self.window)
            seq2 = QRadioButton(self.window)
            seq.addButton(seq1, 1)
            seq.addButton(seq2, 2)
            seq1.setText('DNA')
            seq2.setText('AA')
            delete = QPushButton(self.window)
            line1.move(int(150*self.screenWidth/3000), int((450+70*self.x)*self.screenHeight/2000))
            line1.resize(int(400*self.screenWidth/3000), int(70*self.screenHeight/2000))
            line2.move(int(700*self.screenWidth/3000), int((450+70*self.x)*self.screenHeight/2000))
            line2.resize(int(200*self.screenWidth/3000), int(70*self.screenHeight/2000))
            line3.move(int(550 * self.screenWidth / 3000), int((450 + 70 * self.x) * self.screenHeight / 2000))
            line3.resize(int(150*self.screenWidth/3000), int(70*self.screenHeight/2000))
            box.move(int(900*self.screenWidth/3000), int((450+70*self.x)*self.screenHeight/2000))
            box.resize(int(150*self.screenWidth/3000), int(70*self.screenHeight/2000))
            seq1.move(int(550*self.screenWidth/3000), int((450+70*self.x)*self.screenHeight/2000))
            seq1.resize(int(200*self.screenWidth/3000), int(70*self.screenHeight/2000))
            seq2.move(int(630*self.screenWidth/3000), int((450+70*self.x)*self.screenHeight/2000))
            seq2.resize(int(200*self.screenWidth/3000), int(70*self.screenHeight/2000))
            delete.move(int(1050*self.screenWidth/3000), int((450+70*self.x)*self.screenHeight/2000))
            delete.resize(int(50*self.screenWidth/3000), int(70*self.screenHeight/2000))
            delete.setText('Del')
            for key in self.d.myDict.keys():
                box.addItem(key)
            self.tableline1.append(line1)
            self.tableline2.append(line2)
            self.enzymeBox.append(box)
            self.seqChoice.append(seq)
            self.deleteEnz.append(delete)
            self.tableRow.append(row)
            for i in range(0, self.x+1):
                self.enzymeBox[i].activated.connect(lambda: self.convey2(i))
                self.deleteEnz[i].clicked.connect(lambda: self.delete(i))
            line1.show()
            line2.show()
            line3.show()
            box.show()
            delete.show()
            seq1.show()
            seq2.show()
        else:
            QMessageBox.warning(self.window, 'Nonsense Warning!', 'Please fill in the existing blanks!')

    def debug(self):
        print(self.seq)

    def main(self):
        # DNASequence='CGGCCGCGGCCGGACACGAATTCTAGCCATAGCGCGGCCGTCGTATTTGA'
        # aaSequence=SGSSGSSGSSGSSGSSGSSGSSGSSGSSG'
        # Species="Esc"
        Choice=True
        myData = DataPackage(self.species, Choice)
        # print(myData.getWebSite())
        # myData.setaaSequence(aaSequence)
        i = 0
        for key in self.seq.keys():
            myData.setAvoidREList(self.avoidREList[i])
            i += 1
            if key[0:3] == 'DNA':
                myData.setDNASequence(self.seq[key])
            else:
                myData.setaaSequence(self.seq[key])
            responce = requests.get(myData.url[0])
            # print(responce.text)
            soup = BeautifulSoup(responce.text, 'html.parser')
            # print(soup.pre)
            text = str(soup.pre)
            context = text[5:-6]
            # print(context)
            myCodonBias = codonBias(context)
            myData.setCodonBias(myCodonBias)
            # print(myData.aaSequence)
            myData.CalculationP2N()
            self.result.append(myData.DNASequence)
            #print(myData.DNASequence)
        #QMessageBox.about(self.window,'Result', 'The sequence required：' + myData.CalculationP2N())
        output = sys.stdout
        outputfile = open("result.txt", "a")
        sys.stdout = outputfile
        now = datetime.datetime.now()
        print('--------------------------------\n')
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        print('\nResult: {}\tSpecies: {}\n'.format(len(self.result), self.species))
        print('Gene Name\tDNA sequence\tAvoid restriction sites\n')
        data = []
        for i in range(0,len(self.result)):
            print('{}\t{}\t{}\n'.format(i, self.result[i], self.REPrint[i]))
            data.append(['{}'.format(i), self.result[i], self.REPrint[i]])
        df = pd.DataFrame(data, columns=['Gene Name','DNA sequence', 'Avoid restriction sites'])
        writer = pd.ExcelWriter('result_'+now.strftime("%Y-%m-%d_%H-%M-%S")+'.xlsx')
        df.to_excel(writer, startrow=1)
        ws = writer.sheets['Sheet1']
        ws.write_string(0, 0, '\nResult: {}\tSpecies: {}\n'.format(len(self.result), self.species))
        writer.save()
        #df.to_excel('result_'+now.strftime("%Y-%m-%d_%H-%M-%S")+'.xlsx')
        self.sub = Subwindow(df, len(self.result), self.species)
        self.sub.SubWindow.show()


class Rows:
    def __init__(self,id):
        self.line = id

class Subwindow():
    def __init__(self, df, result_num, species):
        self.SubWindow = QMainWindow()
        desktop = QApplication.desktop()
        self.screenWidth = desktop.width()
        self.screenHeight = desktop.height()
        self.SubWindow.resize(int(self.screenWidth * 0.5), int(self.screenHeight * 0.6))
        self.df = df
        self.result_num = result_num
        self.species = species

        palette = QPalette()
        brush1 = QBrush(QColor(170, 170, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        brush2 = QBrush(QColor(240, 240, 240, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush2)

        font = QFont()
        font.setBold(True)
        font.setWeight(75)

        self.TitleLine = QLineEdit(self.SubWindow)
        self.TitleLine.move(int(150*self.screenWidth/3000), int(150*self.screenHeight/2000))
        self.TitleLine.resize(int(550*self.screenWidth/3000), int(60*self.screenHeight/2000))
        self.TitleLine.setText('Result: {}'.format(self.result_num))
        self.TitleLine.setEnabled(False)

        self.SpeciesLine = QLineEdit(self.SubWindow)
        self.SpeciesLine.move(int(800*self.screenWidth/3000), int(150*self.screenHeight/2000))
        self.SpeciesLine.resize(int(550*self.screenWidth/3000), int(60*self.screenHeight/2000))
        self.SpeciesLine.setText('Species:'+self.species)
        self.TitleLine.setReadOnly(False)

        self.label1 = QLineEdit(self.SubWindow)
        self.label1.move(int(150*self.screenWidth/3000), int(380*self.screenHeight/2000))
        self.label1.resize(int(150*self.screenWidth/3000), int(70*self.screenHeight/2000))
        self.label1.setText(" Gene Name")
        self.label1.setReadOnly(True)
        self.label1.setPalette(palette)
        self.label1.setFont(font)

        self.label2 = QLineEdit(self.SubWindow)
        self.label2.move(int(300*self.screenWidth/3000), int(380*self.screenHeight/2000))
        self.label2.resize(int(550*self.screenWidth/3000), int(70*self.screenHeight/2000))
        self.label2.setText("               DNA sequence")
        self.label2.setReadOnly(True)
        self.label2.setPalette(palette)
        self.label2.setFont(font)

        self.label3 = QLineEdit(self.SubWindow)
        self.label3.move(int(850*self.screenWidth/3000), int(380*self.screenHeight/2000))
        self.label3.resize(int(350*self.screenWidth/3000), int(70*self.screenHeight/2000))
        self.label3.setText(" Avoid restriction sites")
        self.label3.setReadOnly(True)
        self.label3.setPalette(palette)
        self.label3.setFont(font)

        self.SeqResult = []
        self.Enzyme = []
        self.Genename = []
        for i in range(0, self.result_num):
            line1 = QLineEdit(self.SubWindow)
            line2 = QLineEdit(self.SubWindow)
            line3 = QLineEdit(self.SubWindow)
            line1.move(int(150*self.screenWidth/3000), int((450+70*i)*self.screenHeight/2000))
            line2.move(int(250*self.screenWidth/3000), int((450+70*i)*self.screenHeight/2000))
            line3.move(int(800*self.screenWidth/3000), int((450+70*i)*self.screenHeight/2000))
            line1.resize(int(100*self.screenWidth/3000), int(70*self.screenHeight/2000))
            line2.resize(int(550*self.screenWidth/3000), int(70*self.screenHeight/2000))
            line3.resize(int(300*self.screenWidth/3000), int(70*self.screenHeight/2000))
            line1.setText(self.df.iloc[i, 0])
            line2.setText(self.df.iloc[i, 1])
            line3.setText(self.df.iloc[i, 2])
            line1.setReadOnly(False)
            line2.setReadOnly(False)
            line3.setReadOnly(False)
            self.Genename.append(line1)
            self.SeqResult.append(line2)
            self.Enzyme.append(line3)


