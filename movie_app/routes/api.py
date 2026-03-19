from flask import Blueprint, request, jsonify, session
from database import get_db
from models.recommender import search_movies, get_mood_movies, get_similar_movies

api_bp = Blueprint('api', __name__)


@api_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'results': [], 'message': 'No query provided'})

    db = get_db()

    if 'user_id' in session:
        db.execute('INSERT INTO search_history (user_id, query) VALUES (?, ?)',
                   (session['user_id'], query))
        db.commit()

    results = search_movies(db, query)
    return jsonify({'results': [dict(r) for r in results], 'count': len(results)})


@api_bp.route('/recommend')
def recommend():
    mood = request.args.get('mood', '').strip().lower()
    if not mood:
        return jsonify({'results': [], 'message': 'No mood provided'})

    db = get_db()

    if 'user_id' in session:
        db.execute('INSERT INTO user_mood (user_id, mood) VALUES (?, ?)',
                   (session['user_id'], mood))
        db.commit()

    movies = get_mood_movies(db, mood)
    return jsonify({'results': [dict(m) for m in movies], 'mood': mood})


@api_bp.route('/movie/<int:movie_id>')
def movie(movie_id):
    db = get_db()
    movie = db.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    if 'user_id' in session:
        db.execute('INSERT INTO user_history (user_id, movie_id, action) VALUES (?, ?, ?)',
                   (session['user_id'], movie_id, 'view'))
        db.commit()

    similar = get_similar_movies(db, movie_id)
    return jsonify({
        'movie': dict(movie),
        'similar': [dict(m) for m in similar]
    })


@api_bp.route('/trending')
def trending():
    db = get_db()
    from models.recommender import get_trending
    movies = get_trending(db)
    return jsonify({'results': [dict(m) for m in movies]})


@api_bp.route('/set-mood', methods=['POST'])
def set_mood():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    mood = data.get('mood', '').strip().lower()

    valid_moods = ['happy', 'sad', 'action', 'romantic', 'thriller', 'horror', 'drama']
    if mood not in valid_moods:
        return jsonify({'error': 'Invalid mood'}), 400

    db = get_db()
    db.execute('INSERT INTO user_mood (user_id, mood) VALUES (?, ?)',
               (session['user_id'], mood))
    db.commit()

    movies = get_mood_movies(db, mood)
    return jsonify({'success': True, 'mood': mood, 'results': [dict(m) for m in movies]})


@api_bp.route('/history')
def history():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    db = get_db()
    history = db.execute('''
        SELECT m.id, m.title, m.poster_url, m.imdb_rating, h.timestamp
        FROM user_history h
        JOIN movies m ON h.movie_id = m.id
        WHERE h.user_id = ?
        ORDER BY h.timestamp DESC LIMIT 20
    ''', (session['user_id'],)).fetchall()

    return jsonify({'history': [dict(h) for h in history]})
