
# To connect to the postgres and migrtions for the db 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initailize the Migrates
migrate = Migrate()

# Import the whole configurations from the auth
from app.auth import *


