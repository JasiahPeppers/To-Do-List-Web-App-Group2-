from flask import request, jsonify
from models import db, Task

def list_routes(app):  # Pass the app instance into the function

    # GET route - Fetch all tasks
    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([task.to_dictionary() for task in tasks])  # Use to_dictionary to return all task details

    # POST route - Add a new task
    @app.route('/tasks', methods=['POST'])
    def add_task():
        task_data = request.json
        print(f"Received task data: {task_data}")  # Debugging line

        # Validate required fields
        if not task_data.get('task') or not task_data.get('description'):
            return jsonify({'message': 'Task and description are required'}), 400

        # Create new task with priority and task date
        new_task = Task(
            task=task_data['task'],
            description=task_data['description'],
            priority=task_data.get('priority', 'Low'),  # Default to 'Low' if not provided
            task_date=task_data.get('task_date')
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added'}), 201

    # PUT route - Mark a task as completed (change status field)
    @app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
    def complete_task(task_id):
        task = Task.query.get(task_id)
        if task:
            task.status = 'completed'  # Mark as completed by setting status to 'completed'
            db.session.commit()
            return jsonify({'message': 'Task marked as complete'})
        return jsonify({'message': 'Task not found'}), 404

    # DELETE route - Delete a task
    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted'})
        return jsonify({'message': 'Task not found'}), 404
