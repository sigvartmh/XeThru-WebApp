import subprocess
from flask import Flask, jsonify, render_template, url_for
app = Flask(__name__)

sresult = [
{ 'ssid': "Xethru Test",
  'mac': "00:00:00:f0",
  'strenght' : 2,
  'security': True
  },
  { 'ssid': "Xethru Test2",
  'mac': "00:00:00:f1",
  'strenght' : 2,
  'security': False
  },
  { 'ssid': "Xethru Test3",
  'mac': "00:00:00:f2",
  'strenght' : 2,
  'security': True
  }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wlan/api/scan', methods=['GET'])
def list_wifi():
	#subprocess.check_output("iw dev wlan 0 scan | gawk -f wifi_scan.awk")
	return jsonify({'scan': sresult})

@app.route('/wlan/api/connect', methods=['POST'])
def setup_wifi(ssid, password):
	#replace ssid and pwd in template
	return True

def setup_ap():
	return True

if __name__ == '__main__':
	setup_ap()
	app.run(debug=True)
	url_for('static', filename='style.css')
	url_for('static', filename='materialize.min.css')
	url_for('static', filename='jquery.min.js')
	url_for('static', filename='materialize.min.js')

  #gawk -F: '{ print $1 }' /etc/passwd

  #"iw dev wlan0 scan | gawk -f wifi_scan.awk"
