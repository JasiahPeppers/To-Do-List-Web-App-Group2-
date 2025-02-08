import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from backend.models import db, Task
from backend.routes import list_routes  # Import your Blueprint

app = Flask(__name__)

# Specify absolute path for the SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Register the routes as a Blueprint
app.register_blueprint(list_routes)

# Database initialization and Flask app start
if __name__ == '__main__':
    try:
        with app.app_context():
            print("Creating the database...")
            db.create_all()  # Create tables
            print("Database and tables created.")
    except Exception as e:
        print(f"Error creating database: {e}")
    
    # Start the Flask app
    app.run(debug=True)  # You might want to run it in debug mode during development
