# MultiChain Semi-Open Blockchain
One of the problems I have had with MultiChain (http://www.multichain.com) is that when a new node wants to join, they have to try to join, and then send the connection request out of band (e.g. through email) to me. I then have to review it, and decide whether I want them to join.

Making the blockchain "anyone can join, send and receive" requires the workaround listed here:  

  https://www.multichain.com/qa/3601/anyone-can-issue-dont-seem-to-work?show=3604#a3604 

which involves creating a public dummy address with no assets that anyone can use to send an unspent transaction to new addresses. I find that a bit of a hack.

I therefore spent some time thinking about an automated method for admitting new participants with a limited set of permissions, namely a method for making MultiChain a semi-open (or semi-permissioned) blockchain.

This repository provides a sample setup for such a semi-open blockchain, using MultiChain as the backend blockchain. Currently this is Linux only. The master node runs a webserver that automates the sign-up of client nodes.

A semi-open blockchain is where some permissions are granted to anyone who wants to join, but specific permissions are only granted to select participants. In this example, anyone can connect, send and receive assets, and activate other accounts to do the same. And there is no need to use a dummy address. However, it does require at least one node with webserve to be active.

Another advantage is that you can have different levels of access for different client families, and allow access to the families through, for example, a website login.

However, the master node is the only one able to create streams, issue more assets, and revoke access.

The system contains two main components: the master node and the client nodes.

## Installation
Clone or download this repository.

Install the required packages and initialize the virtual environment with the install script:

     sudo ./install.sh

## Master Node
The master creates the original blockchain, issues assets (samplecoin in this example), issues further samplecoin automatically as the bank's supplies run low, and automates client signup. 

    ./run-master.sh
    
This sets up and runs a new MultiChain blockchain if it doesn't already exist, and starts a local webserver.

The master webserver runs on port 5050 by default.

## Client Node
The client sets up a client blockchain node, makes a signup request to the master node, launches the blockchain and creates a webserver interface that allows you to check your balance and associate a name with your account, and others to join via your client node.

Subsequently it just launches the node and webserver, as the blockchain node only needs configuration once. The instructions for signing up a client are on the master node website, listed in the previous section.

If you accidentally close the client web browser, the local webserver runs on port 5000.

