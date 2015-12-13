#!/bin/bash
# Author: Jean Vuda

# Install SSH handler
sudo apt-get update
sudo apt-get install openssh-server
sudo ssh -p 3022 osboxes@127.0.0.1

# Install Java
sudo apt-add-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer

# Install Pycharm
mkdir -p ~/opt/packages/pycharm
cd ~/opt/packages/pycharm
wget http://download.jetbrains.com/python/pycharm-5.0.2.tar.gz
gzip -dc pycharm-5.0.2.tar.gz | tar xf -
ln -s ~/opt/packages/pycharm/pycharm-community-4.0.4 ~/opt/pycharm

# Start PyCharm
~/opt/pycharm/bin/pycharm.sh
