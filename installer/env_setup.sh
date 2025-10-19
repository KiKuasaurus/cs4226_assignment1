#!/bin/bash
pyenv install 3.9.19
pyenv global 3.9.19

pip install wheel mininet setuptools netaddr six eventlet oslo_config routes tinyrpc webob packaging

# git clone https://github.com/mininet/mininet
git clone https://github.com/faucetsdn/ryu.git

sudo apt-get install -y openvswitch-switch

./mininet/util/install.sh
sudo apt-get install -y python3-pip
sudo pip install mininet
cd ryu
python ./setup.py install
cd ..

pip install --force-reinstall "eventlet==0.31.1"

sudo mn -c
