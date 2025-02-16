import os
import requests
from flask import request, jsonify
from app.fragments import fragments_bp
from app.database import db

AUDD_API_KEY = os.getenv('AUDD_API_KEY')

@fragments_bp.route("/convert", methods=["POST"])
def convert_fragment():
    file = request.files.get('file')
    if not file:
        return "No file provided", 400

    full_song_name = file.filename
    full_song_path = os.path.join('resources', full_song_name)

    if db.track_exists(full_song_name):
        response = requests.post(
            'https://api.audd.io/',
            data={'api_token': AUDD_API_KEY, 'return': 'apple_music,spotify'},
            files={'file': file}
        )
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                track_info = data['result']
                track_name = track_info['title']
                artist_name = track_info['artist']
                db.add_track(track_name, artist_name, full_song_path)
                return jsonify({"track_name": track_name, "artist_name": artist_name}), 201
            else:
                error_message = data['error'].get('message', 'Unknown error')
                return error_message, 400
        else:
            return f"Error from audd.io: ", response.status_code
    else:
        return "Full song not found", 404
