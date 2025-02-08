
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from backend.models import db, Task
from routes import list_routes


app = Flask(__name__)

# Specify absolute path for the SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
# Import routes.py (which is in the backend folder)
from backend import routes 
# Enable Cross-Origin Resource Sharing
CORS(app)

# Add the routes
list_routes(app)

# Database initialization
if __name__ == '__main__':
    try:
        with app.app_context():
            print("Creating the database...")
            db.create_all()  # Create tables
            print("Database and tables created.")
    except Exception as e:
        print(f"Error creating database: {e}")
    
    # Start the Flask app
    app.run()


# This imports everything, points to where the DB is, starts or creates the database 
# when the Flask program is started, and is the starting point of the backend.
