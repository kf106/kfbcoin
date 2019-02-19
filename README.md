# MultiChain Semi-Open Blockchain
One of the problems I have had with MultiChain is that when a new node wants to join, they have to try to join, and then send the connection request out of band (e.g. through email) to me. I then have to review it, and decide whether I want them to join.

I therefore spent some time thinking about an automated method for admitting new participants with a limited set of permissions, namely a method for making MultiChain a semi-open (or semi-permissioned) blockchain.

This repository provides a sample setup for such a semi-open blockchain, using MultiChain (http://www.multichain.com) as the backend blockchain. Currently this is Linux only. The master node runs a webserver that automates the sign-up of client nodes.

A semi-open blockchain is where some permissions are granted to anyone who wants to join, but specific permissions are only granted to select participants. In this example, anyone can connect, send and receive assets, and activate other accounts to do the same.

However, the master node is the only one able to create streams, issue more assets, and revoke access.

The system contains two main components: the master node and the client nodes.

## Installation
Clone or download this repository.

Depending on whether you are planning to run a master node (i.e. start a new blockchain) or a client node (i.e. connect to an existing blockchain), either got to the master folder or the client folder:

     cd master

or

     cd client

Install the required packages and initialize the virtual environment with the install script:

     sudo ./install.sh
     
Then run the Python webserver.

    ./run.sh
    
This starts a local webserver.

## Master Node
The master creates the original blockchain, issues assets (samplecoin in this example), issues further samplecoin automatically as the bank's supplies run low, and automates client signup. 

The master webserver runs on port 5050 by default.

## Client Node
The client sets up a client blockchain node, makes a signup request to the master node, launches the blockchain and creates a webserver interface that allows you to check your balance and associate a name with your account.

Subsequently it just launches the node and webserver, as the blockchain node only needs configuration once.

If you accidentally close the client, the local webserver runs on port 5000.

