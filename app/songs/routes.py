from flask import request, jsonify
from app.songs import songs_bp
from app.database import db

@songs_bp.route("/add", methods=["POST"])
def add_track():
    data = request.get_json()
    name = data.get('name')
    file_path = data.get('file_path')
    if not name or not file_path:
        return "Invalid data", 400
    db.add_track(name, file_path)
    return "Track added", 201

@songs_bp.route("/remove/<track_id>", methods=["DELETE"])
def remove_track(track_id):
    db.remove_track(track_id)
    return "Track removed", 200

@songs_bp.route("/list", methods=["GET"])
def list_tracks():
    tracks = db.list_tracks()
    print("tracks", tracks)
    return jsonify(tracks), 200