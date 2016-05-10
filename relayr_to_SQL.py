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

# works most of the time but sometimes this gives error messages... still needs some fixing
while True:
    stuff = list()    
    c = Client(token='<insert your relayr token here>')
    dev = c.get_device(id='<insert your relayr device id here>')
    def mqtt_callback(topic, payload):
        payvar = '%s' % (payload)
        stuff.append(payvar)
    stream = MqttStream(mqtt_callback, [dev])
    stream.start()
    time.sleep(3)
    x = datetime.datetime.now()
    print x
    #there is an erro with the stuff[0] from time to time. I thought the line commented below helped but error still occures occasionally
    #if stuff[0] == None : break
    payvar = stuff[0]
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
