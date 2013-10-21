from flask import Flask, g
import sqlite3
import sys
import json
import time

app = Flask(__name__)

# DATABASE = "sampleData.db"
DATABASE = "../cbData.db"
PORT = 8080
# PORT = 80

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_to_database():
	return sqlite3.connect(DATABASE)

def get_db():
	db = getattr(g, "_database", None)
	if db is None:
		db = g._database = connect_to_database()
	db.row_factory = dict_factory
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

def getKnownStations():
	sql = "select id from stations"
	result = query_db(sql)

	knownStations = getattr(g, "_knownStations", None)
	if knownStations is None:
		knownStations = g._knownStations = []

		for entry in result:
			sid = int(entry['id'])
			knownStations.append(sid)
	return knownStations


@app.route("/v0/timeline/<station>")
def getTimeline(station):
	
	try: station = int(station)
	except: return "Station ID is invalid."

	if station not in getKnownStations():
		return "Station ID is invalid."

	outDict = {}

	sql = "select timestamp, availableBikes, availableDocks from stationlog where id = ? order by timestamp asc"
	try:
		result = query_db(sql, (str(station), ))
	except sqlite3.OperationalError, e:
		print "SQLite3 OperationalError:", e
		return "Error querying the database :("

	jout = json.dumps(result)
	return jout

@app.route("/v0/lastrun")
def getLastRun():

	sql = "select distinct timestamp from stationlog order by timestamp desc limit 1"
	
	try:
		result = query_db(sql)[0]['timestamp']
	except Exception, e:
		print "Exception: %s" % e
		return "Error"

	timestamp = int(result)
	delta = int(time.time() - timestamp)
	return "Last ran %s seconds ago" % delta

if __name__ == "__main__":


	app.debug = True
	app.run(host='0.0.0.0', port=PORT)
