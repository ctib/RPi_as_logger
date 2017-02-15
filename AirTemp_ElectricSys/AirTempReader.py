#importing packages to stream to plot.ly and work with surface Temp-sensors
#tutorial: https://plot.ly/raspberry-pi/tmp36-temperature-tutorial/
import plotly.plotly as py
import json
import time
import datetime
import os
import glob

#try to log in to plot.ly until there is an internet connection
e=str("Error")
while e != ():
    try:
        with open('/your/config/folder/here/config.json') as config_file:
            plotly_user_config = json.load(config_file)
            py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])
    except Exception, e:
##        print "Couldn't do it: %s" % e
        time.sleep(5)
        continue
    else:
        e = ()

#initialize plot online and get url. this contains 3 stream plots
url = py.plot([
    {    
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'T_1',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][0],
            'maxpoints': 1440
        }
    },
    {
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'T_2',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][1],
            'maxpoints': 1440
        }
    },
    {    
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'T_3',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][2],
            'maxpoints': 1440
        }
    },
    {
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'T_4',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][3],
            'maxpoints': 1440
        }
    },
    {    
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'T_5',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][4],
            'maxpoints': 1440
        }
    },
    {
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'T_6',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][5],
            'maxpoints': 1440
        }
    },
    {
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'T_7',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][6],
            'maxpoints': 1440
        }
    }], filename = 'air temperatures', fileopt = 'extend')
print "View streaming graph here: ", url

#initilaze and open 3 streams online
streamT1 = py.Stream(plotly_user_config['plotly_streaming_tokens'][0])
streamT2 = py.Stream(plotly_user_config['plotly_streaming_tokens'][1])
streamT3 = py.Stream(plotly_user_config['plotly_streaming_tokens'][2])
streamT4 = py.Stream(plotly_user_config['plotly_streaming_tokens'][3])
streamT5 = py.Stream(plotly_user_config['plotly_streaming_tokens'][4])
streamT6 = py.Stream(plotly_user_config['plotly_streaming_tokens'][5])
streamT7 = py.Stream(plotly_user_config['plotly_streaming_tokens'][6])

#initial values to create minute averages of measurements
min1 = time.strftime('%M')
min2 = time.strftime('%M')

print('Press Ctrl-C to quit')

while True:

    newestTfile = max(glob.iglob(os.path.join('/your/log/folder/here/Arduino',
                                              '*.txt')),
                      key=os.path.getctime)

    with open(newestTfile) as fT:
        lines = fT.readlines()
        last_row = lines[-1]
        last_row = last_row.split('; ')
##        print last_row

    try:
        streamT1.open()
        streamT2.open()
        streamT3.open()
        streamT4.open()
        streamT5.open()
        streamT6.open()
        streamT7.open()
        streamT1.write({'x': datetime.datetime.now(), 'y': float(last_row[3])})
        streamT2.write({'x': datetime.datetime.now(), 'y': float(last_row[4])})
        streamT3.write({'x': datetime.datetime.now(), 'y': float(last_row[5])})
        streamT4.write({'x': datetime.datetime.now(), 'y': float(last_row[6])})
        streamT5.write({'x': datetime.datetime.now(), 'y': float(last_row[7])})
        streamT6.write({'x': datetime.datetime.now(), 'y': float(last_row[8])})
        streamT7.write({'x': datetime.datetime.now(), 'y': float(last_row[9])})
        streamT1.close()
        streamT2.close()
        streamT3.close()
        streamT4.close()
        streamT5.close()
        streamT6.close()
        streamT7.close()
    except Exception, e:
        print "Couldn't do it: %s" % e
        pass

    

    while min1 == min2:
        min2 = time.strftime('%M')
        time.sleep(5)

    min1 = time.strftime('%M')
    min2 = time.strftime('%M')
    time.sleep(45)