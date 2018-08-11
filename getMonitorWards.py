#http://api.erg.kcl.ac.uk/AirQuality/Annual/MonitoringObjective/GroupName=LAQN/Year=2018/Json
#api.postcodes.io/postcodes?lon=0.074372&lat=51.541119


import requests
import json
import pandas as pd
import pickle
df = pd.DataFrame(columns=['Ward','Monitor','Longitude','Latitude','NO2','PM10','DUST'])
#df = {}


r = requests.get('http://api.erg.kcl.ac.uk/AirQuality/Annual/MonitoringObjective/GroupName=LAQN/Year=2018/Json')
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
#    print(wardLookUpq)
    s = requests.get(wardLookUpq)
#    print(s.status_code)
    s.json()
    locations = json.loads(s.text)
    try:
        res = locations["result"][0]["admin_ward"]
        df.loc[res] = [res,mySiteCode, Site['@Longitude'], Site['@Latitude'], myNO2, myPM10, dust]

    except TypeError:
        print("no ward data")
        print(mySiteCode)
    count = count +1
print(df)
with open('parrot1.pickle', 'wb') as handle:
    pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

#df.to_pickle("./parrot.pkl")
print(count)
