import os
import unittest
from app import create_app
from app.repository import Repository


class TestMusicCatalog(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.repo = Repository(db_name='database/shamzam_test.sqlite')
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_track_path = os.path.join(self.test_dir, 'test_track.mp3')
        self.test_fragment_path = os.path.join(self.test_dir, 'test_fragment.mp3')
        # Create dummy test files
        with open(self.test_track_path, 'wb') as f:
            f.write(b'Test track content')
        with open(self.test_fragment_path, 'wb') as f:
            f.write(b'Test fragment content')

    def tearDown(self):
        self.repo.close()
        # Clean up test files
        if os.path.exists(self.test_track_path):
            os.remove(self.test_track_path)
        if os.path.exists(self.test_fragment_path):
            os.remove(self.test_fragment_path)

    def test_add_track(self):
        data = {
            'file': (open(self.test_track_path, 'rb'), 'test_track.mp3')
        }
        response = self.client.post('/songs/add', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, '../resources/test_track.mp3')))

    # python
    def test_remove_track(self):
        with open(self.test_track_path, 'rb') as file:
            data = {
                'file': (file, 'test_track.mp3')
            }
            self.client.post('/songs/add', data=data, content_type='multipart/form-data')
            with open(self.test_track_path, 'rb') as file:
                data = {
                    'file': (file, 'test_track.mp3')
                }
                response = self.client.post('/songs/remove', data=data, content_type='multipart/form-data')
                self.assertEqual(response.status_code, 200)
                self.assertFalse(os.path.exists(os.path.join(self.test_dir, '../resources/test_track.mp3')))

    def test_list_tracks(self):
        data = {
            'file': (open(self.test_track_path, 'rb'), 'test_track.mp3')
        }
        self.client.post('/songs/add', data=data, content_type='multipart/form-data')
        response = self.client.get('/songs/list')
        self.assertEqual(response.status_code, 200)
        # TODO Test if there's an exact track in the response

    def test_convert_fragment_to_track(self):
        # Have to add a track first because it does not call the API
        # Unless the directory resources/song exists
        song = {
            'file': (open(self.test_track_path, 'rb'), 'test_fragment.mp3')
        }
        self.client.post('/songs/add', data=song, content_type='multipart/form-data')

        fragment = {
            'file': (open(self.test_fragment_path, 'rb'), 'test_fragment.mp3')
        }
        response = self.client.post('/fragments/convert', data=fragment, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        # TODO Check if the track name is the one expected

    def test_add_track_no_file(self):
        response = self.client.post('/songs/add', data={}, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_remove_nonexistent_track(self):
        response = self.client.delete('/songs/remove/nonexistent_track.mp3')
        self.assertEqual(response.status_code, 404)

    def test_list_tracks_empty(self):
        self.client.post('/songs/empty')
        response = self.client.get('/songs/list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])


if __name__ == '__main__':
    unittest.main()
