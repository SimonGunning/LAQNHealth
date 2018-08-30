#http://api.erg.kcl.ac.uk/AirQuality/Annual/MonitoringObjective/GroupName=LAQN/Year=2018/Json
#api.postcodes.io/postcodes?lon=0.074372&lat=51.541119


import requests
import json
import pandas as pd
import pickle
import time
print("Enter the year that you wish to get pollution monitor data for.")
year = input("Year =")

RequestString = "http://api.erg.kcl.ac.uk/AirQuality/Annual/MonitoringObjective/GroupName=LAQN/Year=" + year + "/Json"
df = pd.DataFrame(columns=['Year','Ward','Monitor','Longitude','Latitude','NO2','PM10','DUST'])
df.index.name = 'WardCode'
#r = requests.get('http://api.erg.kcl.ac.uk/AirQuality/Annual/MonitoringObjective/GroupName=LAQN/Year=2018/Json')
r = requests.get(RequestString)

print(r.status_code)
r.json()
count = 0
monitors = json.loads(r.text)
print(type(monitors))
print(type(monitors["SiteObjectives"]))

for Site in monitors["SiteObjectives"]["Site"]:
#    print(type(Site))
#    print(Site["@SiteCode"])
    dust = ""
    myNO2 = ""
    myPM10 = ""
    res = ""
    mySiteCode = Site["@SiteCode"]
    myObjectives = Site["Objective"]
    for obs in myObjectives:
        if obs["@ObjectiveName"] == "40 ug/m3 as an annual mean":
            if (obs["@SpeciesCode"]) == "DUST":
                dust = obs["@Value"]
            elif (obs["@SpeciesCode"]) == "NO2":
                myNO2 = obs["@Value"]
            elif   (obs["@SpeciesCode"]) == "PM10":
                myPM10 = obs["@Value"]

    wardLookUpq = "http://api.postcodes.io/postcodes?lon=" + Site["@Longitude"] + "&lat=" + Site["@Latitude"]
#    time.sleep(3)
#    print(wardLookUpq)
    s = requests.get(wardLookUpq)
    s.json()
    locations = json.loads(s.text)
#    if locations["result"][0]["admin_ward"] is None:
#        print("loc res 1 = " + locations["result"][1]["admin_ward"])
#    print(locations["result"][0]["codes"]["admin_ward"])
    try:
        res = locations["result"][0]["admin_ward"]
        df.loc[locations["result"][0]["codes"]["admin_ward"]] = [year, res,mySiteCode, Site['@Longitude'], Site['@Latitude'], myNO2, myPM10, dust]

    except TypeError:
        NoLoc = "NoLoc" + str(count)
        df.loc[NoLoc] = [year, NoLoc,mySiteCode, Site['@Longitude'], Site['@Latitude'], myNO2, myPM10, dust]

        print("no ward data " + mySiteCode)
        print("res " + res)
#        print("loc res conty = " + locations["result"][0]["admin_county"])
        print("long " + Site['@Longitude'])
        print("lat " + Site['@Latitude'])
        print("myNO2 " + myNO2)
        print("myPM10 " + myPM10)
        print("dust " + dust)
        print(s.status_code)

    count = count +1
#print(df)
MonitorWardsFile = "MonitorWardsFile" + year
df.to_csv("MonitorWardsFile")
#with open('parrot1.pickle', 'wb') as handle:
#    pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

#df.to_pickle("./parrot.pkl")
print(count)
