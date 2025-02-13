from flask import Flask

from app.songs import songs_bp
from app.fragments import fragments_bp

def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app

def register_blueprints(app):
    app.register_blueprint(songs_bp, url_prefix='/songs')
    app.register_blueprint(fragments_bp, url_prefix='/fragments')
