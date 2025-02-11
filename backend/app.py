from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Task  # Importing the model and db object

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional but good practice
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Fetch all tasks from the database.
    """
    tasks = Task.query.all()  # Fetch all tasks from DB
    return jsonify([task.to_dictionary() for task in tasks])  # Convert to list of dicts and return as JSON

@app.route('/tasks', methods=['POST'])
def add_task():
    """
    Add a new task to the database.
    """
    data = request.get_json()  # Get JSON data from the request body
    new_task = Task(
        task=data['task'],
        description=data.get('description'),
        priority=data.get('priority'),
        status=data.get('status', True),
        task_date=data.get('task_date')
    )
    db.session.add(new_task)
    db.session.commit()  # Save to the database
    return jsonify(new_task.to_dictionary()), 201  # Return the added task

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
