import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Task
from routes import list_routes  # Import the function that registers routes

app = Flask(__name__)

# Specify absolute path for the SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "tasks.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Call list_routes to register the routes
list_routes(app)  # Pass app into the function to register the routes

# Database initialization and Flask app start
if __name__ == '__main__':
    try:
        with app.app_context():
            print("Creating the database...")
            db.create_all()  # Create tables
            
            # Check if the database file exists
            if os.path.exists(os.path.join(BASE_DIR, 'tasks.db')):
                print("Database file exists!")
            else:
                print("Database file does NOT exist.")
            print("Database and tables created.")
    except Exception as e:
        print(f"Error creating database: {e}")
    
    # Start the Flask app
    app.run(debug=True)  # Running in debug mode during development
