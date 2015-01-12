from dateutil.parser import parse

from rest_client import DataViewRestClient
from scraper import Seattle911IncidentProcessor

class DataviewNotifier():
    def __init__(self, api_endpoint, api_token):
        self.API_ENDPOINT = api_endpoint
        self.API_TOKEN = api_token
        
        self.client = DataViewRestClient(self.API_ENDPOINT, self.API_TOKEN)
        self.recorded = []

    def process(self, record):
      try:
        print("Response from dataview " + str(self.client.create_model('safety-incident', {'location': record['location'], 'time': parse(record['date']).strftime('%Y-%m-%d %H:%M:%S'), 'units': record['units'], 'type': record['type']})))
      except Exception as e:
          print(e)
      
      self.recorded.append(record['number'])

notifier = DataviewNotifier('', '')
processor = Seattle911IncidentProcessor(notifier, '')
incidents = processor.process_incidents(processor.parse_incidents())
