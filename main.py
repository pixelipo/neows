import os
import time

import ssl
import http
import urllib.request, urllib.parse, urllib.error
import json
import sqlite3


from app import db

# init vars
api_key = 'DEMO_KEY' # Fallback api_key if env folder configuration is missing
page = 1
total = 2

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
    parms['page'] = str(page)
    size = '20'
    baseUrl = 'https://api.nasa.gov/neo/rest/v1/neo/browse?'
    print('Listing last', size, 'items from page', parms['page'])


## Lookup NEO object
if (service == '2'):
    # example: https://api.nasa.gov/neo/rest/v1/neo/3542519?api_key=DEMO_KEY
    baseUrl = 'https://api.nasa.gov/neo/rest/v1/neo/2003200/?'
    neoId = '2003200'
    print("Looking up object", 'neoId')

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

while page <= total:
    url = baseUrl + urllib.parse.urlencode(parms)
    print(url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()

    # fetch remaining rate limit from response headers
    remaining = uh.info()['X-RateLimit-Remaining']
    print('Requests remaining:', remaining)
    if (int(remaining) == 0) : break

    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
        parms['page'] = str(int(parms['page']) + 1)
        total = int(js['page']['total_pages'])
    except:
        print(data)  # We print in case unicode causes an error

    # print(js['links'])
    conn = db.initDb('neows.sqlite')
    cur = conn.cursor()


    for i, neo in enumerate(js['near_earth_objects']):
        db.insertObj(
            cur=cur,
            id=neo['id'],
            name=neo['name'],
            hazardous=neo['is_potentially_hazardous_asteroid'],
            diameter_min=neo['estimated_diameter']['kilometers']['estimated_diameter_min'],
            diameter_max=neo['estimated_diameter']['kilometers']['estimated_diameter_max']
        )

        conn.commit()

        for cad in neo['close_approach_data']:
            db.insertApproach(
                cur=cur,
                date=cad['epoch_date_close_approach'],
                miss=cad['miss_distance']['kilometers'],
                object_id=neo['id']
            )

        # if i == len(js['near_earth_objects']) :
        #     print('Pausing for a bit...')
        #     time.sleep(5)
        # # neo_raw = new NeoRaw()
        # print(neo['name'], "is potentially hazardous:", neo['is_potentially_hazardous_asteroid'])

        # SELECT DISTINCT Object.name, Object.hazardous, Approach.miss FROM Object JOIN Approach ON Object.id = Approach.object_id ORDER by Approach.miss DESC LIMIT 10;
