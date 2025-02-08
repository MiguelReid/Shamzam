from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.songs import songs_bp
    from app.fragments import fragments_bp

    app.register_blueprint(songs_bp, url_prefix='/songs')
    app.register_blueprint(fragments_bp, url_prefix='/fragments')

    return app