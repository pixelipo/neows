import sqlite3
import time

from app import db


def approach(years):
    conn = db.initDb('data/db.sqlite3')
    cur = conn.cursor()

    messages = dict()
    encounters = list()

    for message_row in db.getApproaches(cur) :
        # Convert epoch to year
        year = time.strftime('%Y', time.localtime(message_row[1]/1000))

        if int(year) in range(int(years[0]), int(years[1])):
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
        objects.add(encounter[0])
        years.add(encounter[1])
        approaches.update()

    for object in sorted(objects):
        fhand.write(",'"+object+"'")

    fhand.write("]")

    for year in sorted(years):
        fhand.write(",\n\t['"+year+"'")
        year_list = list()
        for object in sorted(objects):
            found = [encounter for encounter in encounters if encounter[1] == year and encounter[0] == object]
            dist = -1
            for foun in found:
                if dist < int(foun[2]):
                    dist = int(foun[2])
            dist = dist / 384402 # distance measured in Lunar distances
            if (dist > 100):
                dist = -1
            fhand.write(","+str(dist))

        fhand.write("]");

    fhand.write("\n];\n")
    fhand.close()

    return True
