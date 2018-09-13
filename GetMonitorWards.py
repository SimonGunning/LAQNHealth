# This program takes the year from the command line. Then it calls the LAQN API using the year.
# This returns a JSON response with all the monitor readings for that year.
# This is parsed. Then the postcodes API is called using longitude and latitude to look up the ward
# where the monitor is located. The output is a csv file of monitors wards and annual pollution readings
# The 2 APIs are at:
# http://api.erg.kcl.ac.uk/AirQuality/Annual/MonitoringObjective/GroupName=LAQN/Year=2018/Json
# api.postcodes.io/postcodes?lon=0.074372&lat=51.541119


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
r = requests.get(RequestString)
r.json()
count = 0
monitors = json.loads(r.text)


for Site in monitors["SiteObjectives"]["Site"]:
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
    s = requests.get(wardLookUpq)
    s.json()
    locations = json.loads(s.text)
    try:
        res = locations["result"][0]["admin_ward"]
        df.loc[locations["result"][0]["codes"]["admin_ward"]] = [year, res,mySiteCode, Site['@Longitude'], Site['@Latitude'], myNO2, myPM10, dust]

    except TypeError:
        NoLoc = "NoLoc" + str(count)
        df.loc[NoLoc] = [year, NoLoc,mySiteCode, Site['@Longitude'], Site['@Latitude'], myNO2, myPM10, dust]

    count = count +1
MonitorWardsFile = "MonitorWardsFile-" + year
df.to_csv(MonitorWardsFile)

