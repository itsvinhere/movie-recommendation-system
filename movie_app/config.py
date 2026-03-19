import os
import secrets

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    DATABASE = os.path.join(os.path.dirname(__file__), 'data', 'movieapp.db')
    MOVIES_CSV = os.path.join(os.path.dirname(__file__), 'data', 'movies.csv')
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
