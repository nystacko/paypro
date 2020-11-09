"""
***********************************
Author: Steven Stackle
Assignment #4, ICT-4310, Autumn 2020, Instructor: Michael Schwartz
Last Revision: October 10, 2020

Description: This Python program demonstrates communication between a 
client and server over HTTP. It uses the Flask framework to start a server on 
the local machine and generate web pages. On the client side, the cardholder 
fills out a payment form. When the cardholder submits the form, the client 
POSTs the data to the server in JSON format. The server responds with a 
message similar to a credit card authorization, also in JSON format.
************************************
"""

# Instantiate Flask
from app import app
