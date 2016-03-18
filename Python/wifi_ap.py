import subprocess, json, os, jinja2
from flask import Flask, jsonify, render_template, url_for, send_from_directory
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
    #url_for('static', filename='font/Roboto-Regular.woff2')
    #url_for('static', filename='Roboto-Regular.woff')
    #url_for('static', filename='Roboto-Regular.ttf')
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
    out = subprocess.check_output(["bash", "genwifi.sh"])
    escapes = ''.join([chr(char) for char in range(1, 32)])
    s = out.translate(None,escapes)
    jlist = [p+"}" for p in s.split("}") if p != ""]
    output = '{ "scan": ['
    for jsonobj in jlist:
        output+=jsonobj
        output+=","
    created_json = output[:-1]+']}'
    print created_json
    jsondict = json.loads(created_json)
    #subprocess.check_output("iw dev wlan 0 scan | gawk -f wifi_scan.awk")
    #return jsonify({'scan':[ out ]})
    return jsonify(jsondict)
    #return jsonify({'scan': sresult})

@app.route('/font/roboto/<path:filename>')
def send_font(filename):
    print send_from_directory('font/roboto/', filename)
    return send_from_directory('font/roboto/', filename)
@app.route('/font/<path:path>')
def send_test(path):
    return "test:" + path

@app.route('/wlan/api/connect', methods=['POST'])
def setup_wifi(ssid, password):
	#replace ssid and pwd in template
	return True


loader = jinja2.FileSystemLoader( os.path.dirname(__file__))
env = jinja2.Environment( loader=loader )
def write_config(var, path, output):
	template = env.get_template(path)
	try:
		temp = template.render(var)
	except:
		print "Wrong in template"
		raise

	with open(output, "w") as conf:
		conf.write(temp)

def check_connection():
    return True

def setup_ap(config):
    #Define ap interface setup for wlan with static ip and netmask
    path = "linux_config/etc/network/interfaces.ap.template"
    output = "etc/network/interfaces"
    ifsetup = { "ap":{
                "interface": config['interface'],
                "ip" : config['ip'],
                "netmask": config['netmask']
                }
            }
    write_config(ifsetup, path, output)

    #Define hostapd setup with template
    path = "linux_config/etc/hostapd/hostapd.conf.template"
    output = "etc/hostapd/hostapd.conf"
    #driver = check_driver() check if you can use the default driver
    hostapd_setup = { "hostapd" : {
                        "interface" : config['interface'],
                        "ssid" : config['ssid'],
                        "password": config['pwd'],
                        "driver": config['driver']
                        }
                    }
    write_config(hostapd_setup, path, output)


    #Define DHCP conf
    path = "linux_config/etc/dhcp/dhcpd.conf.template"
    output = "etc/dhcp/dhcpd.conf"
    dhcpap_setup = { "dhcp": {
                        "ap": True,
                        "subnet" : {
                            "ip" : config['subnet']['ip'],
                            "range":{
                                "start": config['subnet']['range']['start'],
                                "end"  : config['subnet']['range']['end']
                            },
                            "baddr": config['subnet']['baddr']
                        },
                        "ip": config['ip'],
                        "netmask": config['netmask'],
                        "domain": config['domain']
                      }
                    }
    write_config(dhcpap_setup, path, output)

    #Define DHCP isc server config
    path = "linux_config/etc/default/isc-dhcp-server.template"
    output = "etc/default/isc-dhcp-server"
    iscdhcp_setup = { "isc":{
                        "interface":config['interface']
                        }
                    }
    write_config(iscdhcp_setup, path, output)
    start_ap(config)
    return True

def reset_interfaces(config):
    out = subprocess.check_output(["sudo","ls", "-l"])
    print out
    #out = subprocess.check_output(["sudo", "ifdown", config['interface']])
    #out = subprocess.check_output(["sudo", "ifup", config['interface']])

def start_ap(config):
    reset_interfaces(config)
    #out = subprocess.check_output(["service", "isc-dhcp-server", "restart"])
    #out = subprocess.check_output(["service", "hostapd", "restart"])

'''
def setup_wifi():
'''

if __name__ == '__main__':
    f = open("config.json","r")
    jsondata = f.read()
    f.close()
    config = json.loads(jsondata)['config']
    print config['interface']
    #check_connectivity() if no run setup_ap
    setup_ap(config)
    app.run(debug=True)

  #gawk -F: '{ print $1 }' /etc/passwd

  #"iw dev wlan0 scan | gawk -f wifi_scan.awk"
