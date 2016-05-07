import time
import datetime
import json
import sqlite3
from relayr import Client
from relayr.dataconnection import MqttStream

conn = sqlite3.connect('relayr_sensorsdb.sqlite3')
cur = conn.cursor()

#cur.execute('DROP TABLE IF EXISTS sensors')
cur.execute('CREATE TABLE IF NOT EXISTS sensors (x TEXT, door TEXT, hum TEXT, temp TEXT)')

while True:
    shit = list()    
    c = Client(token='<insert your relayr token here>')
    dev = c.get_device(id='<insert your relayr device id here>')
    def mqtt_callback(topic, payload):
        payvar = '%s' % (payload)
        shit.append(payvar)
    stream = MqttStream(mqtt_callback, [dev])
    stream.start()
    time.sleep(3)
    x = datetime.datetime.now()
    print x
    if shit[0] == None : break
    payvar = shit[0]
    try: js = json.loads(payvar)
    except: js = None
    door = js["readings"][0]["value"]
    hum = js["readings"][1]["value"]
    temp = js["readings"][2]["value"]
    stream.stop()
    cur.execute('INSERT INTO sensors(x, door, hum, temp) VALUES (?, ?, ?, ?)', (x, door, hum, temp))
    conn.commit()
    print 'Line added to database!'
    time.sleep(7)
