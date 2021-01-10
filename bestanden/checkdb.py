import sqlite3
import pytz

db = sqlite3.connect("rekeningen.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
for row in db.execute("SELECT * FROM historie"):
    utc_time = row[0]
    local_time = pytz.utc.localize(utc_time).astimezone()
    print("{} \t {} ".format(utc_time, (local_time)))

db.close()

