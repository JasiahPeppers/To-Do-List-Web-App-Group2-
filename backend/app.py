from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Task  # Import db and Task from models
from routes import list_routes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database (using the db instance)
db.init_app(app)

#allows cross communication
CORS(app)

#from routes.py for all the route methods
list_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the table
        print("database created successfull")
    app.run(debug=True)

    #this imports everything. Points to where the DB is. Starts or creates the database when the flask program is started and is the starting point of the backend.