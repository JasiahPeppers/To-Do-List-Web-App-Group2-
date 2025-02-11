from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db

# Initialize the Flask app
app = Flask(__name__)

# Configure the app with the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Path to the database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask SQLAlchemy modification tracking

# Initialize extensions
db.init_app(app)  # Bind the db to the app
migrate = Migrate(app, db)  # Bind Flask-Migrate to the app

# Routes can be added here later (optional)
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)
