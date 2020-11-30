# Add python modules
import Adafruit_DHT
import time
import psycopg2
import pytz

# Pull from python modules
from datetime import date
from datetime import datetime
from pytz import timezone
from psycopg2.extras import RealDictCursor

def timescaleconnect():
    global conn, cur
    conn = None
    try:
        conn = psycopg2.connect(dbname='temprature', user='***UserName***', password='********', host='timescaleIPaddress', port='5432')
    except:
        print: "I am unable to connect to the database"
    cur = conn.cursor()

def maketable():
	global conn, cur
# just run this manually to create the table once
	cur.execute("CREATE TABLE temphumid (time TIMESTAMPTZ NOT NULL, temprature DOUBLE PRECISION NULL, humidity DOUBLE PRECISION NULL);")
	conn.commit()
	cur.close()
	conn = None

# adjust the following for your timezone
def currentdatetimect():
    global mnow
    fmtwtime = "%Y-%m-%d %H:%M:%S.%f"
    fmt = "%Y-%m-%d"
    now_utc = datetime.now(timezone('UTC'))
    now_central = now_utc.astimezone(timezone('UTC'))
    now_chicago = now_central.astimezone(timezone('UTC'))
    today = (now_chicago.strftime(fmt))
    mnow = (now_chicago.strftime(fmtwtime))

def collecttemphumid():
	global chumidity, ctemprature
	DHT_SENSOR = Adafruit_DHT.DHT22
	DHT_PIN = 4
	chumidity, ctempraturecelcius = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
	ctemprature = (ctempraturecelcius * 1.8) + 32

def committodb():
    cur.execute("""
        INSERT INTO temphumid(time, temprature, humidity) 
        VALUES(%s, %s, %s);
        """, 
        (mnow, ctemprature, chumidity))
    conn.commit()
    cur.close()

timescaleconnect()
currentdatetimect()
collecttemphumid()
committodb()

# The maketable should only be run once.
# maketable()
