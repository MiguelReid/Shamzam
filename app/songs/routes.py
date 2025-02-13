import os

from flask import request, jsonify
from app.songs import songs_bp
from app.database import db


@songs_bp.route("/add", methods=["POST"])
def add_track():
    file = request.files.get('file')
    if not file:
        return "No file provided", 400

    file_path = os.path.join('resources', file.filename)
    file.save(file_path)
    return "File added to resources folder", 201


@songs_bp.route("/remove", methods=["POST"])
def remove_track():
    file = request.files.get('file')
    if not file:
        return "No file provided", 400

    file_path = os.path.join('resources', file.filename)
    db.remove_track(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
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
