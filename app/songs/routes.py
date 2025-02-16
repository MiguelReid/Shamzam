import os

from flask import request, jsonify
from app.songs import songs_bp
from app.database import db


# python
@songs_bp.route("/add", methods=["POST"])
def add_track():
    file = request.files.get('file')
    artist_name = request.form.get('artist_name')
    if not file:
        return "File required", 400
    if not artist_name:
        return "Artist name required", 400

    file_path = os.path.join('resources', file.filename)
    db.add_track(file.filename, artist_name, file_path)
    file.close()
    return "File added to database", 201


@songs_bp.route("/remove", methods=["DELETE"])
def remove_track():
    file = request.files.get('file')
    if not file:
        return "No file provided", 400

    if not db.track_exists(file.filename):
        return "Track not found", 404

    db.remove_track(file.filename)
    return "Track removed", 200


@songs_bp.route("/list", methods=["GET"])
def list_tracks():
    tracks = db.list_tracks()
    print("tracks", tracks)
    return jsonify(tracks), 200


@songs_bp.route("/empty", methods=["DELETE"])
def empty_table():
    db.empty_table()
    return "Table emptied", 200
