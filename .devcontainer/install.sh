#!/bin/bash

set -e

source /opt/ros/humble/setup.bash
apt update
rosdep init
rosdep --rosdistro=humble update 

pip install -U argcomplete

rm -rf /opt/ros/lcas
mkdir -p /opt/ros/lcas/src
cd /opt/ros/lcas/src
vcs import < /tmp/.devcontainer/lcas.repos
rosdep install --from-paths . -r -i -y
cd /opt/ros/lcas
colcon build

#cd /home/lcas/ws
#colcon build 
echo "source /opt/ros/lcas/install/setup.bash" >> /etc/bash.bashrc

