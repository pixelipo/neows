import os
# import time


from app import crawl, line

# init vars
api_key = 'DEMO_KEY' # Fallback api_key if env folder configuration is missing

# fetch secrets from local file
if os.path.isfile('env/conf.py'):
    from env.conf import config
    api_key = config['api_key']

parms = dict()
parms['api_key'] = api_key


service = input("Select service([1] Browse [2] Lookup [3] Feed [4] Generate plot data):")

## Browse data
if (service == '1'):
    # example: https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=DEMO_KEY
    parms['page'] = 1
    parms['size'] = 20
    total = parms['page'] + 1
    baseUrl = 'https://api.nasa.gov/neo/rest/v1/neo/browse?'
    while int(parms['page']) <= int(total):
        total = crawl.crawl(baseUrl, parms, total)


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

if (service == '4'):
    encounters = line.approach()
    print(line.jsonify(encounters))
