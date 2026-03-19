from flask import Flask
from config import Config
from database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    with app.app_context():
        init_db()

    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
