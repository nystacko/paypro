# Paypro Web Application

This Python program demonstrates communication between a 
client and server over HTTP. It uses the Flask framework to start a server on 
the local machine and generate web pages. On the client side, the cardholder 
fills out a payment form. When the cardholder submits the form, the client 
POSTs the data to the server in JSON format. The server responds with a 
message similar to a credit card authorization, also in JSON format.

# Requirements
* Flask
* Flask-WTF
* WTForms

# Running the application
Open a terminal session.
Navigate to the directory containing the application.
Export the flask environment variable:
    In Windows: set FLASK_APP=paypro.py
    Other operating systems: export FLASK_APP= paypro.py
Execute the Flask command: flask run
Open a web browser and navigate to: http://localhost:5000/ or http://127.0.0.1:5000
To enter a card transaction, click 'Make a Payment' and fill out the form fields.

To see a list of all card transactions, click 'Settle Transactions.'