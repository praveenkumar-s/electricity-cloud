import json
from datetime import datetime
cloud_data={
    'year':None,
    'month':None,
    'tags':[],
    'consumption':[
        {
            'date_time':{'day':None,'month':None,'hour':None,'minutes':None,'seconds':None},
            'units':None

        }
    ]
}


def data_fabricate(existing_data,ticks):
    now=datetime.now()
    data={'date_time':{'day':now.day,'month':now.month,'hour':now.hour,'minutes':now.minute,'seconds':now.second},
    'units':ticks/1200}
    existing_data['consumption'].append(data)
    return existing_data

def new_data_fabricate(ticks):
    cloud_data={
    'year':datetime.now().year,
    'month':datetime.now().month,
    'tags':[],
    'consumption':[]
}

    now=datetime.now()
    data={'date_time':{'day':now.day,'month':now.month,'hour':now.hour,'minutes':now.minute,'seconds':now.second},
    'units':ticks/1200}
    cloud_data['consumption'].append(data)
    return cloud_data