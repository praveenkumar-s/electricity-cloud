import json
from datetime import datetime
cloud_data={
    'year':None,
    'month':None,
    'tags':[],
    'consumption':[
        {
            'date_time':None,
            'units':None

        }
    ]
}


def data_fabricate(ticks):
    now=datetime.now()
    data={'date_time':now,
    'units':ticks/1200}
    cloud_data['consumption'].append(data)
    return cloud_data