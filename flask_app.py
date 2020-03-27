from flask import Flask, render_template, redirect, request
import os
import subprocess
import socket
from datetime import datetime
from time import sleep



if os.name == 'nt':
    OS_NAME = 'WINDOWS'
else:
    OS_NAME = 'LINUX'

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    ssid_name = get_wifi_ssid()
    ip_addr = get_ip_address()
    server_time = datetime.now().strftime("%H:%M:%S")
    return render_template('app.html', ssid_name = ssid_name, ip_addr = ip_addr, server_time = server_time)

@app.route('/set_timezone')
def set_timezone():
    return render_template('set_timezone.html')

@app.route('/save_timezone', methods = ['GET', 'POST'])
def save_timezone():
    time_zone = request.form['timezone']
    print(time_zone)
    timeconfig = subprocess.Popen(['sudo', 'timedatectl', 'set-timezone', time_zone], stdout=subprocess.PIPE)
    timeconfig_out, err = timeconfig.communicate()
    print(timeconfig_out)
    print(err)
    sleep(2)
    return redirect('/')


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
