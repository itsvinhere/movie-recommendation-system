from flask import Blueprint, request, session, redirect, url_for, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db
import sqlite3

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('main.index'))
        return render_template('auth.html', mode='login')

    data = request.get_json() or request.form
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    if user is None or not check_password_hash(user['password_hash'], password):
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    session.clear()
    session['user_id'] = user['id']
    session['username'] = user['username']
    return jsonify({'success': True, 'message': 'Login successful', 'username': user['username']})


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('main.index'))
        return render_template('auth.html', mode='signup')

    data = request.get_json() or request.form
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400

    db = get_db()
    try:
        db.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, generate_password_hash(password))
        )
        db.commit()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'success': True, 'message': 'Account created successfully', 'username': username})
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            return jsonify({'success': False, 'message': 'Username already taken'}), 409
        return jsonify({'success': False, 'message': 'Email already registered'}), 409


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
