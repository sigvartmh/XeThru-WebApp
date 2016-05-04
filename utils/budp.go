package main

import (
	//	"fmt"
	"net"
	"time"
)

func main() {
	var ip net.IP
	var mac net.HardwareAddr

	for {
		ifaces, _ := net.Interfaces()

		for _, i := range ifaces {
			if i.Name == "en0" {
				mac = i.HardwareAddr
				addrs, _ := i.Addrs()
				for _, v := range addrs {
					switch T := v.(type) {
					case *net.IPNet:
						ip = T.IP
					}
				}
			}
		}
		ip[15] = 255

		saddr, _ := net.ResolveUDPAddr("udp", ip.String()+":3001")
		Conn, _ := net.DialUDP("udp", nil, saddr)
		Conn.Write([]byte(mac.String()))
		Conn.Close()
		time.Sleep(500 * time.Millisecond)
	}
}
