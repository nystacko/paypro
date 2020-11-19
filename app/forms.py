"""
***********************************
Author: Steven Stackle
Assignment #5, ICT-4310, Autumn 2020, Instructor: Michael Schwartz
Last Revision: November 5, 2020

Description: This Python program demonstrates communication between a 
client and server over HTTP. It uses the Flask framework to start a server on 
the local machine and generate web pages. On the client side, the cardholder 
fills out a payment form. When the cardholder submits the form, the client 
POSTs the data to the server in JSON format. The server responds with a 
message similar to a credit card authorization, also in JSON format.

The input form coding in this application is based on  
*The Flask Mega-Tutorial Part III: Web Form* by Miguel Grinberg.
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

The validation functions and cc_dictionary in this module are used from or 
adapted from code written by Professor Michael Schwartz, University of Denver 
ICT-4310, Autumn 2020
************************************
"""

import re
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Regexp, NumberRange, ValidationError


# A dictionary of regular expressions representing valid credit cards from 
#   several credit card networks
cc_dictionary = {
    'visa': r'^4[0-9]{12}(?:[0-9]{3})?$',
    'mastercard': r'^5[1-5][0-9]{14}$|^2(?:2(?:2[1-9]|[3-9][0-9])|[3-6][0-9][0-9]|7(?:[01][0-9]|20))[0-9]{12}$',
    'amex': r'^3[47][0-9]{13}$',
    'discover': r'^65[4-9][0-9]{13}|64[4-9][0-9]{13}|6011[0-9]{12}|(622(?:12[6-9]|1[3-9][0-9]|[2-8][0-9][0-9]|9[01][0-9]|92[0-5])[0-9]{10})$',
    'diners_club': r'^3(?:0[0-5]|[68][0-9])[0-9]{11}$',
    'jcb': r'^(?:2131|1800|35[0-9]{3})[0-9]{11}$'
}

def is_accepted_credit_card(credit_card_string):
    """ Returns credit card vendor info, or False if card is invalid """
    credit_card = re.sub(r'[\D]', '', credit_card_string)
    for key, value in cc_dictionary.items():
        if re.fullmatch(value, credit_card):
            return key
    return False

def verify_luhn(form, field, debug=False):
    """Verify via Luhn algorithm whether a credit card number has a valid last
       digit. Raise validation error for invalid card."""
    credit_card_string = field.data
    credit_card = re.sub(r'[\D]', '', credit_card_string)
    digit_sum = 0
    cc_parity = len(credit_card) % 2
    for i in range(len(credit_card)-1, -1, -1):
        j = int(credit_card[i])
        if (i + 1) % 2 != cc_parity:
            j = j * 2
            if j > 9:
                j = j - 9
        digit_sum = digit_sum + j
    if debug:
        return digit_sum % 10 == 0, "check sum computed = " + str(digit_sum)
    if digit_sum % 10 != 0:
        raise ValidationError('The credit card number is not valid.')

def verify_month(form, field):
    """ Raise validation error if the month is not between 1-12 """
    exp_month = field.data
    exp_month = int(exp_month)
    if exp_month < 1 or exp_month > 12:
	    raise ValidationError('The card expiration month is not valid.')

def validate_date(form, field):
    """ Raise validation error if month/year are less than current 
        month/exp_year or
        exp_year is more than 5 years in the future.
    """
    max_future_year=5
    today = datetime.date.today()
    exp_year = form.exp_year.data
    exp_month = form.exp_month.data
    expires = datetime.date(int(exp_year), int(exp_month), 28)
    # return expires > today and int(exp_year) - today.year < max_future_year
    if expires < today or int(exp_year) - today.year > max_future_year:
	    raise ValidationError('The card expiration date is not valid.')


def validate_cvv(form, field):
    """ Raise validation error for invalid CVV """
    card_number = form.card_number.data
    cvv = form.cvv.data
    credit_card = re.sub(r'[\D]', '', card_number)
    card_type = is_accepted_credit_card(credit_card)
    if card_type == "amex" and len(str(cvv)) != 4:
        raise ValidationError('The card CVV is not valid.')

    if card_type and len(str(cvv)) != 3:
        raise ValidationError('The card CVV is not valid.')

class PaymentForm(FlaskForm):
    """ This class builds a Flask form to input cc info """
	
    # All fields include a Data Required validator to make sure there is some 
    # data
    cardholder = StringField('Customer Name', [DataRequired('Please enter' +
                                                'the name on the card.')])
    # Uses Luhn algorithm to verify the credit card number
    card_number = StringField('16 Digit Credit Card Number',
        validators=[DataRequired('Please enter a valid 16 digit credit' +
                                 'card number.'), verify_luhn])
	# Includes validation that month is between 1-12
    exp_month = StringField('Card Expiration Month MM', [DataRequired
                ('Please enter a valid 2 digit expiration month.'),
                                                verify_month])
    # Includes expiration date validation
    exp_year = StringField('Card Expiration Year YYYY', [DataRequired
                ('Please enter a valid 4 digit expiration year.'),
                                    validate_date])
    # Includes validation that CVV is the correct number of digits
    cvv = StringField('Card CVV Code', [DataRequired('Please' +
            'enter a valid card CVV code.'), validate_cvv])
    trans_amount = DecimalField('Transaction Amount', [DataRequired
            ('Please enter a valid amount.')])
    submit = SubmitField('Submit Payment')

