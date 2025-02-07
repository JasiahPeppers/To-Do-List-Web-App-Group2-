from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Task  # Import db and Task from models
from routes import list_routes
import os

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tasks.db')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database (using the db instance)
db.init_app(app)

# Allows cross communication
CORS(app)  


# From routes.py for all the route methods
list_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the table
        print("Database created successfully")
    app.run()

# This imports everything, points to where the DB is, starts or creates the database 
# when the Flask program is started, and is the starting point of the backend.
