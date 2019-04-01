#!/bin/bash
# (C) 2019 Keir Finlow-Bates
# See LICENSE for the licensing details of this software

if [ -z $BASH_VERSION ] ; then
	echo -e "You must run this script using bash." 1>&2
	exit 1
fi

# Get latest version. An amazing auto-update feature
echo -e "Checking if you have latest version..."
git pull

# uncomment for debug info
# set -x

source venv/bin/activate

echo -e ""
echo -e "--------------------------------------------------------------------------------"
echo -e "Starting basic node                                            "
echo -e "--------------------------------------------------------------------------------"
echo -e ""

# Proof of concept - so minimal error checking!
# check if the blockchain is set up and running
# if it is not running, start it
# if it does not exist, create it

# the master (first blockchain) is run in the default .multichain directory.
# basic nodes are run in a custom .multichain-client directory to allow
# two blockchains with the same name to work on one machine so you can test
# both on the same machine

# check if the blockchain node is already configured
if [ -e ~/.multichain-client/semi-open/params.dat ]
then
  echo -e "Basic node blockchain already exists."
  multichain-cli -datadir=~/.multichain-client -port=19255 -rpcport=19254 semi-open getinfo
  if [ $? -eq 0 ]
  then
    echo -e "Basic node blockchain is running."
  else
    echo -e "Starting basic node blockchain daemon."
    # run with reindex in case there was a broken shutdown
    multichaind -datadir=~/.multichain-client -port=19255 -rpcport=19254 -reindex=1 semi-open -daemon
  fi

# otherwise sign up, get address activated, and start node
else
  if [ -z "$1" ]
  then
    echo -e "No blockchain address supplied"
	exit 0
  else
    if [ -z "$2" ]
    then
      echo -e "No signup address supplied"
	  exit 0

    else
      # create basic node instance by connecting to master, extract your local address
      # and send it to the master node webserver for automatic connection
      mkdir ~/.multichain-client
      blockchain=$1
      # this complicated expression extracts the node address from the multichain suggested signup message
      myaddress=$(multichaind -datadir=~/.multichain-client -port=19255 -rpcport=19254 $1 | grep -P -i -o -m 1 '(?<=grant )\S+' | sed -r 's/^\W|\W$//g')
      echo -e "My node address: $myaddress"
      # POST section to sign up
      curl --header "Content-Type: application/json" --request POST --data '{"address":"'"$myaddress"'"}' $2 
      # Give server a chance to sign you up
      sleep 8
      echo -e "Starting client node blockchain daemon."
      multichaind -datadir=~/.multichain-client -port=19255 -rpcport=19254 semi-open -daemon     
    fi
  fi
fi

# this runs the application
echo -e "Starting client interface"
# start local webserver and browser
google-chrome --app=http://localhost:5000 --incognito &>/dev/null &
FLASK_APP=client.py flask run --host=0.0.0.0 --port 5000

echo -e ""
echo -e "--------------------------------------------------------------------------------"
echo -e "Basic node running on localhost:5000                                           "
echo -e "--------------------------------------------------------------------------------"
echo -e ""
