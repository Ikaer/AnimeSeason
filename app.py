import os
import json
from flask import Flask
from routes.providers_routes import provider_bp
from routes.mal_routes import mal_bp
from routes.main_routes import main_bp
import configparser
import secrets
import logging
logging.basicConfig(level=logging.DEBUG)

# === CONFIGURATION ===
config = configparser.ConfigParser()
config.read('config.ini')
DB_FOLDER = config['Paths']['anime_db_path']


os.makedirs(DB_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Register blueprints
app.register_blueprint(provider_bp)
app.register_blueprint(mal_bp)
app.register_blueprint(main_bp)

# Add config values to app.config
app.config['DB_FOLDER'] = DB_FOLDER
app.config['CLIENT_ID'] = config['ApiKey']['mal']
app.config['REDIRECT_URI'] = config['ApiKey'].get('redirect_uri', None)
app.config['AUTH_URL'] = 'https://myanimelist.net/v1/oauth2/authorize'
app.config['TOKEN_URL'] = 'https://myanimelist.net/v1/oauth2/token'

if __name__ == '__main__':
    app.run(debug=True, port=12345)
