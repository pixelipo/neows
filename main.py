from dotenv import dotenv_values
# import time

from app import crawl, line


parms = dict()
# fetch secrets from .env file
try:
    config = dotenv_values(".env")
    parms['api_key'] = config['API_KEY']
except:
    parms['api_key'] = 'DEMO_KEY'
    print("Credentials file not found, using limited 'DEMO_KEY'\n")


service = input("Select service:\n[1] Crawl\n[2] Lookup\n[3] Feed (disabled)\n[4] Generate plot data\n")

## Browse data
if (service == '1'):
    # example request: https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=DEMO_KEY
    parms['page'] = 1
    parms['size'] = 20
    total = parms['page'] + 1
    baseUrl = 'https://api.nasa.gov/neo/rest/v1/neo/browse?'
    while int(parms['page']) <= int(total):
        total = crawl.crawl(baseUrl, parms, total)


## Lookup NEO object
if (service == '2'):
    # example request: https://api.nasa.gov/neo/rest/v1/neo/3542519?api_key=DEMO_KEY
    print(crawl.lookup(input('Input object name or id:\n'), parms))


## Get data feed
if (service == '3'):
    # example: https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=DEMO_KEY
    baseUrl = 'https://api.nasa.gov/neo/rest/v1/feed?'
    parms['start_date'] = '2020-09-20'
    parms['end_date'] = '2020-09-25'

if (service == '4'):
    encounters = line.approach()
    print(line.jsonify(encounters))
