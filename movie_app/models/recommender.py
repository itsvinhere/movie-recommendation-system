from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


MOOD_GENRE_MAP = {
    'happy': ['Comedy', 'Animation', 'Adventure', 'Family', 'Music'],
    'sad': ['Drama', 'Biography', 'Romance'],
    'action': ['Action', 'Adventure', 'Sci-Fi', 'War'],
    'romantic': ['Romance', 'Drama', 'Comedy'],
    'thriller': ['Thriller', 'Mystery', 'Crime', 'Horror'],
    'horror': ['Horror', 'Thriller', 'Mystery'],
    'drama': ['Drama', 'Biography', 'History'],
}


def _rows_to_list(rows):
    return [dict(r) for r in rows] if rows else []


def get_trending(db, limit=10):
    rows = db.execute(
        'SELECT * FROM movies ORDER BY imdb_rating DESC LIMIT ?', (limit,)
    ).fetchall()
    return rows


def get_top_rated(db, limit=10):
    rows = db.execute(
        'SELECT * FROM movies ORDER BY imdb_rating DESC, release_year DESC LIMIT ?', (limit,)
    ).fetchall()
    return rows


def get_mood_movies(db, mood, limit=8):
    mood = mood.lower()
    genres = MOOD_GENRE_MAP.get(mood, [])

    if not genres:
        return db.execute('SELECT * FROM movies ORDER BY RANDOM() LIMIT ?', (limit,)).fetchall()

    # Search by mood_tags first
    rows = db.execute(
        "SELECT * FROM movies WHERE LOWER(mood_tags) LIKE ? ORDER BY imdb_rating DESC LIMIT ?",
        (f'%{mood}%', limit)
    ).fetchall()

    if len(rows) < limit:
        # Fallback to genre matching
        conditions = ' OR '.join(["LOWER(genre) LIKE ?" for _ in genres])
        params = [f'%{g.lower()}%' for g in genres] + [limit]
        extra = db.execute(
            f"SELECT * FROM movies WHERE {conditions} ORDER BY imdb_rating DESC LIMIT ?",
            params
        ).fetchall()
        seen_ids = {r['id'] for r in rows}
        rows = list(rows) + [r for r in extra if r['id'] not in seen_ids]
        rows = rows[:limit]

    return rows


def search_movies(db, query, limit=12):
    all_movies = db.execute('SELECT * FROM movies').fetchall()
    if not all_movies:
        return []

    movies_list = [dict(m) for m in all_movies]

    # Build corpus for TF-IDF
    corpus = []
    for m in movies_list:
        text = f"{m['title']} {m['genre']} {m['overview']} {m.get('cast', '')}"
        corpus.append(text.lower())

    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(corpus)
        query_vec = vectorizer.transform([query.lower()])
        scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

        # Get top matches above threshold
        top_indices = np.argsort(scores)[::-1]
        results = []
        for idx in top_indices:
            if scores[idx] > 0.01:
                results.append(all_movies[idx])
            if len(results) >= limit:
                break

        # If nothing found, do simple text search
        if not results:
            results = db.execute(
                "SELECT * FROM movies WHERE LOWER(title) LIKE ? OR LOWER(genre) LIKE ? LIMIT ?",
                (f'%{query.lower()}%', f'%{query.lower()}%', limit)
            ).fetchall()

        return results
    except Exception:
        # Fallback
        return db.execute(
            "SELECT * FROM movies WHERE LOWER(title) LIKE ? LIMIT ?",
            (f'%{query.lower()}%', limit)
        ).fetchall()


def get_similar_movies(db, movie_id, limit=6):
    target = db.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    if not target:
        return []

    all_movies = db.execute('SELECT * FROM movies WHERE id != ?', (movie_id,)).fetchall()
    if not all_movies:
        return []

    target_dict = dict(target)
    target_text = f"{target_dict.get('genre','')} {target_dict.get('overview','')} {target_dict.get('mood_tags','')}"
    corpus = [f"{dict(m).get('genre','')} {dict(m).get('overview','')} {dict(m).get('mood_tags','')}" for m in all_movies]
    corpus.insert(0, target_text)

    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=3000)
        tfidf_matrix = vectorizer.fit_transform(corpus)
        target_vec = tfidf_matrix[0]
        other_vecs = tfidf_matrix[1:]
        scores = cosine_similarity(target_vec, other_vecs).flatten()
        top_indices = np.argsort(scores)[::-1][:limit]
        return [all_movies[i] for i in top_indices]
    except Exception:
        return db.execute(
            "SELECT * FROM movies WHERE id != ? ORDER BY imdb_rating DESC LIMIT ?",
            (movie_id, limit)
        ).fetchall()


def get_recommendations_for_user(db, user_id, limit=8):
    # Get user's watch history
    history = db.execute('''
        SELECT movie_id FROM user_history
        WHERE user_id = ?
        ORDER BY timestamp DESC LIMIT 5
    ''', (user_id,)).fetchall()

    if not history:
        return get_trending(db, limit)

    watched_ids = [h['movie_id'] for h in history]
    all_watched = db.execute(
        f"SELECT * FROM movies WHERE id IN ({','.join(['?']*len(watched_ids))})",
        watched_ids
    ).fetchall()

    if not all_watched:
        return get_trending(db, limit)

    # Get genres from watched movies
    genres = set()
    for m in all_watched:
        if m['genre']:
            for g in m['genre'].split('|'):
                genres.add(g.strip())

    if not genres:
        return get_trending(db, limit)

    conditions = ' OR '.join(["LOWER(genre) LIKE ?" for _ in genres])
    exclude = ','.join(['?'] * len(watched_ids))
    params = [f'%{g.lower()}%' for g in genres] + watched_ids + [limit]
    results = db.execute(
        f"SELECT * FROM movies WHERE ({conditions}) AND id NOT IN ({exclude}) ORDER BY imdb_rating DESC LIMIT ?",
        params
    ).fetchall()

    if len(results) < limit:
        more = db.execute(
            f"SELECT * FROM movies WHERE id NOT IN ({exclude}) ORDER BY imdb_rating DESC LIMIT ?",
            watched_ids + [limit]
        ).fetchall()
        seen = {r['id'] for r in results}
        results = list(results) + [m for m in more if m['id'] not in seen]
        results = results[:limit]

    return results
