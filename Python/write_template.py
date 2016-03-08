import os
import jinja2

loader = jinja2.FileSystemLoader( os.path.dirname(__file__))
env = jinja2.Environment( loader=loader )

t = "linux_config/wifi_test.conf"

output = { "wlan":{
			"ssid23" : "testWlan",
		  	"password" : "********"
		 	}
		 }


def write_config(var, path, output):

	template = env.get_template(path)
	try:
		temp = template.render(var)
	except:
		print "Wrong in template"
		raise


	with open(output, "w") as conf:
		conf.write(temp)

write_template(output, t, "test_func.conf")