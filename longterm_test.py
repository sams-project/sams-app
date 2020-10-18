from main.dataset import Dataset
from tinydb import TinyDB, Query
import time

dataset = Dataset()
db = TinyDB('/home/pi/sams_system/testing.json')

# data = Query()
# testing = db.search(data.status == False)


def testing():
    while True:
        test_data = dataset.get_microphone_data()
        db.insert(test_data)
        time.sleep(5)





