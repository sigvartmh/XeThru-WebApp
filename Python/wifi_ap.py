import time
from flask.ext.cors import CORS
from flask import Flask, jsonify, render_template, url_for, send_from_directory, request, abort
from flask.ext.cors import CORS
from RaspberryProvisioner import RaspberryProvisioner as RP
app = Flask(__name__)
CORS(app)
ap  = RP()

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

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

@app.route('/api/wlan/scan', methods=['GET'])
def list_wifi():
    res = ap.scan()
    return jsonify(res)

@app.route('/font/roboto/<path:filename>')
def send_font(filename):
    print send_from_directory('font/roboto/', filename)
    return send_from_directory('font/roboto/', filename)

@app.route('/api/wlan/connect', methods=['POST'])
def setup_wifi():
    if not request.json or not 'ssid' in request.json:
        abort(400)
    ap.connect_wifi(request.json)
    response = { 'status': "success"}
    return jsonify(response)

@app.route('/api/wlan/connectivity', methods=['GET'])
def check_connectivity():
    return jsonify({'status' : ap.check_connectivity()})

@app.route('/api/wlan/uploadspeed', methods=['POST'])
def check_uploadspeed():
    if not request.json or not 'size' in request.json:
        abort(400)
    ap.upload_speed
    return jsonify({'speed' : ap.upload_speed()})

def check_connection():
    wlan = ap.check_connection("wlan0")
    eth0 = ap.check_connection("eth0")
    connection = ap.check_connectivity()
    if((wlan or eth0) and connection):
        return True
    else:
        return False

if __name__ == '__main__':
    if(check_connection()):
        app.run(host="0.0.0.0",port=80,debug=False)
    else:
        #Sets up the necessary config files for access point mode
        ap.setup()
        #Sets the raspberry into Access point mode
        ap.enable()
        #Start flask server
        app.run(host="0.0.0.0",port=80,debug=False)
