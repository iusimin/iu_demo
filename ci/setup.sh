#!/bin/bash

# Getting machine version
unameOut="$(uname -s)"
case "$unameOut" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    *)          machine="UNKNOWN"
esac
if [ "$machine" = "UNKNOWN" ]; then
    echo "Unsupport OS $unameOut"
    exit
fi
echo "Running on system: $machine..."

if [ -z "$IU_HOME" ]; then
    echo "Please set environment variable IU_HOME"
    exit
else
    echo "IU_HOME: $IU_HOME"
fi

# Install docopt and cli tool
sudo pip install docopt
sudo ln -s $IU_HOME/ci/iu-cli.py /usr/local/bin/iu-cli
sudo chmod 755 /usr/local/bin/iu-cli

# Setup hosts
host_setup=`grep "# BEGIN - IU hosts setup" /etc/hosts`
if [ -z "$host_setup" ]; then
    echo "Installing /etc/hosts..."
    sudo sh -c "cat $IU_HOME/ci/hosts >> /etc/hosts"
else
    echo "hosts already setup, skip.."
fi

# Build up containers
docker-compose -f $IU_HOME/ci/docker-compose/stage.yml build