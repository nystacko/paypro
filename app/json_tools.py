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

import json

def make_json(form_obj):    
    """ Make a python dictionary and return it as a JSON object """
	
	# Make a dict from the selected form fields
    data_dict ={
        'cardholder': form_obj.get('cardholder'),
        'card_number': form_obj.get('card_number'),
        'exp_date': form_obj.get('exp_date'),
        'cvv': form_obj.get('cvv'),
        'trans_amount': form_obj.get('trans_amount')
        }
		
	# Return the dict as a JSON object	
    return json.dumps(data_dict)

def make_dict(json_data):
    """ Convert a JSON object to a Python dictionary """
    cc_dict = json.loads(json_data)
    return cc_dict
