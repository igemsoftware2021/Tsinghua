import requests
from bs4 import BeautifulSoup
import urllib
from RestrictEnzyme import *

f = open("RE Site Collection-from GenSmart.txt","r")   #设置文件对象
str = f.read()     #将txt文件的所有内容读入到字符串str中
f.close()   #将文件关闭

# print(str)
soup=BeautifulSoup(str,'html.parser')
RESet=[]
#print(soup.option.children)
for item in soup.find_all('option'):
    cacheString=item.string
    # print(cacheString)
    index1=cacheString.find(' ')
    name=cacheString[0:index1]
    index2=cacheString.find('[')
    index3=cacheString.find(']')
    recognitionSite=cacheString[index2+1:index3]
    # print('Name:' + name + '\tRecognition Site:' + recognitionSite)
    newRE=RestrictEnzyme(name,recognitionSite)
    RESet.append(newRE)

OutPut='Name\tRecognition Site\n'
for RE in RESet:
    OutPut=OutPut+RE.getREMessage()
OutPutData=open('RestrictEnzyme Sheet.txt','w+')
print(OutPut,file=OutPutData)
OutPutData.close()

for RE in RESet:
    RE.printRE()
    # print()
