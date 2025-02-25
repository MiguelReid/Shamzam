from flask import Flask

from app.routes import fragments_bp, songs_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(songs_bp, url_prefix='/songs')
    app.register_blueprint(fragments_bp, url_prefix='/fragments')
    return app
