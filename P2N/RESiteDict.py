import pandas as pd

class RESiteDict(object):
    def __init__(self):
        RE_Site_Data=pd.read_table('RestrictEnzyme Collection.txt', sep='\t', engine='python')
        # print(RE_Site_Data)
        self.myDict=RE_Site_Data.groupby('Name')['Recognition Site'].apply(list).to_dict()
        # print(self.myDict)

    def getRestrictionSite(self,REName):
        return self.myDict[REName][0]

    def getRestrictionSiteList(self,REList):
        SiteList=[]
        for RE in REList:
            Site=self.getRestrictionSite(RE)
            SiteList.append(Site)
        return SiteList

