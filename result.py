from tinydb import TinyDB, Query


db = TinyDB('/home/pi/sams_system/testing.json')

data = Query()
testing = db.search(data.status == False)

print(testing)