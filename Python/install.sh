#!/bin/bash
if [[ $UID != 0 ]]; then
    echo "Please run script as sudo:"
    sudo bash $0 $*
    exit 1
fi

apt-get update
for i in `cat dependencies.txt`;
do apt-get install $i -y;
done
pip install -r requirements.txt
