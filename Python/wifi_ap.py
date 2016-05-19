import time
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

@app.route('/wlan/api/scan', methods=['GET'])
def list_wifi():
    res = ap.scan()
    return jsonify(res)

@app.route('/font/roboto/<path:filename>')
def send_font(filename):
    print send_from_directory('font/roboto/', filename)
    return send_from_directory('font/roboto/', filename)

@app.route('/font/<path:path>')
def send_test(path):
    return "test:" + path

@app.route('/wlan/api/connect', methods=['POST'])
def setup_wifi():
    if not request.json or not 'ssid' in request.json:
        abort(400)
    ap.connect_wifi(request.json)
    response = { 'status': "sucess"}
    return jsonify(response)

@app.route('/wlan/api/connectivity', methods=['GET'])
def check_connectivity():
    return jsonify({'status' : ap.check_connectivity()})

if __name__ == '__main__':
    #FIXME: This check should also be running while flask server is running.
    if(ap.check_connection("wlan0")): #TODO: could add  or (ap.check_connection("eth0") && ap.check_connectivity())
        app.run(host="0.0.0.0",port=80,debug=True)
   
    #Sets up the necessary config files for access point mode
    ap.setup()
    #Sets the raspberry into Access point mode
    ap.enable()
    #Start flask server
    app.run(host="0.0.0.0",port=80,debug=True)
