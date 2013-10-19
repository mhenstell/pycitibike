import sqlite3
from pycitibike import Citibike
import sys
import datetime

try:
	con = sqlite3.connect('test.db')

	cur = con.cursor()
	cur.execute('SELECT SQLITE_VERSION()')
	data = cur.fetchone()
	print "SQLite version: %s" % data
except sqlite3.Error, e:
	print "Error %s" % e.args[0]
	sys.exit(1)


# client = Citibike()
# stations = client.fullStations()

# for station in stations:

# 	sid = int(station['id'])
# 	lat = float(station['latitude'])
# 	longg = float(station['longitude'])
# 	label = station['label']
# 	sstatus = station['status']
# 	if sstatus == "Active": status = 1
# 	else: status = 0

# 	sql = "insert into stations(id, lat, long, label, status) values(%i, %f, %f, '%s', %i)" % (sid, lat, longg, label, status)
# 	cur.execute(sql)
# con.commit()

sid = int(sys.argv[1])

sql = "select * from stationlog where id = %i order by timestamp asc" % sid
cur.execute(sql)
data = cur.fetchall()

for point in data:
	timestamp = point[1]
	timestamp = datetime.datetime.fromtimestamp(timestamp)
	bikes = point[2]
	docks = point[3]

	print timestamp, bikes, docks