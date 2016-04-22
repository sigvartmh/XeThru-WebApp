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
    ap.connect_wifi(request.json)
    response = { 'status': "sucess"}
    return jsonify(response)

def check_connectivity(): #If this false restart AP
    return True

if __name__ == '__main__':
    #Sets up the necessary config files for access point moode
    ap.setup()
    #Sets the raspberry into Access point mode
    ap.enable()
    #Start flask server
    app.run(host="0.0.0.0",port=80,debug=True)

  #gawk -F: '{ print $1 }' /etc/passwd

  #"iw dev wlan0 scan | gawk -f wifi_scan.awk"
