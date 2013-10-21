from pycitibike import Citibike
import time
import sqlite3
import sys

con = None
client = Citibike()

stations = {}

DATABASE = "../cbData.db"
# DATABASE = "sampleData.db"

try:
	con = sqlite3.connect(DATABASE)

	cur = con.cursor()
	cur.execute('SELECT count(*) from stations')
	data = cur.fetchone()
	print "Number of stations: %s" % data
except sqlite3.Error, e:
	print "SQLite Error %s" % e.args[0]
	sys.exit(1)


# stations = client.stations()

# for station in stations:
# 	sid = station['id']
# 	status = station['status']
# 	istatus = 0
# 	if status == "Active": istatus = 1
# 	sql = "insert into knownStations(id, status) values (%i, %i)" % (sid, istatus)
# 	cur.execute(sql)
# con.commit()


timestamp = int(time.time())
print "Updating %s" % timestamp

stations = client.stations()

for station in stations:
	sid = station['id']

	sql = "select availableBikes, availableDocks from stationlog where id = ? order by timestamp desc limit 1"

	# if sid not in oldStations:
	# 	pass
	# elif station['availableDocks'] != oldStations[sid]['availableDocks'] or station['availableBikes'] != oldStations[sid]['availableBikes']:
	
	cur.execute(sql, (sid,))
	result = cur.fetchone()
	
	try:
		if int(result[0]) != station['availableBikes'] or int(result[1]) != station['availableDocks']:
			sql = "insert into stationlog(id, timestamp, availableBikes, availableDocks) values (%i, %i, %i, %i)" % (sid, timestamp, station['availableBikes'], station['availableDocks'])
			# print sid, "old: ", result[0], " new: ", station['availableBikes']
			cur.execute(sql)
			print "\tUpdated station %s" % sid
	except:
		pass

con.commit()
con.close()
