import sqlite3
import datetime
import Adafruit_DHT
import time

conn = sqlite3.connect('sensordb.sqlite3')
cur = conn.cursor()

#cur.execute('DROP TABLE IF EXISTS dht')
cur.execute('CREATE TABLE IF NOT EXISTS dht (x TEXT, temp TEXT, hum TEXT)')

while True:
    humidity, temperature = Adafruit_DHT.read_retry(22, 4)

    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
    temp = float(format(temperature, '.1f'))
    hum = float(format(humidity, '.1f'))
    x = datetime.datetime.now()
    print x, 'It is',temp, 'degrees and', hum,'%' 'humid'
    cur.execute('INSERT INTO dht (x, temp, hum) VALUES (?, ?, ?)', (x, temp, hum))
    conn.commit()
    time.sleep(5)
