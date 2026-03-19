import sqlite3
import csv
import os
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db_path = current_app.config['DATABASE']
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create tables
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            genre TEXT,
            overview TEXT,
            cast TEXT,
            imdb_rating REAL,
            poster_url TEXT,
            trailer_url TEXT,
            release_year INTEGER,
            mood_tags TEXT
        );

        CREATE TABLE IF NOT EXISTS user_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            action TEXT DEFAULT 'view',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (movie_id) REFERENCES movies (id)
        );

        CREATE TABLE IF NOT EXISTS user_mood (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mood TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            query TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')

    # Load movies from CSV if table is empty
    cursor.execute('SELECT COUNT(*) FROM movies')
    count = cursor.fetchone()[0]

    if count == 0:
        csv_path = current_app.config['MOVIES_CSV']
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cursor.execute('''
                        INSERT OR IGNORE INTO movies 
                        (id, title, genre, overview, cast, imdb_rating, poster_url, trailer_url, release_year, mood_tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        int(row['id']),
                        row['title'],
                        row['genre'],
                        row['overview'],
                        row['cast'],
                        float(row['imdb_rating']),
                        row['poster_url'],
                        row['trailer_url'],
                        int(row['release_year']),
                        row['mood_tags']
                    ))

    conn.commit()
    conn.close()
