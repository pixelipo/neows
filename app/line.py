import sqlite3
import time

from app import db

def approach():
    conn = db.initDb('data/db.sqlite3')
    cur = conn.cursor()

    messages = dict()
    encounters = list()

    for message_row in db.getApproaches(cur) :
        # Convert epoch to year
        year = time.strftime('%Y', time.localtime(message_row[1]/1000))

        ## TODO: parametrize range
        if int(year) in range(2000, 2050):
            encounters.append((message_row[0], year, message_row[2]))

    return encounters

def jsonify(encounters):
    objects = set()
    years = set()
    approaches = dict()

    fhand = open('data/encounters.js','w')
    fhand.write("encounters = [\n\t['Year'")

    encounters.sort()
    for encounter in encounters:
        # pre = len(objects)
        objects.add(encounter[0])
        years.add(encounter[1])
        approaches.update()
        # post = len(objects)
        # if pre != post:
            # fhand.write(",'"+encounter[0]+"'")

    for object in sorted(objects):
        fhand.write(",'"+object+"'")

    fhand.write("]")
    # print(encounters)

    for year in sorted(years):
        fhand.write(",\n\t['"+year+"'")
        year_list = list()
        for object in sorted(objects):
            found = [encounter for encounter in encounters if encounter[1] == year and encounter[0] == object]
            dist = 0
            if (len(found) == 1):
                dist = int(found[0][2])
            elif len(found) > 1:
                for foun in found:
                    if dist < int(foun[2]):
                        dist = int(foun[2])
            dist = dist / 384402
            if (dist < 20):
                fhand.write(","+str(dist))
            else:
                fhand.write(",0")
                # print(found[i][2] for i in len(found))
            # fhand.write(","+str(val))
        # print(encounters)
        # for object in sorted(objects):
        #     if year in encounters[object]
        #     encounter[2]



        # for encounter in encounters:
        #     key = (year, encounter)
        #     val = encounter.get(, 0)
        #     fhand.write(","+str(val))
        fhand.write("]");

    fhand.write("\n];\n")
    fhand.close()
    #
    # print("Output written to encounters.js")
    # print("Open index.html to visualize the data")

    return True
