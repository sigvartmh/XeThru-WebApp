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
    res = {"scan":[{"ssid":"test",
            "encryption" : 
            "WPA",
            "mac" :"f4:cf:e2:40:a3:30"},
            {"ssid":"test3","encryption" : "WPA","mac" :"f3:cf:e2:40:a3:30"}]}
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

@app.route('/wlan/api/connectivity',methods=['GET'])
def check_connectivity():
    return jsonify({'status' : ap.check_connectivity()})

if __name__ == '__main__':
    #Start flask server
    app.run(host="0.0.0.0",port=3000,debug=True)
