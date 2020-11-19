"""
***********************************
Author: Steven Stackle
Assignment #5, ICT-4310, Autumn 2020, Instructor: Michael Schwartz
Last Revision: November 18, 2020

Description: This Python program demonstrates communication between a 
client and server over HTTP. It uses the Flask framework to start a server on 
the local machine and generate web pages. On the client side, the cardholder 
fills out a payment form. When the cardholder submits the form, the client 
POSTs the data to the server in JSON format. The server responds with a 
message similar to a credit card authorization, also in JSON format.

The input form coding in this application is based on  
*The Flask Mega-Tutorial Part III: Web Form* by Miguel Grinberg.
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

This module does format conversion to-from JSON and dictionary objects.
************************************
"""

import json
import uuid
import random


def make_json(form_obj):    
    """ Make a python dictionary and return it as a JSON object """
	
	# Make a dict from the selected form fields

    card_object = {
        'cardholder': form_obj.get('cardholder'),
        'card_number': form_obj.get('card_number'),
        'exp_month': form_obj.get('exp_month'),
		'exp_year': form_obj.get('exp_year'),
        'cvv': form_obj.get('cvv'),
        'currency': 'usd'
        }
    
    merchant_info = make_merchant_object()

    data_dict = {
        'card_object': card_object,
        'trans_amount': form_obj.get('trans_amount'),
        'trans_id': "auth_" + str(uuid.uuid4()),
        'merchant_name': merchant_info.get('merchant_name'),
        'network_id': merchant_info.get('network_id')
        }

	# Return the dict as a JSON object	
    return json.dumps(data_dict)

def make_merchant_object():
    """ Build a dictionary of merchant info and return the dict """
    merchant_dict = {
        'merchant_name' : 'Stacks',
        'network_id': 3970
    }

    return merchant_dict
    

def make_dict(json_data):
    """ Convert a JSON object to a Python dictionary """
    cc_dict = json.loads(json_data)
    return cc_dict
