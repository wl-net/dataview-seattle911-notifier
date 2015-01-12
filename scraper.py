#!/usr/bin/python

import requests, json, time, urllib
from bs4 import BeautifulSoup

class Seattle911IncidentProcessor:
    def __init__(self, processor):
        self.RECORDS_URL = 'http://www2.ci.seattle.wa.us/fire/realtime911/getRecsForDatePub.asp?action=Today&incDate=&rad1=des'
        self.processor = processor
        pass
    
    def parse_incidents(self):            
        soup = BeautifulSoup(requests.get(self.RECORDS_URL).content)
        rows = soup.find_all('table')[3].find_all('tr')
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
            recorded = json.load(open('incidents.json'))
        except Exception as inst:
            recorded = []

        try:
            for incident in incidents:
                if not incident['number'] in recorded:
                    self.processor.process(incident)

            self.save_state(recorded)
        except Exception as e:
            print("Caught Exception: " + str(e))
            self.save_state(recorded)

    def save_state(self, incidents):
        savefile = open('incidents.json', 'w')
        savefile.write(json.dumps(incidents))
        savefile.close()
