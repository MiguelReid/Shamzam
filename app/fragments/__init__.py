from flask import Blueprint

fragments_bp = Blueprint('fragments', __name__)

from app.fragments import routes