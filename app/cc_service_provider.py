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

This module authorizes a transaction and validates data, similar to a
credit card processing network.

The validation transaction function in this module is 
adapted from code written by Professor Michael Schwartz, University of Denver 
ICT-4310, Autumn 2020.
************************************
"""

from random import randint
import json
import uuid
import app.cc_service_validators
from app.cc_service_validators import validate_date, validate_card, validate_cvv


def authorize(cc_json_data):
    """Build and return a JSON object similar to a credit card authorization """
	
	# Convert the JSON data to a Python dict
    cc_dict = json.loads(cc_json_data)
    card_object = cc_dict.get('card_object')
    trans_amount = float(cc_dict.get('trans_amount'))
    approval = ''

    # Get card status and failure results from the validate function
    status, failure_code, failure_message = validate_transaction(card_object, trans_amount)

    if status:
        approval = 'Approved'
    else:
        approval = 'Declined'

    # Create a dict for the response authorization
    auth_response = {
        'cardholder': card_object.get('cardholder'),
        'account_number': mask_card(card_object),
        'approval': approval,
        'amount': trans_amount,
        'currency': card_object.get('currency'),
        'trans_id': cc_dict.get('trans_id'),
        'merchant_name': cc_dict.get('merchant_name'),
        'network_id': cc_dict.get('network_id')
    }

    # Append to the dict if the transaction is approved
    if approval == 'Approved':
        # Generate mock approval code if trans is approved
        auth_response['approval_code'] = make_approval_code()
        auth_response['result_code'] = 'OK'

    # Append to the dict if the transaction is declined
    if approval == 'Declined':
        auth_response['approval_code'] = failure_code
        auth_response['result_code'] = failure_message

    # Return the response authorization as a JSON object
    return json.dumps(auth_response)


def make_approval_code():
    """ Generate a UUID to use as an approval code """
    approval_code = "appr_" + str(uuid.uuid4())
    return approval_code

def mask_card(cc_dict):
    """ Convert the first 8 digits of the cc number to *s and return string """
    masked_number = (cc_dict.get('card_number'))
    masked_number = masked_number[-4:].rjust(len(masked_number), "*")
    return masked_number


def validate_transaction(card_object, trans_amount):
    """
    Validate and approve a transaction
    A true credit card processor would verify the card has been issued,
    the information matches the card
    It would also verify the merchant is legitimate and the information matches the merchant.
    Other checks might also occur to prevent fraud.
    """
    card_number = card_object.get('card_number')
    cvv = card_object.get('cvv')
    exp_month = card_object.get('exp_month')
    exp_year = card_object.get('exp_year')
    trans_amount = trans_amount

    # Go through a transaction failure decision tree
    status = True
    failure_code = ''
    failure_message = ''
    # Check if the card is valid
    if not validate_card(card_number, cvv):
        status = False
        failure_code = 401
        failure_message = 'Card is not valid'
    # Check if the transacation amount is between $1-500
    elif trans_amount < 0 or trans_amount > 500:
        status = False
        failure_code = 405
        failure_message =  'Transaction amount threshold exceeded'
    # Check card expiration date
    elif not validate_date(exp_month, exp_year):
        status = False
        failure_code = 408
        failure_message =  'Invalid expiration date'
    # Card is valid
    else:
        status = True
        failure_code = ''
        failure_message = ''
    return status, failure_code, failure_message
        
