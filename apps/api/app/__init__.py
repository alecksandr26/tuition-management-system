from flask import Flask
from app.config import Config


def create_app(config_class = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here


    # Register blueprints here

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the backend setup</h1>'
    
    return app






