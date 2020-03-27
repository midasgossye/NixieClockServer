from flask import Flask, render_template, redirect, request, jsonify
import os
import subprocess
import socket
import time
from time import sleep
import configparser
import requests
import json


if os.name == 'nt':
    OS_NAME = 'WINDOWS'
else:
    OS_NAME = 'LINUX'

app = Flask(__name__)
app.debug = True

config = configparser.ConfigParser()

@app.route('/')
def hello_world():
    config.read('conf.ini')

    ssid_name = get_wifi_ssid()
    ip_addr = get_ip_address()
    server_time = time.strftime("%H:%M:%S %Z")

    server_timezone = get_server_timezone()

    openweather_enabled = config['Weather'].getboolean('OpenWeatherEnabled')
    openweather_city = config['Weather']['City']
    openweather_api_key = config['Weather']['ApiKey']

    if openweather_enabled:
        temp = get_local_temp(openweather_city, openweather_api_key)
    else:
        temp = 0
    
    return render_template('app.html', ssid_name = ssid_name, ip_addr = ip_addr, server_time = server_time, server_timezone = server_timezone, openweather_enabled = openweather_enabled, openweather_city = openweather_city, openweather_api_key=  openweather_api_key, temp = temp)

@app.route('/set_timezone')
def set_timezone():
    return render_template('set_timezone.html')

@app.route('/save_timezone', methods = ['GET', 'POST'])
def save_timezone():
    time_zone = request.form['timezone']
    set_system_timezone(time_zone)

    return redirect('/')

@app.route('/_change_api_key')
def change_api_key():
    api_key = request.args.get('api_key', type=str)
    print(api_key)
    openweather_city = config['Weather']['City']
    temp = get_local_temp(openweather_city, api_key)

    config['Weather']['ApiKey'] = api_key
    with open('conf.ini', 'w') as configfile:
        config.write(configfile)

    return jsonify(api_key=api_key, temp=temp)

@app.route('/_change_city')
def change_city():
    city_name = request.args.get('city_name', type=str)
    openweather_api_key = config['Weather']['ApiKey']
    config['Weather']['City'] = city_name
    with open('conf.ini', 'w') as configfile:
        config.write(configfile)
    temp = get_local_temp(city_name, openweather_api_key)
    return jsonify(temp=temp)


def get_local_temp(weather_location, weather_api_key):
    try:
        r = requests.get("http://api.openweathermap.org/data/2.5/weather", params = {'q' : weather_location, 'appid' : weather_api_key}, timeout=0.1)
        weather_data = json.loads(r.text)
        temp = int(round(weather_data[u'main'][u'temp'])-273.15)
    except:
        return -1000

    return temp

def get_server_timezone():
    if OS_NAME == 'LINUX':
        timedatectl = subprocess.Popen(['timedatectl'], stdout=subprocess.PIPE)
        timedatectl_out, err = timedatectl.communicate()
        raw_lines =  timedatectl_out.decode('utf-8').rsplit('\n')

        for line in raw_lines:
            if 'Time zone' in line:
                idx = line.find(':')
                server_timezone = line[idx+2:]
                break

        print(server_timezone)
    else:
        server_timezone = 'unavailable'

    return server_timezone

def set_system_timezone(time_zone):
    if OS_NAME == 'LINUX':
        timeconfig = subprocess.Popen(['sudo', 'timedatectl', 'set-timezone', time_zone], stdout=subprocess.PIPE)
        timeconfig_out, err = timeconfig.communicate()
        #print(timeconfig_out)
        #print(err)
        sleep(2)
        time.tzset()
        sleep(2)
    else:
        print("Function not available on " + OS_NAME)

def get_wifi_ssid():
    if OS_NAME == 'LINUX':
        iwconfig_raw = subprocess.Popen(['iwconfig'], stdout=subprocess.PIPE)
        ap_details, err = iwconfig_raw.communicate()
        raw_line =  ap_details.decode('utf-8').rsplit('\n')[0]
        ssid_name = raw_line[30:-3]
    elif OS_NAME == 'WINDOWS':
        win_network_raw = subprocess.Popen(['Netsh', 'WLAN', 'show', 'interfaces'], stdout=subprocess.PIPE)
        ap_details, err = win_network_raw.communicate()
        raw_lines =  ap_details.decode('utf-8').rsplit('\n')

        for line in raw_lines:
            if 'SSID' in line:
                idx = line.find(':')
                ssid_name = line[idx+2:-1]
                break

    else:
        ssid_name = 'not available...'
    
    return ssid_name

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_addr = s.getsockname()[0]
    except:
        print('no internet connection')
    s.close()

    return ip_addr

if __name__ == '__main__':
    app.run(host='0.0.0.0')
