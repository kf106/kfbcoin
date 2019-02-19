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
    clientname = StringField('Client name', validators=[DataRequired()])
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
            print("Got the NameForm with " + form.clientname.data )
            writeName(multichainCli, form.clientname.data)
            sleep(5)

    balances = getBalances(multichainCli)
    return render_template(
        'index.html',
        currentname = getNameFromAddress(multichainCli, clientAddress),
        address = clientAddress,
        coins = balances["samplecoin"],
        form = NameForm()
    )    



