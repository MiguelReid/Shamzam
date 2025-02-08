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

    response = requests.post(
        'https://api.audd.io/',
        data={'api_token': AUDD_API_KEY, 'return': 'apple_music,spotify'},
        files={'file': file}
    )

    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            track_info = data['result']
            file_path = save_file(file)
            db.add_track(track_info['title'], track_info['artist'], file_path)
            return jsonify(track_info), 201
        else:
            return data['error']['message'], 400
    else:
        return "Error connecting to audd.io", 500


def save_file(file):
    file_path = f"resources/full-{file.filename}"
    file.save(file_path)
    return file_path