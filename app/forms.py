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

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Regexp, NumberRange

class PaymentForm(FlaskForm):
    """ This class builds a Flask form to input cc info """
	
    # All fields include a validator to make sure there is some data
    cardholder = StringField('Customer Name', [DataRequired('Please enter' +
                                                'the name on the card.')])
    # Includes regular expression validator to require 16 digits
    card_number = StringField('16 Digit Credit Card Number',
        validators=[DataRequired('Please enter a valid 16 digit credit' +
                                 'card number.'), Regexp('^(\d{16})?$')])
    # Includes regular expression validator to require 4 digits
    exp_date = StringField('Card Expiration Date MMYY', [DataRequired
                ('Please enter a valid 4 digit expiration date.'),
                                                Regexp('^(\d{4})?$')])
    # Includes regular expression validator to require 3 digits
    cvv = StringField('Card 3 Digit CVV Code', [DataRequired('Please' +
            'enter a valid 3 digit card code.'),Regexp('^(\d{3})?$')])
    trans_amount = DecimalField('Transaction Amount', [DataRequired
            ('Please enter a valid amount.')])
    submit = SubmitField('Submit Payment')
