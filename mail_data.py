import datetime
import os
from SQLiteWrapper import DBW
DBPath = "/mnt/NAS_QData/Stas/omnik.sqlite"

DBU = DBW(DBPath)
today = str(datetime.date.today())
cur = DBU.get_dict_cursor()
row = cur.execute("""SELECT * FROM minutes WHERE stamp LIKE ? ORDER BY id DESC;""", (today+"%",)).fetchone()
#print "=== Data from tuxhome solar ==="
#print "date/time", row['stamp'].split('.')[0]
#print "Total today:", row['EToday'], "KW"
#print "Total:", row['ETotal'], "KW"
#print "=== Peak today ==="
row1 = cur.execute("""SELECT * FROM minutes WHERE stamp LIKE ? ORDER BY PAC1 DESC;""", (today+"%",)).fetchone()
#print "date/time", row1['stamp'].split('.')[0]
#print "Peak output", row1['PAC1'], "KW"

mesg = """To: foo@bar.org
From: pi@rspi.org
Subject: Solar data

=== Data from tuxhome solar ===
date/time: %s
Total today: %s KW
Total: %s W

=== Peak today ===
date/time: %s
Peak output: %s W

""" % (row['stamp'].split('.')[0], row['EToday'], row['ETotal'], row1['stamp'].split('.')[0], row1['PAC1'])

print mesg
