import requests

class DataViewRestClient():
    def __init__(self, endpoint, authtoken, certificate=None):
      self.ENDPOINT = endpoint
      self.AUTHTOKEN = authtoken
      self.CERTIFICATE = certificate
      
      if not self.ENDPOINT.endswith('/'):
        self.ENDPOINT = self.ENDPOINT + '/'

    def get_headers(self):
      headers = {'Authorization': 'Token: ' + self.AUTHTOKEN, 'Accept': 'application/json'}

    def list_models(self, name):
      r = requests.get(self.ENDPOINT + '' + name, headers=self.get_headers(), verify=self.CERTIFICATE)

      if r.status_code == 200:
        return r.json()
      else:
        raise Exception(r.status_code, r.text)

    def create_model(self, name, values):
      r = requests.post(self.ENDPOINT + '' + name + '/', headers=self.get_headers(), verify=self.CERTIFICATE, data=values)

      if r.status_code == 201:
        return r.json()
      else:
        raise Exception(r.status_code, r.text)

    def get_model(self, name, key):
      r = requests.get(self.ENDPOINT + '' + name + '/' + str(key), headers=self.get_headers(), verify=self.CERTIFICATE)

      if r.status_code == 200:
        return r.json()
      else:
        raise Exception(r.status_code, r.text)
      
    def update_model(self, name, key, values):
      r= requests.get(self.ENDPOINT + '' + name + '/' + str(key), headers=self.get_headers(), verify=self.CERTIFICATE, data=values)

    def delete_model(self):
      r= requests.delete(self.ENDPOINT + '' + name + '/' + str(key), headers=self.get_headers(), verify=self.CERTIFICATE)

      if r.status_code == 200:
        return r.json()
      else:
        raise Exception(r.status_code, r.text)
