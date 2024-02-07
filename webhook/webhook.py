"""
This webhook listens to the POST request 
from Elementor contact form.

NOTE: To test webhook, use ngrok
to expose localhost to the internet."""

# NOTE: Must also run pip install pyngrok to call ngrok from Terminal
# Get Auth at https://dashboard.ngrok.com/get-started/your-authtoken
# Quiclstart: https://dashboard.ngrok.com/get-started/setup/macos


import os
from flask import Blueprint, request
from dotenv import load_dotenv, find_dotenv
from servicem_client import post_servicem as post
from pprint import pprint

load_dotenv(find_dotenv())

webhook_bp = Blueprint('webhook', __name__)

servicem8_key = os.getenv('UPS_KEY')

#app = Flask(__name__)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook_received():
    #data = request.text
    try:
        content_type = request.headers.get('Content-Type')
        print(f"Content-Type: {content_type}")
        if content_type == 'application/x-www-form-urlencoded':
            form_data = request.form
            d = dict(form_data)  # This is a flat dict,. keys are strings representing a nested structure
            #pprint(f'This is a dict ===>>{d}')
            # Using the .get method to get the value of the key,
            # if the key is not present,
            # it returns None as opposed to key error
            name = d.get('fields[name][value]', None)
            email = d.get('fields[email][value]', None)
            mobile = d.get('fields[mobile][value]', None)
            address = d.get('fields[address][value]', None)
            suburb = d.get('fields[suburb][value]', None)
            postcode = d.get('fields[postcode][value]', None)
            services = d.get('fields[services][value]', None)
            message = d.get('fields[message][value]', None)
            # Contactnate message & services
            description = message + ' ' + services
            # Concactnate address, suburb and postcode
            full_address = address + ', ' + suburb + ', ' + postcode
            quote = post.ServiceM8(name, email, mobile, full_address, description, servicem8_key)
            uuid = quote.create_job()
            quote.create_contact(uuid)
        return '', 200
    except Exception as e:
        print(f"Exception: {e}")
    


#if __name__ == '__main__':
#    app.run(port=4040, debug=True)
