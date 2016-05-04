#!/bin/bash
if [[ $UID != 0 ]]; then
    echo "Please run script as sudo:"
    sudo bash $0 $*
    exit 1
fi

#Setup Path and command for running application
base=$(pwd)
app="wifi_ap.py"
#Change this to >> file to log output of app data
command="/usr/bin/python ${base}/${app} &> /dev/null"

#install dependencies
apt-get update
for i in `cat dependencies.txt`;
do apt-get install $i -y;
done
pip install -r requirements.txt
apt-get remove python-dev

#Install crontab with starting the app on reboot
crontab -l | { cat; echo "@reboot ${command}";} | crontab -
