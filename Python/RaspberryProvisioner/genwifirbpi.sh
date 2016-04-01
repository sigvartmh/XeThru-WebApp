#!/usr/bin/env bash
iw dev wlan0 scan ap-force | gawk -f wifi_scan.awk

