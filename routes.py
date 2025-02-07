from flask import request, jsonify
from models import db, Task

def list_routes(app):
    # Get all tasks
    @app.route('/tasks', methods=["GET"])
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([task.to_dictionary() for task in tasks]), 200

    # Create a new task
    @app.route('/tasks', methods=['POST'])
    def add_task():
        data = request.json  # or data = request.get_json()
        new_task = Task(
            task=data['task'],
            desc=data.get('desc'),
            priority=data.get('priority'),
            status=data.get('status', True)
            task_date=data.get('task_date')
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added successfully'}), 201  

    # Update task
    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        data = request.json
        task = Task.query.get_or_404(task_id)
        task.task = data.get('task', task.task)
        task.desc = data.get('desc', task.desc)
        task.priority = data.get('priority', task.priority)
        task.status = data.get('status', task.status)
        task.task_date = data.get('task_date', task.task_date)
        db.session.commit()
        return jsonify({'message': 'Task Updated'}), 200

    # Delete task
    @app.route('/tasks/<int:id>', methods=['DELETE'])
    def delete_task(id):
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task Deleted'}), 200

    # Basic routes for add, update, and delete. Might need a few tweaks but should be close generally.
    # May have to add more for more functionality, but for now, I'm keeping it basic.
