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

from app.json_tools import *
from random import randint
import json

def authorize(cc_json_data):
    """Build and return a JSON object similar to a credit card authorization """
	
	# Convert the JSON data to a Python dict
    cc_dict = make_dict(cc_json_data)
    trans_amount = int(cc_dict.get('trans_amount'))
    approval = ''

    # Hard code a maximum ammount for transaction approval
    if trans_amount <= 500:
        approval = 'Approved'
    else:
        approval = 'Declined'

    # Create a dict for the response authorization
    auth_response = {
        'account_number': mask_card(cc_dict),
        'approval': approval
    }

    # Append to the dict if the transaction is approved
    if approval == 'Approved':
        auth_response['approval_code'] = make_approval_code()
        auth_response['result_code'] = 'OK'

    # Return the response authorization as a JSON object
    return json.dumps(auth_response)


def make_approval_code():
    """ Generate a random 6-digit number similar to an approval code """
    approval_code = randint(0, 999999)
    approval_code = str(approval_code)
    approval_code = approval_code.zfill(6)
    return approval_code


def mask_card(cc_dict):
    """ Convert the first 8 digits of the cc number to *s and return string """
    masked_number = (cc_dict.get('card_number'))
    masked_number = masked_number[-4:].rjust(len(masked_number), "*")
    return masked_number
        

