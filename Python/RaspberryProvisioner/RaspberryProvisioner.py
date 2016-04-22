import subprocess, json, os, jinja2, time, urllib2
import netifaces as ni

class RaspberryProvisioner:
    
    def __init__(self):
        loader = jinja2.FileSystemLoader( os.path.dirname(__file__))
        self.env = jinja2.Environment( loader=loader )
        f = open("config.json","r")
        self.config = json.loads(f.read())['config']
        f.close()

    def scan(self):
        out = subprocess.check_output(["sudo","bash", "genwifirbpi.sh"])
        escapes = ''.join([chr(char) for char in range(1, 32)])
        s = out.translate(None,escapes)
        jlist = [p+"}" for p in s.split("}") if p != ""]
        output = '{ "scan": ['
        for jsonobj in jlist:
            try:
                json.loads(jsonobj)
                output+=jsonobj
                output+=","
            except ValueError:
                print "Weird ssid name"
        created_json = output[:-1]+']}'
        jsondict = json.loads(created_json)
        return jsondict

    def dhcp_service(self, command):
        out = subprocess.call(["sudo", "service", "isc-dhcp-server", command])
        print "DHCP server " + command
    
    def hostapd_service(self, command):
        out = subprocess.call(["sudo", "service", "hostapd", command])
        print "hostapd " + command
    
    def connect_wifi(self,info):
        path = "linux_config/etc/network/interfaces.wifi.template"
        output = "/etc/network/interfaces"
        self.write_config(info,path,output)
        self.teardown()
   
        print "Resetting interfaces from connection"
        self.reset_interfaces()
        self.check_wifi()
        pass
    
    def enable(self):
        self.dhcp_service("start")
        self.hostapd_service("start")


    def setup(self):
        #stop services
        self.dhcp_service("stop")
        self.hostapd_service("stop")
        
        #Interface setup
        #Setting up interface to be hotspot
        path = "linux_config/etc/network/interfaces.ap.template"
        output = "/etc/network/interfaces"
        self.write_config(self.config, path, output)
        
        #Hostapd setup
        #driver = check_driver() check if you can use the default driver
        path = "linux_config/etc/hostapd/hostapd.conf.template"
        output = "/etc/hostapd/hostapd.conf"
        self.write_config(self.config, path, output)

        #Setting up default hostapd source file to hostapd.conf
        path = "linux_config/etc/default/hostapd.template"
        output = "/etc/default/hostapd"
        self.write_config(self.config, path, output)

        #Define DHCP conf
        path = "linux_config/etc/dhcp/dhcpd.conf.template"
        output = "/etc/dhcp/dhcpd.conf"
        self.config["enable_ap"] = True
        self.write_config(self.config, path, output)

        #Define DHCP isc-server config
        path = "linux_config/etc/default/isc-dhcp-server.template"
        output = "/etc/default/isc-dhcp-server"
        self.write_config(self.config, path, output)

        #Define DNS config
        #Load config 
        self.reset_interfaces()

    def teardown(self):
        path = "linux_config/etc/dhcp/dhcpd.conf.template"
        output = "/etc/dhcp/dhcpd.conf"
        
        self.config["enable_ap"] = False
        self.write_config(self.config, path, output)

        self.dhcp_service("stop")
        self.hostapd_service("stop")
        
        pass

    def reset_interfaces(self):
        print "Restarting interface " + str(self.config['interface'])
        
        out = subprocess.call(["sudo", "ifdown", self.config['interface']])
        time.sleep(1)
        out = subprocess.call(["sudo", "ifup", self.config['interface']])

        pass

    def write_config(self,var, path, output):
        template = self.env.get_template(path)
        try:
            temp = template.render(var)
        except:
            print "Wrong in template"
            raise
        with open(output, "w") as conf:
            conf.write(temp)
    
    def check_connection(self):
        subprocess.call(["ping", "-i", self.config['interface'], self.config['server']])

    def check_wifi(self):
        out = ni.ifaddresses('wlan0')
        print out
        
        try:
           ip = out[2][0]['addr']
        except:
	   self.setup()
	   self.enable()
           print "No ip from wifi  restarting AP"

    def check_connectivity(self):
	try:
	    response=urllib2.urlopen('http://google.com',timeout=1)
	    print response
	    return True
        except urllib2.URLError as err:
            print "Failed connecting to the web restarting AP"
            return False   

if __name__ == '__main__':
    rp = RaspberryProvisioner()
    rp.setup()
    rp.enable()
