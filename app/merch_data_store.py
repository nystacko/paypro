"""
***********************************
Author: Steven Stackle
Assignment #5, ICT-4310, Autumn 2020, Instructor: Michael Schwartz
Last Revision: November 7, 2020

Description: This Python program demonstrates communication between a
client and server over HTTP. It uses the Flask framework to start a server on
the local machine and generate web pages. On the client side, the cardholder
fills out a payment form. When the cardholder submits the form, the client
POSTs the data to the server in JSON format. The server responds with a
message similar to a credit card authorization, also in JSON format.

The input form coding in this application is based on  
*The Flask Mega-Tutorial Part III: Web Form* by Miguel Grinberg.
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

This module writes to and reads from the merchant's transaction database.
************************************
"""

import json
import sqlite3

def write_auth_to_db(auth_response):
    """ Store the authorization response in the database """
    # Build a dictionary from the JSON authorization response
    response_dict = json.loads(auth_response)

    # Initialize the variables with data from the dictionary
    cardholder = response_dict.get('cardholder')
    account_number = response_dict.get('account_number')
    approval = response_dict.get('approval')
    amount = response_dict.get('amount')
    currency = response_dict.get('currency')
    trans_id = response_dict.get('trans_id')
    merchant_name = response_dict.get('merchant_name')
    network_id = response_dict.get('network_id')
    approval_code = response_dict.get('approval_code')
    result_code = response_dict.get('result_code')

    # Save the the transaction information to a SQLite database
    try:
        with sqlite3.connect("transactions.db") as conn:
            cur = conn.cursor() 
            cur.execute("""INSERT INTO merch_trans (cardholder,account_number,\
                       approval, amount, currency, trans_id, merchant_name,\
                           network_id, approval_code, result_code) \
                   VALUES(?,?,?,?,?,?,?,?,?,?)""", (cardholder,account_number,\
                       approval, amount, currency, trans_id, merchant_name,\
                           network_id, approval_code, result_code))

            conn.commit()
            ## msg = "Record successfully added"
    
    except:
        conn.rollback()
        ## msg = "Error in insert operation"
        pass
      
    finally:
        conn.close()

def trans_to_list():
    """ Return the transactions database as a list """
    try:
        with sqlite3.connect("transactions.db") as conn:
            trans_list = []
            cur = conn.cursor()
            cur.execute("""SELECT * from merch_trans""")
            for row in cur.fetchall():
                trans_list.append(row)
            return trans_list
    except:
        pass
    finally:
        conn.close()