from flask import Blueprint, render_template, session, redirect, url_for, request
from database import get_db
from models.recommender import get_trending, get_top_rated, get_recommendations_for_user, get_mood_movies

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    db = get_db()
    trending = get_trending(db)
    top_rated = get_top_rated(db)

    recommended = []
    mood_movies = []
    last_mood = None

    if 'user_id' in session:
        user_id = session['user_id']
        recommended = get_recommendations_for_user(db, user_id)

        # Get last mood
        mood_row = db.execute(
            'SELECT mood FROM user_mood WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1',
            (user_id,)
        ).fetchone()
        if mood_row:
            last_mood = mood_row['mood']
            mood_movies = get_mood_movies(db, last_mood)

    return render_template('index.html',
                           trending=trending,
                           top_rated=top_rated,
                           recommended=recommended,
                           mood_movies=mood_movies,
                           last_mood=last_mood)


@main_bp.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    db = get_db()
    movie = db.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()

    if not movie:
        return redirect(url_for('main.index'))

    # Log view in history
    if 'user_id' in session:
        db.execute(
            'INSERT INTO user_history (user_id, movie_id, action) VALUES (?, ?, ?)',
            (session['user_id'], movie_id, 'view')
        )
        db.commit()

    # Get similar movies
    from models.recommender import get_similar_movies
    similar = get_similar_movies(db, movie_id)

    # Parse cast
    cast_list = []
    if movie['cast']:
        for item in movie['cast'].split('|'):
            parts = item.split(' as ')
            if len(parts) == 2:
                cast_list.append({'actor': parts[0].strip(), 'character': parts[1].strip()})

    return render_template('movie_detail.html', movie=movie, similar=similar, cast_list=cast_list)


@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    db = get_db()

    results = []
    if query:
        # Log search if logged in
        if 'user_id' in session:
            db.execute(
                'INSERT INTO search_history (user_id, query) VALUES (?, ?)',
                (session['user_id'], query)
            )
            db.commit()

        from models.recommender import search_movies
        results = search_movies(db, query)

    return render_template('search.html', results=results, query=query)


@main_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db = get_db()
    user_id = session['user_id']

    history = db.execute('''
        SELECT m.*, h.timestamp FROM user_history h
        JOIN movies m ON h.movie_id = m.id
        WHERE h.user_id = ?
        ORDER BY h.timestamp DESC LIMIT 10
    ''', (user_id,)).fetchall()

    search_hist = db.execute('''
        SELECT query, timestamp FROM search_history
        WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10
    ''', (user_id,)).fetchall()

    return render_template('profile.html', history=history, search_history=search_hist)
