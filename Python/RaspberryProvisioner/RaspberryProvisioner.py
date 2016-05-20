import subprocess, json, os, jinja2, time, urllib, urllib2, glob
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
        pass
    
    def hostapd_service(self, command):
        out = subprocess.call(["sudo", "service", "hostapd", command])
        print "hostapd " + command
        pass
    
    def dnsmasq_service(self, command):
        out = subprocess.call(["sudo", "service", "dnsmasq", command])
        print "dnsmasq " + command
        pass
    
    def connect_wifi(self,info):
        path = "linux_config/etc/network/interfaces.wifi.template"
        output = "/etc/network/interfaces"
        info['interface'] = self.config['interface']
        self.write_config(info,path,output)
        self.teardown()
   
        print "Resetting interfaces from connection"
        self.reset_interfaces()
        self.check_connection(self.config['interface'])
        pass
    
    def enable(self):
        self.dhcp_service("start")
        self.hostapd_service("start")
        self.dnsmasq_service("start")
        pass

    def setup(self):
        #Stop services
        self.dhcp_service("stop")
        self.hostapd_service("stop")
        self.dnsmasq_service("stop")
        
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

        #Define DNS config for dnsmasq
        path = "linux_config/etc/dnsmasq.conf.template"
        output = "/etc/dnsmasq.conf"
        self.write_config(self.config, path, output)

        #Reset interfaces to load interface config
        self.reset_interfaces()
        pass

    def teardown(self):
        path = "linux_config/etc/dhcp/dhcpd.conf.template"
        output = "/etc/dhcp/dhcpd.conf"
        
        self.config["enable_ap"] = False
        self.write_config(self.config, path, output)

        self.dhcp_service("stop")
        self.hostapd_service("stop")
        self.dnsmasq_service("stop")

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

    def check_connection(self,interface):
        out = ni.ifaddresses(interface)
        try:
           ip = out[2][0]['addr']
           if ip == self.config['ip']:
               return False
           return True
        except:
            self.setup()
            self.enable()
            print "No Ip obtained from wifi restarting AP"
            return False

    def check_connectivity(self):
        try:
            response=urllib2.urlopen('http://google.com',timeout=1)
            print response.getcode()
            return True

        except urllib2.URLError as err:
            print err
            print "Failed pinging google"
            return False

    def check_radar(self):
        search=os.path.join(self.config['radardir'], '*.[Cc][Ss][Vv]')
        newest = max(glob.iglob(search), key=os.path.getctime)
        statinfo = os.stat(newest)
        if(statinfo.st_size):
            return True
        else:
            return False

    def upload_speed(self, size):
        data=''.join("1" for x in xrange (size))
        params = urllib.urlencode({'data': data })
        print self.config['uploadserver']
	req = urllib2.Request(self.config['uploadserver'])
        starttime = time.time
        res = urllib2.urlopen(req, timeout=10);
        endtime = datetime.datetime.now()
        bytespersec = bytestransfered / (endtime - starttime)
        return bytespersec

    def latency(self,count):
        averagetime=0
        total=0
        for i in range(count):
            error=0
            startTime = time.time()
            try:
                response = urllib2.urlopen('http://google.com', timeout = 5)
            except (urllib2.URLError, socket.timeout), e:
                error=1

            if error==0:
                averagetime = averagetime + (time.time() - startTime)
                total=total+1
            if total==0:
                return False

        return averagetime/total

if __name__ == '__main__':
    rp = RaspberryProvisioner()
    rp.setup()
    rp.enable()
