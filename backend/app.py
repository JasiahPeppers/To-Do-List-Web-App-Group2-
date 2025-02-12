from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Set up SQLite database (will create tasks.db in your project folder)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    """
    Task Model represents the tasks in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    priority = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Boolean, default=True)  # Default to True (task is active)
    task_date = db.Column(db.String(20), nullable=True)

    def __init__(self, task, description=None, priority=None, status=True, task_date=None):
        self.task = task
        self.description = description
        self.priority = priority
        self.status = status
        self.task_date = task_date

    def to_dictionary(self):
        """
        Convert Task object to dictionary format.
        """
        return {
            "id": self.id,
            "task": self.task,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "task_date": self.task_date
        }

# Create the database tables (run this once)
@app.before_first_request
def create_tables():
    db.create_all()  # Creates all database tables

# Get all tasks (GET /tasks)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Fetch tasks for today or tomorrow
    date_filter = request.args.get('date')
    if date_filter:
        filtered_tasks = Task.query.filter_by(task_date=date_filter).all()
        return jsonify([task.to_dictionary() for task in filtered_tasks])
    tasks = Task.query.all()  # Get all tasks
    return jsonify([task.to_dictionary() for task in tasks])

# Add a new task (POST /tasks)
@app.route('/tasks', methods=['POST'])
def add_task():
    new_task_data = request.get_json()
    new_task = Task(
        task=new_task_data['task'],
        description=new_task_data.get('description', ''),
        priority=new_task_data.get('priority', ''),
        status=True,  # Default to active
        task_date=new_task_data.get('task_date', '')
    )
    db.session.add(new_task)  # Add task to the session
    db.session.commit()  # Commit changes to the database
    return jsonify(new_task.to_dictionary()), 201  # Return the newly created task

# Update a task (PUT /tasks/<task_id>)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)  # Fetch the task or return 404 if not found
    updated_data = request.get_json()
    task.description = updated_data.get('description', task.description)
    task.status = updated_data.get('status', task.status)
    db.session.commit()  # Commit the changes
    return jsonify(task.to_dictionary())

# Delete a task (DELETE /tasks/<task_id>)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)  # Fetch task or return 404 if not found
    db.session.delete(task)  # Delete task from session
    db.session.commit()  # Commit the deletion
    return jsonify({"message": "Task deleted successfully"}), 204  # 204 No Content

if __name__ == '__main__':
    app.run(debug=True)
