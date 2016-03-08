class APMode:
	def restart_dhcp_service:
		#service isc-dhcp-server restart
		print "DHCP server restarted"
	def restart_hostapd_service:
		#service hostapd restart
		print "hostapd restarted"
	def enable_wifi:
		#service isc-dhcp-server stop
	def enable_AP:
		#write ap template -> /etc/network/interfaces
		#write DHCP conf dhcpd.conf.template -> /etc/dhcp/dhcpd.conf
		#write isc-dhcp-server.template -> /etc/defult/isc-dhcp-server
		#write hostapd.conf.template -> /etc/hostapd/hostapd.conf
		#write hostpad.template -> /etc/default/hostapd
		#reboot wlan
		#restart dhcp service isc-dhcp-server restart
		#restart hostapd service hostapd restart


	def write_wlan:
		write_template_to_file()