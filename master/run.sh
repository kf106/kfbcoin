#!/bin/bash
# (C) 2019 Keir Finlow-Bates
# See LICENSE for the licensing details of this software

if [ -z $BASH_VERSION ] ; then
	echo -e "You must run this script using bash." 1>&2
	exit 1
fi

source venv/bin/activate

echo -e ""
echo -e "--------------------------------------------------------------------------------"
echo -e "Starting master node                                            "
echo -e "--------------------------------------------------------------------------------"
echo -e ""

# Proof of concept - so minimal error checking!
# check if the blockchain is set up and running
# if it is not running, start it
# if it does not exist, create it

# the master (first blockchain) is run in the default directory.
# semi-open nodes are run in a custom directory to allow
# two blockchains to work on one machine so you can test
# both on the same machine

# Note: we are assuming that if the blockchain exists,
# then the relevant sample digital assets have been created.

if [ -e ~/.multichain/semi-open/params.dat ]
then
  echo -e "Semi-open blockchain already exists."
  multichain-cli semi-open getinfo
  if [ $? -eq 0 ]
  then
    echo -e "Semi-open blockchain is running."
  else
    echo -e "Starting semi-open blockchain daemon."
    # run with reindex in case there was a broken shutdown
    multichaind semi-open -reindex=1 -daemon
  fi
else
  multichain-util create semi-open
  multichaind semi-open -daemon
  # create the initial sample coin
  masteraddress=$(multichain-cli semi-open listpermissions issue | python -c "import json,sys;obj=json.load(sys.stdin);print(obj[0]['address']);")
  sleep 5 # it can take a while for the blockchain to be ready
  multichain-cli semi-open issue $masteraddress '{"name":"samplecoin","open":true}' 10000 1

fi

# this runs the application
echo -e "Starting master interface"
export FLASK_APP=master-webserver.py
google-chrome --app=http://localhost:5050 &>/dev/null &
flask run --host=0.0.0.0 --port ${1:-5050}

echo -e ""
echo -e "--------------------------------------------------------------------------------"
echo -e "Master node running on localhost:5050                                            "
echo -e "--------------------------------------------------------------------------------"
echo -e ""
