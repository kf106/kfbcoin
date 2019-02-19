#!/usr/bin/env python
from flask import Flask, render_template, session, request
import sys
import json
from random import random
from threading import Lock
from modules.blockchain import *

multichainCli = "multichain-cli semi-open "

app = Flask(__name__)
app.config['SECRET_KEY'] = 'masterapp450jh906#&'

###
# Static pages
###

# Route for serving up the index page
@app.route('/')
def index():
    return render_template(
        'master/index.html',
         nodeaddress = getNodeAddress(multichainCli)
    )


# Route for serving up the admin page
@app.route('/admin')
def admin():
    return render_template(
        'master/admin.html',
         balances = json.dumps(getBalances(multichainCli), sort_keys = True, indent = 4, separators = (',', ': ')),
         clients = json.dumps(listAddresses(multichainCli), sort_keys = True, indent = 4, separators = (',', ': '))
    )

# Route for automatic master-approved client signup
@app.route('/signup', methods=['POST'])
def login():
    if request.method == 'POST':
        # get posted address (should do error checking on this)
        sent_address = request.get_json()['address']
        print("Got signup request with address: " + sent_address)
        # grant connect send receive and activate
        print(signupAddress(multichainCli, sent_address))
        # asset bank imports all addresses
        print(importAddress(multichainCli, sent_address))          
        # issue more of the assets (gold and xp) to the new address
        print(issueAssetToAddress(multichainCli, sent_address, "samplecoin", "1000"))  
        return render_template('master/signup_success.html')       
    else:
        return render_template('master/signup_error.html') 

