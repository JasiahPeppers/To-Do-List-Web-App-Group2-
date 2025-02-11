from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Task  # Assuming you're importing db and Task from models.py

app = Flask(__name__)

# Make sure your Flask app is correctly configured with the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks = Task.query.all()  # Fetch all tasks from the database
        return jsonify([task.to_dictionary() for task in tasks])  # Return tasks as JSON

    elif request.method == 'POST':
        data = request.get_json()  # Get the data from the request
        new_task = Task(
            task=data['task'],
            description=data.get('description', ''),
            priority=data.get('priority', ''),
            status=True,  # Default to True for active tasks
            task_date=data.get('task_date', '')
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dictionary()), 201  # Return the newly created task

@app.route('/tasks/<int:id>', methods=['PUT', 'DELETE'])
def task(id):
    task = Task.query.get_or_404(id)

    if request.method == 'PUT':
        data = request.get_json()
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        db.session.commit()
        return jsonify(task.to_dictionary())

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
