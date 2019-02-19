#!/usr/bin/env python
# (C) 2019 Keir Finlow-Bates
# See LICENSE for the licensing details of this software

from flask import Flask, render_template, session, request
import sys
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from time import sleep
from modules.blockchain import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clientapp450i46##'

# precursor string for calling multichain command line interface
multichainCli = "multichain-cli -datadir=~/.multichain-client -port=19255 -rpcport=19254 semi-open "
clientAddress = getAddress(multichainCli)

###
#  WTForms
###

class NameForm(FlaskForm):
    currentname = StringField('Current name', validators=[DataRequired()])
    submit = SubmitField('Update')

###
# Routes for client pages
###

# Route for serving up the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
   
    if request.method == 'POST':
        if form.validate() == False:
            # validate here
            print("NameForm didn't validate")
        else:
            print("Got the NameForm with " + form.currentname.data )
            writeName(multichainCli, form.currentname.data)
            sleep(5)

    balances = getBalances(multichainCli)

    if not checkActivate(multichainCli):
        return render_template(
            'client/index-sub.html',
            currentname = getNameFromAddress(multichainCli, clientAddress),
            address = clientAddress,
            coins = balances["samplecoin"],
            form = NameForm(),
            nodeaddress = getNodeAddress(multichainCli)
        )
    else:
        return render_template(
            'client/index.html',
            currentname = getNameFromAddress(multichainCli, clientAddress),
            address = clientAddress,
            coins = balances["samplecoin"],
            form = NameForm(),
            nodeaddress = getNodeAddress(multichainCli)
        )    

# Route for automatic client-approved signup 
# note: as a client can't issue more coins
# this doesn't grant coints though. You could
# give away some of your own

@app.route('/signup', methods=['POST'])
def login():
    if request.method == 'POST':
        # get posted address (should do error checking on this)
        sent_address = request.get_json()['address']
        print("Got signup request with address: " + sent_address)
        # grant connect send and receive
        print(clientsignupAddress(multichainCli, sent_address))
        # if you want the client can watch its signups addresses
        # print(importAddress(multichainCli, sent_address))          
        # send some of the assets (samplecoin) to the new address
        # you'll need to check that you have enough balance or client app will crash
        # print(issueAssetToAddress(multichainCli, sent_address, "samplecoin", "10"))  
        return render_template('master/signup_success.html')       
    else:
        return render_template('master/signup_error.html') 


