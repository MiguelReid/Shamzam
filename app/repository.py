import sqlite3

class Repository:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    # Adding tracks will be done by admin, therefore user_added will be 0
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                track_id INTEGER PRIMARY KEY AUTOINCREMENT,
                track_name TEXT NOT NULL,
                artist_name TEXT,
                file_data BLOB NOT NULL,
                user_added INTEGER DEFAULT 0,
                UNIQUE(track_name, artist_name)
            )
        ''')
        self.connection.commit()

    def add_track(self, track_name, file_data):
        self.cursor.execute('INSERT INTO tracks (track_name, file_data) VALUES (?, ?)',
                            (track_name, file_data,))
        self.connection.commit()

    def remove_track(self, track_name):
        self.cursor.execute('DELETE FROM tracks WHERE track_name = ?', (track_name,))
        self.connection.commit()

    def list_tracks(self):
        self.cursor.execute('SELECT track_name, artist_name FROM tracks WHERE user_added = 1')
        return self.cursor.fetchall()

    def track_exists(self, track_name):
        self.cursor.execute('SELECT 1 FROM tracks WHERE track_name LIKE ?', (f'%{track_name}%',))
        return self.cursor.fetchone() is not None

    def update_track(self, new_artist_name, track_name):
        self.cursor.execute('''
            UPDATE tracks
            SET artist_name = ?, user_added = 1
            WHERE track_name = ?
        ''', (new_artist_name, track_name))
        self.connection.commit()

    def empty_table(self):
        self.cursor.execute('DELETE FROM tracks')
        self.connection.commit()

    def close(self):
        self.connection.close()