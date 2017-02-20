#importing packages to stream to plot.ly and work with surface Temp-sensors
#tutorial: https://plot.ly/raspberry-pi/tmp36-temperature-tutorial/
import plotly.plotly as py
import json
import time
import datetime
import os
import glob
import urllib2
import re

#reading file with user credentials and streaming tokens for plotly, repeat the login attemp until successfully completed
e=str("Error")
while e != ():
    try:
        with open('/your/script/directory/config.json') as config_file:
            plotly_user_config = json.load(config_file)
            py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])
    except Exception, e:
        print "Couldn't do it: %s" % e
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
        'name':'I_charge',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][7],
            'maxpoints': 1440
        }
    },
    {    
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'I_PV',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][8],
            'maxpoints': 1440
        }
    },
    {
        'x': [],
        'y': [],
        'type':'scatter',
        'name':'I_AC (@220V)',
        'stream': {
            'token': plotly_user_config["plotly_streaming_tokens"][9],
            'maxpoints': 1440
        }
    }], filename = 'current flows', fileopt = 'extend')
print "View streaming graph here: ", url

#initilaze and open 3 streams online
streamIbat = py.Stream(plotly_user_config['plotly_streaming_tokens'][7])
streamIpv = py.Stream(plotly_user_config['plotly_streaming_tokens'][8])
streamIac = py.Stream(plotly_user_config['plotly_streaming_tokens'][9])

#initial values to create minute averages of measurements
min1 = time.strftime('%M')
min2 = time.strftime('%M')

print('Press Ctrl-C to quit')

while True:

    #get the newest file in logging directory
    #the acutal measurement is done with a Steca Tarom 4545 which is connect via serial USB connection and logged with "cat"
    newestIfile = max(glob.iglob(os.path.join('/your/tarom/directory',
                                              '*.txt')),
                      key=os.path.getctime)

    #read the last line within the file and split the content at each ";"
    with open(newestIfile) as fI:
        lines = fI.readlines()
        last_row = lines[-2]
        last_row = last_row.split(';')

    #open the youless energy monitor (attached to electricity counter) within the local network,
    #read the content of the webpage, split the content each new line, each tab and each space and read the second last entry
    youless = 'http://192.168.0.14/V?h=1'
    response = urllib2.urlopen(youless)
    webcontent = response.read()
    webcontent = re.split('\n|  | ', webcontent)
    l = len(webcontent)
    P_ac = float(webcontent[l-2])

    #get the charging power of the charge controller and the used power from the PV field by multiplying current and voltage from the serial connected charge controller
    P_bat = float(last_row[8])*float(last_row[3])
    P_pv = float(last_row[9])*float(last_row[4])
    
    try:
        streamIbat.open()
        streamIpv.open()
        streamIac.open()
        streamIbat.write({'x': datetime.datetime.now(), 'y': P_bat})
        streamIpv.write({'x': datetime.datetime.now(), 'y': P_pv})
        streamIac.write({'x': datetime.datetime.now(), 'y': P_ac})
        streamIbat.close()
        streamIpv.close()
        streamIac.close()
    except Exception, e:
        print "Couldn't do it: %s" % e
        pass

    while min1 == min2:
        min2 = time.strftime('%M')
        time.sleep(5)

    #wait for 45 seconds after a minute has passed so that serial monitoring shell script has engough time to read the charge controller
    min1 = time.strftime('%M')
    min2 = time.strftime('%M')
    time.sleep(45)

    
