# 🎬 CineVault — Movie Recommendation Web App

A full-stack Netflix-style movie recommendation application built with Flask, SQLite, and Scikit-learn.

## Features

- **Authentication** — Signup, Login, Session management
- **Netflix-style UI** — Dark theme, movie cards, hero banner
- **Mood-based Recommendations** — Happy, Sad, Action, Romantic, Thriller, Horror, Drama
- **Search** — TF-IDF + Cosine Similarity content-based search
- **Movie Details** — Poster, cast, IMDb rating, trailer embed, overview
- **User History** — Tracks watched movies and searches
- **Personalized Recommendations** — Based on watch history

## Project Structure

```
movie_app/
├── app.py                  # App factory
├── config.py               # Configuration
├── database.py             # DB init & helpers
├── requirements.txt
├── data/
│   ├── movies.csv          # Movie dataset
│   └── movieapp.db         # SQLite DB (auto-created)
├── models/
│   └── recommender.py      # TF-IDF recommendation engine
├── routes/
│   ├── auth.py             # /login /signup /logout
│   ├── main.py             # / /movie/<id> /search /profile
│   └── api.py              # /api/* endpoints
├── static/
│   ├── css/style.css
│   └── js/main.js
└── templates/
    ├── base.html
    ├── index.html
    ├── movie_detail.html
    ├── auth.html
    ├── search.html
    ├── profile.html
    └── partials/
        └── movie_card.html
```

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser at
http://localhost:5000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/login` | User login |
| GET/POST | `/signup` | User signup |
| GET | `/logout` | Logout |
| GET | `/search?q=` | Search movies |
| GET | `/movie/<id>` | Movie detail page |
| GET | `/profile` | User profile |
| GET | `/api/recommend?mood=` | Mood-based recommendations |
| GET | `/api/search?q=` | JSON search results |
| GET | `/api/movie/<id>` | JSON movie details |
| GET | `/api/trending` | Trending movies |
| POST | `/api/set-mood` | Set user mood |
| GET | `/api/history` | User watch history |

## Recommendation Engine

- **Content-based filtering**: TF-IDF vectorization on title, genre, overview, and cast
- **Cosine similarity**: Finds movies most similar to search query or watched films
- **Mood-based filtering**: Maps moods to genres and mood_tags in dataset
- **History-based**: Recommends movies based on user's watch history genres

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **ML**: Scikit-learn (TF-IDF, Cosine Similarity)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Vanilla JS
- **Auth**: Werkzeug password hashing + Flask sessions
