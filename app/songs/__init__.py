from flask import Blueprint

songs_bp = Blueprint('songs', __name__)

from app.songs import routes