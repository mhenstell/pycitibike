from pycitibike import Citibike
import time
import sqlite3
import sys

con = None
client = Citibike()

stations = {}
oldStations = {}

lastTime = 0

# class Station:
	
# 	num   = 0
# 	bikes = 0
# 	docks = 0

# 	def __init__(self, number):
# 		self.num = number
	
# 	def update(self, bikes, docks):
# 		self.bikes = bikes
# 		self.docks = docks

# 	def check(self, bikes, docks):
# 		if bikes != self.bikes or docks != self.docks:
# 			print "\tStation %s changed: Bikes: %s to %s, Docks: %s to %s" % (self.num, self.bikes, bikes, self.docks, docks)
# 			self.update(bikes, docks)


try:
	con = sqlite3.connect('test.db')

	cur = con.cursor()
	cur.execute('SELECT SQLITE_VERSION()')
	data = cur.fetchone()
	print "SQLite version: %s" % data
except sqlite3.Error, e:
	print "Error %s" % e.args[0]
	sys.exit(1)


stations = client.stations()

for station in stations:
	sid = station['id']
	status = station['status']
	istatus = 0
	if status == "Active": istatus = 1
	sql = "insert into knownStations(id, status) values (%i, %i)" % (sid, istatus)
	cur.execute(sql)
con.commit()

# while True:

# 	timestamp = int(time.time())
# 	print "Updating %s" % timestamp

# 	stations = client.stations()

# 	for station in stations:
# 		sid = station['id']
# 		if sid not in oldStations:
# 			pass
# 		elif station['availableDocks'] != oldStations[sid]['availableDocks'] or station['availableBikes'] != oldStations[sid]['availableBikes']:
			
# 			sql = "insert into stationlog(id, timestamp, availableBikes, availableDocks) values (%i, %i, %i, %i)" % (sid, timestamp, station['availableBikes'], station['availableDocks'])
# 			print sql
# 			cur.execute(sql)

# 		oldStations[sid] = station

# 		# print station, oldStations[sid]

# 	con.commit()

# 	time.sleep(5)
