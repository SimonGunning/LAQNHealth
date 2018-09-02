#Read the QOF File. Get all London Practices. Join with Practice File (epracur)
# This requires the latest version of Pandas
import pandas as pd
import requests
import json
from tkinter  import Tk
from tkinter.filedialog import askopenfilename
QOFMetaData = [[2013,0,6,8,9],[2014,0,12,14,15],[2015,0,9,12,13],[2016,0,11,13,14],[2017,0,11,16,17]]
QOFMetaDatadf = pd.DataFrame(QOFMetaData,columns=['Year','RegionPos','PracticeCodePos','ListSizePos','RegisterPos'])
QOFMetaDatadf = QOFMetaDatadf.set_index('Year')
print(QOFMetaDatadf)
print("Enter the year of the QOF")
year = input("Year =")
#print(QOFMetaDatadf.loc[int(year)]['ListSizePosition'])
print("Enter the disease that you wish to get data for (AST, COPD,....")
disease = input("Disease =")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(title = "Select QOF file") # show an "Open" dialog box and return the path to the selected file
print(filename)
#qofDF = pd.read_excel(filename, sheet_name='AST', usecols=[2,9,12,13])
qofDF = pd.read_excel(filename, sheet_name=disease,
                      usecols=[QOFMetaDatadf.loc[int(year)]['RegionPos'],
                               QOFMetaDatadf.loc[int(year)]['PracticeCodePos'],
                               QOFMetaDatadf.loc[int(year)]['ListSizePos'],
                               QOFMetaDatadf.loc[int(year)]['RegisterPos']])

qofDF.columns = ['RegionCode', 'PracticeCode', 'ListSize', 'Register']
#print(qofDF.head(15))
qofDF['Year'] = year
#qofDF['Year'] = year
LondonQofDF = qofDF.loc[qofDF['RegionCode'] == "Y56"]
# returns 1330 rows
print(LondonQofDF.head(10))

#read epracur file
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(title = "Select Practices file") # show an "Open" dialog box and return the path to the selected file
print(filename)

PracticeLocations = pd.read_csv(filename)
PracticeLocations.columns = ["PracticeCode", "2", "3", "4", "5", "6", "7", "8", "9","Postcode","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27"]
#print(PracticeLocations[["PracticeCode", "Postcode"]])

#print("PrLOc info = " + PracticeLocations.info())
LondonQofDF = pd.merge(PracticeLocations[["PracticeCode", "Postcode"]], LondonQofDF, left_on='PracticeCode', right_on='PracticeCode', how='inner')
#LondonQofDF = LondonQofDF.head(10)

print(LondonQofDF)

#for each LondonQOF get the Ward. Then merge the ward into the DF
PCLookupList = LondonQofDF["Postcode"].tolist()
print("PCLookupListLEN " + str(len(PCLookupList)))
# the api only accepts 100 postcodes at a time
# make len(PCLookupList) /100 calls to the api
#the dups start after here
PCLookupListIterations = (len(PCLookupList) // 100) + 1
remainder = len(PCLookupList) % 100

j = 0
k = 0
WardsPostCodesDF = pd.DataFrame(columns=['Postcode', 'Ward', 'WardCode','PracticeLongitude','PracticeLatitude'])

for i in range (0, PCLookupListIterations):
    k = j + 100
    print("look up list")
    lenLookupList = len(PCLookupList[j:k])
    postData = "{'postcodes' : " + str(PCLookupList[j:k]) + "}"
    postData = postData.replace("'",'"')
    d = json.loads(postData)
    print("k is " + str(k))
    print("j is " + str(j))
    print(d)
    s = requests.post("https://api.postcodes.io/postcodes", json=d)
    s.json()
    locations = json.loads(s.text)
    print(locations)
    m = 0
    if lenLookupList % 100 != 0:
        print("lll is " + str(lenLookupList))
        k = lenLookupList + j
        print("new k is " + str(k))
        print("new j is " + str(j))
    for l in range (j,k):
#        print(locations["result"][m]["result"])
        if locations["result"][m]["result"] is not None:
            WardsPostCodesDF.loc[l] = [PCLookupList[l], locations["result"][m]["result"]["admin_ward"],
                                       locations["result"][m]["result"]["codes"]["admin_ward"],
                                       locations["result"][m]["result"]["longitude"],
                                       locations["result"][m]["result"]["latitude"]]
#            WardsDF.append([PCLookupList[l], locations["result"][m]["result"]["admin_ward"]])

#        print(WardsDF.loc[l])
        m = m + 1
    j = j + 100
WardsPostCodesDF.drop_duplicates(subset="Postcode", keep="first", inplace=True)
WardsPostCodesDF.to_csv("WardsPostcode2")
# now merge WardsDF with the LondonQofDF
LondonQofDF = pd.merge(WardsPostCodesDF, LondonQofDF, left_on='Postcode', right_on='Postcode', how='inner')
outPutFileName = "LondonQOF-" + year
LondonQofDF.to_csv(outPutFileName)

#There may be more than 1 surgery per ward aggregate the surgeries prevalences within the ward
#then the file will be ready for rendering in a map

