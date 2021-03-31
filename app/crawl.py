import json
import requests

from app import db


def crawl (baseUrl, parms, total):

    print('Fetching ', str(parms['size']), 'items from page', str(parms['page']) + '/' + str(total))
    response = requests.get(baseUrl, params=parms)

    # fetch remaining rate limit from response headers
    remaining = response.headers['X-RateLimit-Remaining']
    print('Requests remaining:', remaining)
    if (int(remaining) == 0) : return 0

    print('Retrieved', len(response.text), 'characters')

    try:
        js = response.json()
        parms['page'] = str(int(parms['page']) + 1)
        total = int(js['page']['total_pages'])
    except err:
        return err


    conn = db.initDb('data/db.sqlite3')
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

    return total


def lookup(name, params):
    conn = db.initDb('data/db.sqlite3')
    cur = conn.cursor()

    id = db.getObjectId(cur, name)
    if id is None:
        return "Object not found"

    url = 'https://api.nasa.gov/neo/rest/v1/neo/'+str(id[0])+'/?'
    response = requests.get(url, params=params)

    return json.dumps(response.json(), indent=2)
