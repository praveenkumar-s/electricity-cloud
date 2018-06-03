import time
import pigpio
import firebase_client
from datetime import datetime

timediff=datetime.now()
counter=0


# 1200 imp / hour 
# current wattage usage = 3600/ (time interval * 1200)
#call back function, that gets triggered every time there is a pulse
def cbf(gpio, level, tick):
    print("{:2d}->{} at {}".format(gpio, level, tick))
    global timediff
    delta=datetime.now() - timediff
    timediff= datetime.now()
    wattage = 3600/(delta.total_seconds * 1200)
    global counter
    if(counter>10):
        fbc= firebase_client.firebase_client()
        fbc.putvalue("realtime_data","x")
        print("Updated Realtime usage to Cloud")
        fbc=None
        counter=0
    counter= counter+1

GPIO=15
GLITCH=500
SLEEP=60

pi = pigpio.pi()

if not pi.connected:
   exit(0)

pi.set_mode(GPIO, pigpio.INPUT)

# Ignore edges shorter than GLITCH microseconds.
pi.set_glitch_filter(GPIO, GLITCH)

cb = pi.callback(GPIO, pigpio.FALLING_EDGE, cbf)

while True:
    pass