from flask import Flask, render_template
import os
import subprocess
import socket
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    ssid_name = get_wifi_ssid()
    ip_addr = get_ip_address()
    server_time = datetime.now().strftime("%H:%M:%S")
    return render_template('app.html', ssid_name = ssid_name, ip_addr = ip_addr, server_time = server_time)

def get_wifi_ssid():
    iwconfig_raw = subprocess.Popen(['iwconfig'], stdout=subprocess.PIPE)
    ap_details, err = iwconfig_raw.communicate()
    raw_line =  ap_details.decode('utf-8').rsplit('\n')[0]
    ssid_name = raw_line[30:-3]
    
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
