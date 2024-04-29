"""App initialisation and Flask Blueprint registration"""
import os
from flask import Flask
from webhook.webhook import webhook_bp
from mail.mail import mail_bp, mail
import config as Config


port = int(os.environ.get('PORT', 4242))  # This is needed to deploy on fl0


app = Flask(__name__)
app.config.from_object(Config.Config)

mail.init_app(app)

app.register_blueprint(webhook_bp)
app.register_blueprint(mail_bp)

if __name__ == '__main__':
    app.run(port=port, debug=True)