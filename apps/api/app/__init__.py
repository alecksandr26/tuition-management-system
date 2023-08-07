from flask import Flask
from app.config import Config

# For testing
import unittest

# For the commands
import click

# Import the extensions
from app.extensions import *

# Import the models
from app.models import *

def create_app(config_class = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    
    db.init_app(app)
    migrate.init_app(app)

    # Register blueprints here
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp) # Link the auth
    
    @app.cli.command("test")
    @click.option('--file', default = None, help = 'Path to a specific test file')
    def test(file):
        if file:
            tests = unittest.TestLoader().discover('test', pattern = file.split('/')[-1])
        else:
            tests = unittest.TestLoader().discover('test')
        unittest.TextTestRunner().run(tests)


    @app.cli.command("models")
    @click.argument("interact")
    def models_interact(interact):
        if interact == "create":
            db.create_all()
        elif interact == "drop":
            db.drop_all()

    
    return app






