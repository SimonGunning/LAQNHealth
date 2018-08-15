#Read the QOF File. Get all London Practices. Join with Practice File (epracur)
# This requires the latest version of Pandas
import pandas as pd

qofDF = pd.read_excel('C:\\Users\\gunning\\Documents\\simon\\MSCProject\\qof-1516-prev-ach-exc-resp-prac-v2.xlsx',
                      sheet_name='AST', usecols=[2,9,14,17])
qofDF.columns = ['RegionName', 'PracticeCode', 'Y1Prevalence', 'Y2Prevalance']
print(qofDF.head(15))

LondonQofDF = qofDF.loc[qofDF['RegionName'] == "LONDON"]
# returns 1330 rows
print(LondonQofDF.head(4))

#read epracur file

PracticeLocations = pd.read_csv('C:\\Users\\gunning\\Documents\\simon\\MSCProject\\epraccur.csv')
PracticeLocations.columns = ["PracticeCode", "2", "3", "4", "5", "6", "7", "8", "9","Postcode","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27"]
#print("PrLOc info = " + PracticeLocations.info())
#LondonQofDF = pd.merge(PracticeLocations, LondonQofDF, left_on='PracticeCode', right_on='PracticeCode: 11', how='inner')
print(PracticeLocations.head(5))

#postcodes are col 9
#print(PracticeLocations.iloc[:,[9]])


