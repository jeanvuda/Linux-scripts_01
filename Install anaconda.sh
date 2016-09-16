
# Get the latest version from the continuum website
wget https://repo.continuum.io/archive/Anaconda3-4.1.1-Linux-x86_64.sh

# Give the location where you downloaded
bash '/home/john/Anaconda3-4.1.1-Linux-x86_64.sh'

# Install pip and jupyter
sudo apt install python3-pip
pip3 install --upgrade pip
pip3 install jupyter

# Initiate jupyter notebook
jupyter notebook

