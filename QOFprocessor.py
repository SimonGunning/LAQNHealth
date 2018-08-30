#Read the QOF File. Get all London Practices. Join with Practice File (epracur)
# This requires the latest version of Pandas
import pandas as pd
import requests
import json
from tkinter  import Tk
from tkinter.filedialog import askopenfilename
print("Enter the year of the QOF")
year = input("Year =")
print("Enter the disease that you wish to get data for (AST, COPD,....")
disease = input("Disease =")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)
#'C:\\Users\\gunning\\Documents\\simon\\MSCProject\\qof-1516-prev-ach-exc-resp-prac-v2.xlsx'
qofDF = pd.read_excel(filename, sheet_name='AST', usecols=[2,9,12,13])
qofDF.columns = ['RegionName', 'PracticeCode', 'ListSize', 'Register']
#print(qofDF.head(15))
qofDF['Year'] = year
#qofDF['Year'] = year
LondonQofDF = qofDF.loc[qofDF['RegionName'] == "LONDON"]
# returns 1330 rows
print(LondonQofDF.head(10))

#read epracur file

PracticeLocations = pd.read_csv('C:\\Users\\gunning\\Documents\\simon\\MSCProject\\epraccur.csv')
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
outPutFileName = "LondonQOF" + year
LondonQofDF.to_csv(outPutFileName)

#There may be more than 1 surgery per ward aggregate the surgeries prevalences within the ward
#then the file will be ready for rendering in a map

