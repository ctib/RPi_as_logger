#importing packages to stream to plot.ly and work with surface Temp-sensors
#tutorial: https://plot.ly/raspberry-pi/tmp36-temperature-tutorial/
import plotly.plotly as py
import json
import time
import datetime
import Adafruit_TMP.TMP006 as TMP006

#create initial file, named by date, and write first line with header
date = time.strftime("%Y%m%d")
f = open('/your/logging/directory/'+ date +'-SurfTemp', 'a')
f.write('#; date; time; t_surf1; t_surf2; t_surf3\n')

#initializing temperature sensors
sensor1 = TMP006.TMP006(address=0x44)
sensor2 = TMP006.TMP006(address=0x40)
sensor3 = TMP006.TMP006(address=0x41)
sensor1.begin()
sensor2.begin()
sensor3.begin()
print('Sensors started')

#reading file with user credentials and streaming tokens for plotly
with open('/your/script/directory/config.json') as config_file:
    plotly_user_config = json.load(config_file)
    py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])
print('config file loaded')

#initialize plot online and get url. this contains 3 stream plots
url = py.plot([
    {    
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'surf_north',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][0],
            'maxpoints': 1440
        }
    },
    {
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'surf_up',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][1],
            'maxpoints': 1440
        }
    },
    {
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'surf_south',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][2],
            'maxpoints': 1440
        }
    }], filename = 'surface temperatures', fileopt = 'extend')
print "View streaming graph here: ", url

#initilaze and open 3 streams online
streamT1 = py.Stream(plotly_user_config['plotly_streaming_tokens'][0])
streamT2 = py.Stream(plotly_user_config['plotly_streaming_tokens'][1])
streamT3 = py.Stream(plotly_user_config['plotly_streaming_tokens'][2])

#initial values to create minute averages of measurements
min1 = time.strftime('%M')
min2 = time.strftime('%M')
n=0
sum_surf_temp1=0
sum_surf_temp2=0
sum_surf_temp3=0
n_avg = 0

print('Press Ctrl-C to quit')

# measurement process
while True:

    #open file and write number of measurement and time to file    
    date = time.strftime("%Y%m%d")
    f = open('/your/logging/directory/'+ date +'-SurfTemp', 'a')
    count = str(n)
    t = time.strftime('%H:%M')
    f.write(count+'; ' +time.strftime("%d")+'/'+time.strftime("%m")+'/'+time.strftime("%Y") + '; ' + t +'; ')

    #reading over 1 minute
    while min1 == min2:

        t = time.strftime('%H:%M')
        
        #actual reading of sensors
        current_surf_temp1 = sensor1.readObjTempC()
        current_surf_temp2 = sensor2.readObjTempC()
        current_surf_temp3 = sensor3.readObjTempC()

        #sum up readings
        sum_surf_temp1 = sum_surf_temp1 + current_surf_temp1
        sum_surf_temp2 = sum_surf_temp2 + current_surf_temp2
        sum_surf_temp3 = sum_surf_temp3 + current_surf_temp3
                     
        n_avg = n_avg + 1
        min2 = time.strftime('%M')
        time.sleep(1.0)

    #creating the average after a minute has passed                 
    surf_temp1 = sum_surf_temp1 / n_avg
    surf_temp2 = sum_surf_temp2 / n_avg
    surf_temp3 = sum_surf_temp3 / n_avg
    n=n+1

    #write minute average to the file
    f = open('/your/logging/directory/'+ date +'-SurfTemp', 'a')
    f.write('{0:0.2F}*C'.format(surf_temp1) + '; ')
    f.write('{0:0.2F}*C'.format(surf_temp2) + '; ')
    f.write('{0:0.2F}*C\n'.format(surf_temp3))
    
    #write average to plot.ly but pass if there is no internet connection
    try:
        streamT1.open()
        streamT2.open()
        streamT3.open()
        streamT1.write({'x': datetime.datetime.now(), 'y': surf_temp1})
        streamT2.write({'x': datetime.datetime.now(), 'y': surf_temp2})
        streamT3.write({'x': datetime.datetime.now(), 'y': surf_temp3})
        streamT1.close()
        streamT2.close()
        streamT3.close()
    except:
        print "cannot connect to plot.ly-stream"
        pass

    #reset values for average calculation
    sum_surf_temp1=0
    sum_surf_temp2=0
    sum_surf_temp3=0
    n_avg = 0
    min1 = time.strftime('%M')
    min2 = time.strftime('%M')
    f.close()
    
