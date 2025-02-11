from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_migrate import Migrate
from models import db, Task  # Import the Task model after db initialization

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["https://todolistapp.infy.uk/?i=1"])
# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional but good practice

# Initialize db object
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Home route
@app.route('/')
def home():
    return 'Hello, World!'

# Route to fetch all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()  # Get all tasks from the database
    tasks_list = [task.to_dictionary() for task in tasks]  # Convert tasks to dictionary format
    return {"tasks": tasks_list}

# Route to add a task (POST request)
@app.route('/tasks', methods=['POST'])
def add_task():
    task_data = request.get_json()  # Get JSON data from request
    new_task = Task(
        task=task_data['task'],
        description=task_data.get('description'),
        priority=task_data.get('priority'),
        status=task_data.get('status', True),  # Default to True if not provided
        task_date=task_data.get('task_date')
    )
    db.session.add(new_task)  # Add the new task to the session
    db.session.commit()  # Commit the changes to the database
    return {"message": "Task added successfully", "task": new_task.to_dictionary()}

# Route to update a task (PUT request)
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task_data = request.get_json()  # Get JSON data from request
    task = Task.query.get(id)  # Get the task by ID
    if task:
        task.task = task_data.get('task', task.task)
        task.description = task_data.get('description', task.description)
        task.priority = task_data.get('priority', task.priority)
        task.status = task_data.get('status', task.status)
        task.task_date = task_data.get('task_date', task.task_date)

        db.session.commit()  # Commit the changes
        return {"message": "Task updated successfully", "task": task.to_dictionary()}
    else:
        return {"message": "Task not found"}, 404

# Route to delete a task (DELETE request)
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)  # Get the task by ID
    if task:
        db.session.delete(task)  # Delete the task
        db.session.commit()  # Commit the changes
        return {"message": "Task deleted successfully"}
    else:
        return {"message": "Task not found"}, 404

if __name__ == '__main__':
    app.run(debug=True)
