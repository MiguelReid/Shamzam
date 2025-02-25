import base64
from io import BytesIO
import requests
from flask import request, send_file
from app.database import db
from app.fragments import fragments_bp

#AUDD_API_KEY = os.getenv('AUDD_API_KEY')
AUDD_API_KEY = 'test'

@fragments_bp.route("/convert", methods=["POST"])
def convert_fragment():
    file = request.files.get('file')
    if not file:
        return "No file provided", 400

    try:
        track_name = request.form.get('track_name')

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

    finally:
        file.close()
