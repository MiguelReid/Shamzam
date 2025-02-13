import sqlite3

class Repository:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                track_id INTEGER PRIMARY KEY AUTOINCREMENT,
                track_name TEXT NOT NULL,
                artist_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                UNIQUE(track_name, artist_name)
            )
        ''')
        self.connection.commit()

    def add_track(self, track_name, artist_name, file_path):
        self.cursor.execute('INSERT INTO tracks (track_name, artist_name, file_path) VALUES (?, ?, ?)', (track_name, artist_name, file_path))
        self.connection.commit()

    def remove_track(self, file_path):
        self.cursor.execute('DELETE FROM tracks WHERE file_path = ?', (file_path,))
        self.connection.commit()

    def list_tracks(self):
        self.cursor.execute('SELECT * FROM tracks')
        return self.cursor.fetchall()

    def get_track(self, track_id):
        self.cursor.execute('SELECT * FROM tracks WHERE track_id = ?', (track_id,))
        return self.cursor.fetchone()

    def empty_table(self):
        self.cursor.execute('DELETE FROM tracks')
        self.connection.commit()

    def close(self):
        self.connection.close()