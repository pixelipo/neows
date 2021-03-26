import os
import time

import ssl
import http
import urllib.request, urllib.parse, urllib.error
import json
import sqlite3


# init vars
api_key = 'DEMO_KEY' # Fallback api_key if env folder configuration is missing
page = '1'

# fetch secrets from local file
if os.path.isfile('env/conf.py'):
    from env.conf import config
    api_key = config['api_key']

parms = dict()
parms['api_key'] = api_key


service = input("Select service([1] Browse [2] Lookup [3] Feed):")

## Browse data
if (service == '1'):
    # example: https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=DEMO_KEY
    parms['page'] = page
    baseUrl = 'https://api.nasa.gov/neo/rest/v1/neo/browse?'
    print('Listing last', size, 'items:')


## Lookup NEO object
if (service == '2'):
    # example: https://api.nasa.gov/neo/rest/v1/neo/3542519?api_key=DEMO_KEY
    baseUrl = 'https://api.nasa.gov/neo/rest/v1/neo/?'
    parms['neoId'] = '3542519'
    print("Looking up object", parms['neoId'])

## Get data feed
if (service == '3'):
    # example: https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=DEMO_KEY
    baseUrl = 'https://api.nasa.gov/neo/rest/v1/feed?'
    parms['start_date'] = '2020-09-20'
    parms['end_date'] = '2020-09-25'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = baseUrl + urllib.parse.urlencode(parms)
print(url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()

# fetch remaining rate limit from response headers
print('Requests remaining:', uh.info()['X-RateLimit-Remaining'])

print('Retrieved', len(data), 'characters')
js = json.loads(data)

# print(js['links'])

for neo in js['near_earth_objects']:
    print(neo['name'], "is potentially hazardous:", neo['is_potentially_hazardous_asteroid'])
