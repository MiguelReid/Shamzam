import base64
from io import BytesIO
import requests
from flask import jsonify, send_file
from database.db import db

AUDD_API_KEY = 'test'

def add_track(file, artist_name, track_name):
    # Check if the required parameters are present
    if not file or not artist_name or not track_name:
        return "File, artist and track name required", 400

    # Check if the file is a .wav file
    if not file.filename.lower().endswith('.wav'):
        return "Only .wav files are accepted", 400

    # Base64 encoding
    file_data = file.read()
    encoded_file = base64.b64encode(file_data)
    db.add_track(track_name, artist_name, encoded_file)
    file.close()
    return "Track added successfully", 201

def remove_track(track_name):
    # Check if the track name is present
    if not track_name:
        return "Track name required", 400
    # Check if track exists
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
    # Check if the required parameters are present
    if not file or not track_name:
        return "File and track name required", 400

    # Check if the file is a .wav file
    if not file.filename.lower().endswith('.wav'):
        return "Only .wav files are accepted", 400

    try:
        # Check if the track exists
        if db.track_exists(track_name):
            file_data = db.get_file_data(track_name)

            if not file_data:
                return "File not found in database", 404

            # Read the file content before passing to requests
            file_content = file.read()

            response = requests.post(
                'https://api.audd.io/',
                data={'api_token': AUDD_API_KEY, 'return': 'apple_music,spotify'},
                files={'file': ('audio.wav', file_content, 'audio/wav')}
            )

            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    # Return the base64-encoded file data as JSON
                    return jsonify({"encoded_file": file_data.decode('utf-8')}), 201
                else:
                    return "Error from external service", 400
            else:
                return f"Error from audd.io: ", 500
        else:
            return "Full song not found", 404
    finally:
        file.close()