from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)  # Ensure description column is here
    priority = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='incomplete')
    task_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Ensure the task table exists, with the description column
@app.before_first_request
def create_tables():
    db.create_all()

# Fetch all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'task': task.task,
        'description': task.description,
        'priority': task.priority,
        'status': task.status,
        'task_date': task.task_date
    } for task in tasks])

# Add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(
        task=data['task'],
        description=data['description'],
        priority=data['priority']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        'id': new_task.id,
        'task': new_task.task,
        'description': new_task.description,
        'priority': new_task.priority,
        'status': new_task.status,
        'task_date': new_task.task_date
    })

# Edit task description
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task:
        data = request.get_json()
        task.description = data.get('description', task.description)
        db.session.commit()
        return jsonify({
            'id': task.id,
            'task': task.task,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'task_date': task.task_date
        })
    return jsonify({'error': 'Task not found'}), 404

# Delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    return jsonify({'error': 'Task not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
