import sqlite3

class Repository:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    # Create tracks table
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                track_id INTEGER PRIMARY KEY AUTOINCREMENT,
                track_name TEXT NOT NULL,
                artist_name TEXT,
                file_data BLOB NOT NULL,
                UNIQUE(track_name, artist_name)
            )
        ''')
        self.connection.commit()

    # Add track to tracks table
    def add_track(self, track_name, artist_name, file_data):
        self.cursor.execute('INSERT INTO tracks (track_name, artist_name, file_data) VALUES (?, ?, ?)',
                            (track_name, artist_name, file_data,))
        self.connection.commit()

    # Remove track from tracks table by track_name
    def remove_track(self, track_name):
        self.cursor.execute('DELETE FROM tracks WHERE track_name = ?', (track_name,))
        self.connection.commit()

    # List all tracks from tracks table
    def list_tracks(self):
        self.cursor.execute('SELECT track_name, artist_name FROM tracks')
        return self.cursor.fetchall()

    # Check if track exists in tracks table
    def track_exists(self, track_name):
        self.cursor.execute('SELECT 1 FROM tracks WHERE track_name LIKE ?', (f'%{track_name}%',))
        return self.cursor.fetchone() is not None

    # Get file to return to user
    def get_file_data(self, track_name):
        self.cursor.execute('SELECT file_data FROM tracks WHERE track_name = ?', (track_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    # Empty tracks table
    def empty_table(self):
        self.cursor.execute('DELETE FROM tracks')
        self.connection.commit()

    def close(self):
        self.connection.close()