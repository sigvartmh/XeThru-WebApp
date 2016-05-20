package main

import (
	//"fmt"
	"net"
	//"reflect"
	"time"
)

func main() {
	var ip net.IP
	var mac net.HardwareAddr
	var addrs []net.Addr
	for {
		ifaces, _ := net.Interfaces()

		for _, i := range ifaces {
			if i.Name == "wlan0" {
				mac = i.HardwareAddr
				addrs, _ = i.Addrs()

			}
		}

		for _, ipaddr := range addrs {
			ip = ipaddr.(*net.IPNet).IP
			if ip.To4() != nil {
				ip[15] = 255
				saddr, _ := net.ResolveUDPAddr("udp", ip.String()+":8080")
				Conn, _ := net.DialUDP("udp", nil, saddr)
				Conn.Write([]byte(mac.String()))
				Conn.Close()
				time.Sleep(1000 * time.Millisecond)
			}
		}
		time.Sleep(1000 * time.Millisecond)
	}
}
