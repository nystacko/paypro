"""
***********************************
Author: Steven Stackle
Assignment #4, ICT-4310, Autumn 2020, Instructor: Michael Schwartz
Last Revision: November 7, 2020

Description: This Python program demonstrates communication between a
client and server over HTTP. It uses the Flask framework to start a server on
the local machine and generate web pages. On the client side, the cardholder
fills out a payment form. When the cardholder submits the form, the client
POSTs the data to the server in JSON format. The server responds with a
message similar to a credit card authorization, also in JSON format.

This module controls the routing logic.
************************************
"""

from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app.forms import PaymentForm
import json
from app.json_tools import make_json
from app.cc_service_provider import authorize
import sqlite3
from app.merch_data_store import write_auth_to_db, trans_to_list

# Root and index/home page URLs
@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')

# Payments page URL
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    # Create a Payment Form object
    form = PaymentForm()
    # Do if all form fields are valid
    if form.validate_on_submit():
        ## flash('The transaction was submitted for approval.')

        # If the form is POSTed, load it as object and convert to JSON
        if request.method == 'POST':
            # Request key-value pairs from the HTML form
            form_obj = request.form
            # Convert the form data into JSON
            cc_json_data = make_json(form_obj)
            # 'Request' authorization from the credit card service provider
            # using the 'authorize' function.
            auth_response = authorize(cc_json_data)
            
            # Pull approval and amount out of JSON to send to page
            response_dict = json.loads(auth_response)
            approval = response_dict.get('approval')
            amount = response_dict.get('amount')

            # Save the authorization response to the database
            write_auth_to_db(auth_response)
            # Display the authorization response in the page template.
            return render_template('make-payment.html', \
                auth_response=auth_response, approval = approval,\
                amount = amount)
        # Reload page if form does not validate
    return render_template('payment.html', title='Make a Payment', form=form)

# Results page URL
@app.route('/make-payment')
def results():
    # return render_template('make-payment.html')
    return redirect('make-payment.html')

# Transaction list page URL
@app.route('/trans-list')
def trans_list():
    trans_list = trans_to_list()
    return render_template('trans-list.html', trans_list = trans_list)