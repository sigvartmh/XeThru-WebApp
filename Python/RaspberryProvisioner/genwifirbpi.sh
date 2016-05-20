#!/usr/bin/env bash
iw dev wlan0 scan ap-force | gawk -f $1/wifi_scan.awk

