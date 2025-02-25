from flask import request, jsonify
from app.manager import manage
from app.routes import songs_bp


@songs_bp.route("/add", methods=["POST"])
def add_track():
    file = request.files.get('file')
    artist_name = request.form.get('artist_name')
    track_name = request.form.get('track_name')

    try:
        response, status_code = manage.add_track(file, artist_name, track_name)
        return response, status_code
    finally:
        if file:
            file.close()

@songs_bp.route("/remove", methods=["DELETE"])
def remove_track():
    track_name = request.form.get('track_name')
    response, status_code = manage.remove_track(track_name)
    return response, status_code

@songs_bp.route("/list", methods=["GET"])
def list_tracks():
    response, status_code = manage.list_tracks()
    return response, status_code

@songs_bp.route("/empty", methods=["DELETE"])
def empty_table():
    response, status_code = manage.empty_table()
    return response, status_code
