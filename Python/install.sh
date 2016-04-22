#!/bin/bash
sudo apt-get update
for i in `cat dependencies.txt`;
do sudo apt-get install $i -y;
done
pip install -r requirements.txt
