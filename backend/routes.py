# backend/routes.py

from .app import app, db  # Import db from app
from model import Task
from flask import Blueprint, request, jsonify

# Create a Blueprint to hold your routes
list_routes = Blueprint('list_routes', __name__)

# GET route - Fetch all tasks
@list_routes.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.description for task in tasks])

# POST route - Add a new task
@list_routes.route('/tasks', methods=['POST'])
def add_task():
    task_data = request.json
    new_task = Task(task=task_data['task'], description=task_data['description'])  # Task, not description
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added'}), 201


# PUT route - Mark a task as completed
@list_routes.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
        return jsonify({'message': 'Task marked as complete'})
    return jsonify({'message': 'Task not found'}), 404

# DELETE route - Delete a task
@list_routes.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'})
    return jsonify({'message': 'Task not found'}), 404



    # Basic routes for add, update, and delete. Might need a few tweaks but should be close generally.
    # May have to add more for more functionality, but for now, I'm keeping it basic.

