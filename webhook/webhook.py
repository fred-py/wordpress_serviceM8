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
from threading import Thread
from flask import current_app, render_template
from flask_mail import Mail, Message  # Add missing import statement

load_dotenv(find_dotenv())

"""NOTE: two blueprints are used to separate the mail and webhook, 
refacture for better readability"""

webhook_bp = Blueprint('webhook', __name__)

mail_bp = Blueprint('mail', __name__)

mail = Mail()  # Add this line to create a mail object

to_emails = ['info@unitedpropertyservices.au', 'marketing@unitedropertyservices.au']
#servicem8_key = os.getenv('UPS_KEY')

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
            msg = d.get('fields[message][value]', None)
            # Contactnate message & services
            description = message + ' ' + services
            # Concactnate address, suburb and postcode
            full_address = address + ', ' + suburb + ', ' + postcode
            
            # Concat everything into a single message
            message = f"Name: {name}\nEmail: {email}\nMobile: {mobile}\nAddress: {full_address}\n Description: {description}"
            send_email(to_emails, 'New Enquiry', message)
            """The below is for use with ServiceM8 API, include tha on git for portfolio"""
            #quote = post.ServiceM8(name, email, mobile, full_address, description, servicem8_key)
            #uuid = quote.create_job()
            #quote.create_contact(uuid)
        return '', 200
    except Exception as e:
        print(f"Exception: {e}")


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, message):  # , template, **kwargs):
    """This function is used to send emails asynchronously
    Note, for bulk emails using celery task queue is recommended"""
    app = current_app._get_current_object()  # Get the actual Flask app object
    msg = Message(current_app.config['UNITED_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=current_app.config['UNITED_MAIL_SENDER'],
                  recipients=[to])
    msg.body = msg
    #msg.body = render_template(template + '.txt', **kwargs)
    #msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

#if __name__ == '__main__':
#    app.run(port=4040, debug=True)
