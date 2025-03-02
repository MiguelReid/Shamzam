from flask import request
from app.manager import manage
from app.routes import fragments_bp

@fragments_bp.route("/convert", methods=["POST"])
def convert_fragment():
    # Request file and track name
    file = request.files.get('file')
    track_name = request.form.get('track_name')

    try:
        result, status_code = manage.convert_fragment(file, track_name)
        return result, status_code
    finally:
        file.close()
