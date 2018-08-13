#Read the QOF File. Get all London Practices. Join with Practice File (epracur)
import pandas as pd

qofDF = pd.read_excel('C:\\Users\\gunning\\Documents\\simon\\MSCProject\\qof-1617-prev-ach-exc-resp-prac.xlsx',
                      sheetname="AST")
#print(qofDF.head(15))
qofDF = qofDF.loc[qofDF['Unnamed: 2'] == "LONDON"]
print(qofDF.head(5))
#read epracur file
PracticeLocations = pd.read_csv('C:\\Users\\gunning\\Documents\\simon\\MSCProject\\epraccur.csv', names = ["A", "B", "C", "D"])
print(PracticeLocations.info())

print(PracticeLocations.head(5))


