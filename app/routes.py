"""
***********************************
Author: Steven Stackle
Assignment #2, ICT-4310, Autumn 2020, Instructor: Michael Schwartz
Last Revision: October 10, 2020

Description: This Python program demonstrates communication between a 
client and server over HTTP. It uses the Flask framework to start a server on 
the local machine and generate web pages. On the client side, the cardholder 
fills out a payment form. When the cardholder submits the form, the client 
POSTs the data to the server in JSON format. The server responds with a 
message similar to a credit card authorization, also in JSON format.
************************************
"""

from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app.forms import PaymentForm
import json
from app.json_tools import *
from app.cc_service_provider import authorize

# Root and index/home page URLs
@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')

# Payments page URL
@app.route('/payments', methods=['GET', 'POST'])
def payments():
    # Create a Payment Form object
    form = PaymentForm()
	# Do if all form fields are valid
    if form.validate_on_submit():
        ## flash('The transaction was submitted for approval.')
		
		# If the form is POSTed, load it as object and convert to JSON
        if request.method == 'POST':
            form_obj = request.form
            cc_json_data = make_json(form_obj)
            return render_template('results.html', auth_response = authorize(cc_json_data))
	# Reload page if form does not validate
    return render_template('payments.html', title='Make a Payment', form=form)

# Results page URL
@app.route('/results')
def results():
    return render_template('results.html')

