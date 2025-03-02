import gc
import os
import unittest
from io import BytesIO

from app import create_app
from database.repository import Repository


class TestMusicCatalog(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.repo = Repository(db_name=':memory:')
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_track_path = os.path.join(self.test_dir, 'test_track.wav')
        self.test_fragment_path = os.path.join(self.test_dir, 'test_fragment.wav')

    def tearDown(self):
        self.client.delete('/songs/empty')
        self.repo.close()
        gc.collect()

    # Test adding a track and listing all tracks
    def test_adding_and_listing(self):
        with open(self.test_track_path, 'rb') as file:
            file_content = file.read()

        data = {
            'file': (BytesIO(file_content), 'test_track.wav'),
            'track_name': 'test_track.wav',
            'artist_name': 'test_artist'
        }
        response = self.client.post('/songs/add', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        track = self.repo.track_exists('test_track.wav')
        self.assertIsNotNone(track)

        response2 = self.client.get('/songs/list')
        self.assertEqual(response2.status_code, 200)
        self.assertNotEqual(len(response2.get_json()), 0)

    # Test removing a track
    def test_remove_track(self):
        with open(self.test_track_path, 'rb') as file:
            file_content = file.read()

        data = {
            'file': (BytesIO(file_content), 'test_track.wav'),
            'track_name': 'test_track.wav',
            'artist_name': 'test_artist'
        }
        self.client.post('/songs/add', data=data, content_type='multipart/form-data')

        data2 = {
            'track_name': 'test_track.wav'
        }
        response = self.client.delete('/songs/remove', data=data2, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        track = self.repo.track_exists('test_track.wav')
        self.assertFalse(track)

    # Test converting a fragment
    def test_convert_fragment(self):
        # Error 901 is returned when the API key is invalid
        with open(self.test_track_path, 'rb') as file:
            file_content = file.read()
            
            data = {
                'file': (BytesIO(file_content), 'test_track.wav'),
                'track_name': 'test_track.wav',
                'artist_name': 'test_artist'
            }
            self.client.post('/songs/add', data=data, content_type='multipart/form-data')
    
            with open(self.test_fragment_path, 'rb') as fragment_file:
                fragment_content = fragment_file.read()
                data = {
                    'file': (BytesIO(fragment_content), 'test_track.wav'),
                    'track_name': 'test_track.wav',
                    'artist_name': 'test_artist'
                }
                response = self.client.post('/fragments/convert', data=data, content_type='multipart/form-data')
                self.assertEqual(response.status_code, 201)

    # Test adding a track with missing metadata
    def test_add_track_no_file(self):
        response = self.client.post('/songs/add', data={}, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    # Test removing a non-existent track
    def test_remove_nonexistent_track(self):
        data = {
            'track_name': 'non_existing_track.wav'
        }
        response = self.client.delete('/songs/remove', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 404)

    # Test only accepting .wav files for tracks
    def test_file_type_validation(self):
        audio_formats = [('tests/test_track.wav', True),
                         ('tests/test_app.py', False)]

        for file_path, should_accept in audio_formats:
            with open(file_path, 'rb') as file:
                file_content = file.read()
                data = {
                    'file': (BytesIO(file_content), os.path.basename(file_path)),
                    'track_name': 'test_validation',
                    'artist_name': 'test_artist'
                }
                response = self.client.post('/songs/add', data=data, content_type='multipart/form-data')
                expected_code = 201 if should_accept else 400
                self.assertEqual(response.status_code, expected_code, f"Failed for {file_path}")

    # Test emptying the database
    def test_empty_database(self):
        # Add a track first
        with open(self.test_track_path, 'rb') as file:
            file_content = file.read()
            data = {
                'file': (BytesIO(file_content), 'test_track.wav'),
                'track_name': 'test_track',
                'artist_name': 'test_artist'
            }
            self.client.post('/songs/add', data=data, content_type='multipart/form-data')

        response = self.client.delete('/songs/empty')
        self.assertEqual(response.status_code, 200)

        # Verify database is empty
        response = self.client.get('/songs/list')
        self.assertEqual(len(response.get_json()), 0)

if __name__ == '__main__':
    unittest.main()
