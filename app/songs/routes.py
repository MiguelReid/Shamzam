import os

from flask import request, jsonify
from app.songs import songs_bp
from app.database import db
import base64

# python
@songs_bp.route("/add", methods=["POST"])
def add_track():
    file = request.files.get('file')
    if not file:
        return "File required", 400

    file_data = file.read()
    encoded_file = base64.b64encode(file_data)

    track_name = request.form.get('track_name')

    db.add_track(track_name, encoded_file)
    file.close()
    return "File added to database", 201


@songs_bp.route("/remove", methods=["DELETE"])
def remove_track():
    track_name = request.form.get('track_name')

    if not db.track_exists(track_name):
        return "Track not found", 404

    db.remove_track(track_name)
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
