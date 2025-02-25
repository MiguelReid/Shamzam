import base64
from io import BytesIO
import requests
from flask import jsonify, send_file
from database.db import db

#AUDD_API_KEY = os.getenv('AUDD_API_KEY')
AUDD_API_KEY = 'test'

def add_track(file, artist_name, track_name):
    if not file or not artist_name or not track_name:
        return "File, artist and track name required", 400

    file_data = file.read()
    encoded_file = base64.b64encode(file_data)
    db.add_track(track_name, artist_name, encoded_file)
    file.close()
    return "Track added successfully", 201

def remove_track(track_name):
    if not track_name:
        return "Track name required", 400
    if not db.track_exists(track_name):
        return "Track not found", 404
    db.remove_track(track_name)
    return "Track removed", 200

def list_tracks():
    tracks = db.list_tracks()
    return jsonify(tracks), 200

def empty_table():
    db.empty_table()
    return "Table emptied", 200

def convert_fragment(file, track_name):
    if not file or not track_name:
        return "File and track name required", 400

    if db.track_exists(track_name):
        file_data = db.get_file_data(track_name)

        if not file_data:
            return "File not found in database", 404

        response = requests.post(
            'https://api.audd.io/',
            data={'api_token': AUDD_API_KEY, 'return': 'apple_music,spotify'},
            files={'file': file}
        )
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                db.update_track(track_name)
                decoded_file = base64.b64decode(file_data)
                memory_file = BytesIO(decoded_file)
                memory_file.seek(0)
                return send_file(memory_file, mimetype='audio/wav', as_attachment=False), 201
            else:
                return "Error from external service", 400
        else:
            return f"Error from audd.io: ", response.status_code
    else:
        return "Full song not found", 404