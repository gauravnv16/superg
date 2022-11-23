import json
import urllib2

from datetime import datetime


class Api(object):
    def __init__(self):
        self.server_key = "AIzaSyAZ2vppCUJkh-EEcx164C2rgWS3Fb2YmI0"
        self.table_id = "1oAIu-g2fXBKVYown0m5m8BYf2Ubgt9CJraqmXU0r"
        self.base_url = "https://www.googleapis.com/fusiontables/v2"
        self.client_id = "570232241224-qbog6b9c9r5qamq0qkt9vpfcd0hubu3q.apps.googleusercontent.com"
        self.client_secret = "tFuui76RzsDvtN8xBKg-aeyg"
        self.redirect_uri = "http://localhost:8000/"

    def get_auth_url(self):
        return '%s?client_id=%s&redirect_uri=%s&scope=%s&response_type=code' % (
            'https://accounts.google.com/o/oauth2/auth',
            self.client_id,
            self.redirect_uri,
            'https://www.googleapis.com/auth/fusiontables'
        )

    def get_table(self):
        url = "%s/tables/%s?key=%s" % (self.base_url, self.table_id, self.server_key)
        data = self.make_request(url)
        return data

    def get_datas(self):
        sql = "SELECT * FROM %s" % self.table_id
        url = "%s/query?sql=%s&key=%s" % (self.base_url, sql, self.server_key)
        data = self.make_request(url)
        return data

    def insert_data(self, data):
        now = datetime.now().strftime("%Y-%m-%d")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        address = data.get("address")
        sql = "INSERT INTO %s (Date, latitude, longitude, address) VALUES ('%s', '%s', '%s', '%s')" % (
            self.table_id, now, latitude, longitude, address
        )
        print sql
        url = "%s/query?sql=%s&key=%s" % (self.base_url, sql, self.server_key)
        print url
        data = self.make_request(url, method="POST")
        return data

    def make_request(self, url, method="GET"):
        url = urllib2.quote(url, safe=":/=?*&(),")
        print url
        if method == "GET":
            response = urllib2.urlopen(url)
        elif method == "POST":
            request = urllib2.Request(url, {})
            response = urllib2.urlopen(request)
        data = response.read()
        json_data = json.loads(data)
        return json_data


"""
from map.api import Api
api = Api()
data = {"latitude": 41.0343050853874, "longitude": 29.080810546875, "address": "Test"}
api.insert_data(data)




from sherpany import settings
from oauth2client.service_account import ServiceAccountCredentials
file_path = "%s/static/sherpany-694ffd3384ff.json" % settings.BASE_DIR
scopes = ['https://www.googleapis.com/auth/fusiontables']
credentials = ServiceAccountCredentials.from_json_keyfile_name(file_path, scopes=scopes)

from httplib2 import Http
http_auth = credentials.authorize(Http())
from apiclient.discovery import build
fusion = build('fusiontables', 'v2', http=http_auth)
query = fusion.query()
sql1 = "SELECT * FROM 1oAIu-g2fXBKVYown0m5m8BYf2Ubgt9CJraqmXU0r"
data = query.sql(sql=sql1)
data.execute()

sql = "INSERT INTO 1oAIu-g2fXBKVYown0m5m8BYf2Ubgt9CJraqmXU0r (Date, latitude, longitude, address) VALUES ('2016-03-16', '2', '2', '2')"
sql = "INSERT INTO 1oAIu-g2fXBKVYown0m5m8BYf2Ubgt9CJraqmXU0r (Date,latitude,longitude,address) VALUES ('2016-03-16','41.0343050854','29.0808105469','Test')"



from sherpany import settings
secret_name = "client_secret_570232241224-qbog6b9c9r5qamq0qkt9vpfcd0hubu3q.apps.googleusercontent.com"
file_path = "%s/static/%s.json" % (settings.BASE_DIR, secret_name)

from oauth2client.client import flow_from_clientsecrets
flow = flow_from_clientsecrets(file_path, scope='https://www.googleapis.com/auth/fusiontables', redirect_uri='http://localhost:8000')



"""
