from flask import Blueprint

fragments_bp = Blueprint('fragments', __name__)
songs_bp = Blueprint('songs', __name__)

from app.routes import fragments
from app.routes import songs



