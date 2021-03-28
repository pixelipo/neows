import urllib.request, urllib.parse, urllib.error
import ssl
import json

from app import db

def crawl (baseUrl, parms, total):
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print('Fetching ', str(parms['size']), 'items from page', str(parms['page']) + '/' + str(total))
    url = baseUrl + urllib.parse.urlencode(parms)
    # print(url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()

    # fetch remaining rate limit from response headers
    remaining = uh.info()['X-RateLimit-Remaining']
    print('Requests remaining:', remaining)
    if (int(remaining) == 0) : return 0

    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
        parms['page'] = str(int(parms['page']) + 1)
        total = int(js['page']['total_pages'])
    except err:
        return err

    # print(js['links'])
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
