#!/bin/bash
# Author: Jean Vuda

sudo apt-get update
sudo apt-get install openssh-server
sudo ssh -p 3022 osboxes@127.0.0.1
