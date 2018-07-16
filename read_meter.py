import time
import pigpio
from datetime import datetime
import config
import subprocess
from datetime import datetime
import os
from Firebase_Client_Library import firebase_client
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import data_model
import json
try:
    import asyncio
except ImportError:
    import trollius as asyncio





timediff=datetime.now()
counter=0
IMP=0

# 1200 imp / hour 
# current wattage usage = 3600/ (time interval * 1200)
#call back function, that gets triggered every time there is a pulse
def cbf(gpio, level, tick):
    global IMP
    IMP=IMP+1
    print("{:2d}->{} at {}".format(gpio, level, tick))
    global timediff
    delta=datetime.now() - timediff
    timediff= datetime.now()
    wattage = 3600/(delta.total_seconds() * 1200)
    global counter
    if(counter>config.config['firebase_update_interval']):
        subprocess.Popen(["python","firebase_client.py","realtime_data",str(wattage)],stdin=None, stdout=None, stderr=None, close_fds=True)
        counter=0
    counter= counter+1

def blacklist(in_str,characters,safechar):
    for items in characters:
        in_str=in_str.replace(items,safechar)
    return in_str
    
    
    
    
def upload_imp():
    global IMP

    #try to get data for the existing month:
    month= datetime.now().month
    year=datetime.now().year
    fb=firebase_client()
    data=fb.getdata(str(year)+'_'+str(month))
    if(data is not None):
        data=json.loads(data)
        data_to_upload=data_model.data_fabricate(data,IMP)
    else:
        data_to_upload=data_model.new_data_fabricate(IMP)

    try:
        subprocess.Popen(["python","firebase_client.py",str(year)+'_'+str(month),json.dumps(data_to_upload)],stdin=None, stdout=None, stderr=None, close_fds=True)
        IMP=0
        print("Uploaded Ticks data to cloud @ {0}".format(str(datetime.now())))
    except Exception as e:
        print("Exception While uploading IMP")
        print(e.message())

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

scheduler = AsyncIOScheduler()
scheduler.add_job(upload_imp, 'interval', seconds=config.config['IMP_upload_interval'])
scheduler.start()
print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

# Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
try:
    asyncio.get_event_loop().run_forever()
except (KeyboardInterrupt, SystemExit):
    pass
