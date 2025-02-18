import os
import unittest
from app import create_app
from app.repository import Repository


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

    def test_add_track(self):
        with open(self.test_track_path, 'rb') as file:
            data = {
                'file': (file, 'test_track.wav'),
                'artist_name': 'Test Artist'
            }
            response = self.client.post('/songs/add', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 201)
            track = self.repo.track_exists('test_track.wav')
            self.assertIsNotNone(track)

    def test_remove_track(self):
        with open(self.test_track_path, 'rb') as file:
            data = {
                'file': (file, 'test_track.wav'),
                'artist_name': 'Test Artist'
            }
            self.client.post('/songs/add', data=data, content_type='multipart/form-data')

        with open(self.test_track_path, 'rb') as file2:
            data = {
                'file': (file2, 'test_track.wav')
            }
            response = self.client.delete('/songs/remove', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            track = self.repo.track_exists('test_track.wav')
            self.assertFalse(track)

    def test_list_tracks(self):
        with open(self.test_track_path, 'rb') as file:
            data = {
                'file': (file, 'test_track.wav'),
                'artist_name': 'Test Artist'
            }
            self.client.post('/songs/add', data=data, content_type='multipart/form-data')
            response = self.client.get('/songs/list')
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(len(response.get_json()), 0)

    def test_convert_fragment_to_track(self):
        # Error 901 is returned when the API key is invalid
        with open(self.test_track_path, 'rb') as file:
            data = {
                'file': (file, 'test_track.wav'),
                'artist_name': 'Test Artist',
            }
            self.client.post('/songs/add', data=data, content_type='multipart/form-data')

            with open(self.test_fragment_path, 'rb') as fragment_file:
                data = {
                    'file': (fragment_file, 'test_track.wav')
                }
                response = self.client.post('/fragments/convert', data=data, content_type='multipart/form-data')
                self.assertEqual(response.status_code, 201)
            # TODO Check if the track name is the one expected

    def test_add_track_no_file(self):
        response = self.client.post('/songs/add', data={}, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_remove_nonexistent_track(self):
        with open(self.test_track_path, 'rb') as file:
            data = {
                'file': (file, 'non_existent_track.wav')
            }
            response = self.client.delete('/songs/remove', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 404)

    def test_list_tracks_empty(self):
        response = self.client.get('/songs/list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])


if __name__ == '__main__':
    unittest.main()
