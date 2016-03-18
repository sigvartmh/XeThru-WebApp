#!/usr/bin/bash
/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s | awk -F ' ' 'NR >= 2 {print "{ \"ssid\":\"" $1 "\",\n" "\"mac\":\"" $2 "\",\n" "\"strenght\":\"" $3 "\",\n" "\"channel\":\""$4 "\",\n" "\"security\":\""$7"\"}"}'
