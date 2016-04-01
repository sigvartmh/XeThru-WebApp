import subprocess, json, os, jinja2
from flask import Flask, jsonify, render_template, url_for, send_from_directory, request, abort
from RaspberryProvisioner import RaspberryProvisioner as RP
app = Flask(__name__)
ap  = RP()


@app.route('/')
def index():
    url_for('static', filename='style.css')
    url_for('static', filename='icons.css')
    url_for('static', filename='materialize.min.css')
    url_for('static', filename='jquery.min.js')
    url_for('static', filename='materialize.min.js')
    url_for('static', filename='angular.min.js')
    url_for('static', filename='angular.map.js')
    url_for('static', filename='app.js')
    return render_template('index.html')

@app.route('/wlan/api/scan', methods=['GET'])
def list_wifi():
    res = ap.scan()
    return jsonify(res)
    #return jsonify({'scan': sresult})

@app.route('/font/roboto/<path:filename>')
def send_font(filename):
    print send_from_directory('font/roboto/', filename)
    return send_from_directory('font/roboto/', filename)

@app.route('/font/<path:path>')
def send_test(path):
    return "test:" + path

@app.route('/wlan/api/connect', methods=['POST'])
def setup_wifi():
    print request.json
    if not request.json or not 'ssid' in request.json:
        abort(400)
    print request.json
    #replace ssid and pwd in template
    ap.enable_wifi(request.json)
    response = { 'status': "sucess"}
    return jsonify(response)

def check_connection():
    return True

def enable_wifi(wlan):
    print "wlan loaded into json"
    print wlan
    print ap.config['interface']
    
    print "Stopping dhcp server"
    out = subprocess.check_output(["sudo", "service", "isc-dhcp-server", "stop"])
    print "Stopping hostapd"
    out = subprocess.check_output(["sudo", "service", "hostapd", "stop"])
    reset_interaces(config)
    return True

def setup_ap(config):
    reset_interfaces(config)
    start_ap(config)
    return True

def reset_interfaces(config):
    print "Restarting interface " + str(config['interface'])
    #out = subprocess.check_output(["sudo","ls", "-l"])
    out = subprocess.check_output(["sudo", "ifdown", config['interface']])
    out = subprocess.check_output(["sudo", "ifup", config['interface']])

def start_ap(config):
    #reset_interfaces(config)
    out = subprocess.check_output(["sudo", "service", "isc-dhcp-server", "restart"])
    print out
    #out = subprocess.check_output(["sudo", "service", "hostapd", "restart"])
    #out = subprocess.check_output(["sudo", "service", "hostapd", "restart"])
    #out = subprocess.call(["sudo", "/usr/sbin/hostapd", "/etc/hostapd/hostapd.conf"])
    arg = ["sudo", "/usr/sbin/hostapd", "/etc/hostapd/hostapd.conf"]
    p = subprocess.Popen(arg)
    print out

if __name__ == '__main__':
    #Sets up the necessary config files for access point moode
    ap.setup()
    #Sets the raspberry into Access point mode
    ap.enable()
    #Start flask server
    app.run(host="0.0.0.0",port=80,debug=False)

  #gawk -F: '{ print $1 }' /etc/passwd

  #"iw dev wlan0 scan | gawk -f wifi_scan.awk"
