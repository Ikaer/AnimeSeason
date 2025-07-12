import os
import logging
import configparser
import secrets

from flask import Flask
from db.anime_db_storage import init_anime_db_storage
from mal.mal_auth import init_mal_auth
from routes.providers_routes import provider_bp
from routes.mal_routes import mal_bp
from routes.main_routes import main_bp

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_config(config_path: str = 'config.ini') -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def create_app() -> Flask:
    config = load_config()
    db_folder: str = config['Paths']['anime_db_path']
    os.makedirs(db_folder, exist_ok=True)

    init_anime_db_storage(db_folder)
    init_mal_auth(
        config['ApiKey']['mal'],
        config['ApiKey'].get('redirect_uri', None),
        'https://myanimelist.net/v1/oauth2/authorize',
        'https://myanimelist.net/v1/oauth2/token'
    )
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)

    # Register blueprints
    app.register_blueprint(provider_bp)
    app.register_blueprint(mal_bp)
    app.register_blueprint(main_bp)

    # Add config values to app.config
    app.config['DB_FOLDER'] = db_folder
    app.config['CLIENT_ID'] = config['ApiKey']['mal']
    app.config['REDIRECT_URI'] = config['ApiKey'].get('redirect_uri', None)
    app.config['AUTH_URL'] = 'https://myanimelist.net/v1/oauth2/authorize'
    app.config['TOKEN_URL'] = 'https://myanimelist.net/v1/oauth2/token'

    return app

app: Flask = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=12345)