#!/usr/bin/python

import requests, json, time, urllib
from bs4 import BeautifulSoup

class Seattle911IncidentProcessor:

    def __init__(self, geofence):
        self.RECORDS_URL = 'http://www2.ci.seattle.wa.us/fire/realtime911/getRecsForDatePub.asp?action=Today&incDate=&rad1=des'
        self.GEOJSON_FENCE = geofence
        pass
    
    def parse_incidents(self):            
        soup = BeautifulSoup(requests.get(self.RECORDS_URL).content)
        rows = soup.find_all("table")[3].find_all("tr")
        incidents = []
        for row in rows:
            try:
                tds = row.find_all("td")
                a = {}
                if len(tds[0].contents) > 0:
                    a['date'] = tds[0].contents[0]
                else:
                    a['date'] = "Unknown"
                    print("Date missing!")
                if len(tds[1].contents) > 0:
                    a['number'] = tds[1].contents[0]
                else:
                    a['number'] = "Unknown"
                    print("Incident number missing!")
                if len(tds[2].contents) > 0:
                    a['level'] = tds[2].contents[0]
                else:
                    a['level'] = "Unknown"
                    print("Level missing for incident %s" % a['number'])
                if len(tds[3].contents) > 0:
                    a['units'] = tds[3].contents[0]
                else:
                    a['units'] = "Unknown"
                    print("Units missing for incident %s" % a['number'])
                if len(tds[4].contents) > 0:
                    a['location'] = tds[4].contents[0]
                else:
                    a['location'] = "Unknown"
                    print("Location missing for incident %s" % a['number'])
                if len(tds[5].contents) > 0:
                    a['type'] = tds[5].contents[0]
                else:
                    a['type'] = "Unknown"
                    print("Type missing for incident %s" % a['number'])
                incidents.append(a)
            except IndexError:
                print(row.prettify())

        return incidents

    def process_incidents(self, incidents):
        try:
            recorded = json.load(open("incidents.json"))
        except Exception as inst:
            recorded = []

        for incident in incidents:
            if not incident['number'] in recorded:
                print("Looking up %s" % incident["location"], end = '', flush = True)
                incident["location"] = incident['location'].replace('/', '%26').replace(' Av ', ' Ave ')
                recorded.append(incident['number'])

                try:
                        result = json.loads(requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=%s Seattle&components=administrative_area:WA|country:US" % incident["location"]).content.decode('utf-8'))
                        time.sleep(1)
                except:
                    time.sleep(30)
                    print("... Failed")

                if len(result['results']) != 1:
                        print("... \033[93mWARNING: Skipping %s - couldn't geocode it\033[0m" % incident['location'])
                        continue
                lat = result['results'][0]['geometry']['location']['lat']
                lng = result['results'][0]['geometry']['location']['lng']
                print("... %s, %s" % (lat, lng))

                if lat > self.GEOJSON_FENCE[0][0][1] and lat < self.GEOJSON_FENCE[0][1][1] and lng > self.GEOJSON_FENCE[0][0][0] and lng < self.GEOJSON_FENCE[0][2][0]:
                    print("\033[91mWARNING: %s %s falls within bounds\033[0m" % (incident['number'], incident['location']))
                    
        return incidents

processor = Seattle911IncidentProcessor()
incidents = processor.process_incidents(processor.parse_incidents())

savefile = open("incidents.json", "w")
savefile.write(json.dumps(recorded))
savefile.close()
    