"""App initialisation and Flask Blueprint registration"""
import os
from flask import Flask
from webhook.webhook import webhook_bp
import config as Config

port = int(os.environ.get('PORT', 4242))  # This is needed to deploy on fl0

app = Flask(__name__)
app.config.from_object(Config.Config)

app.register_blueprint(webhook_bp)

if __name__ == '__main__':
    app.run(port=port, debug=True)