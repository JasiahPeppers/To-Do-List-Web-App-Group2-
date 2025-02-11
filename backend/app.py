from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Initialize migration
migrate = Migrate(app, db)

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Boolean, default=True)  # Status of task (True = Incomplete, False = Completed)

    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'description': self.description,
            'status': self.status
        }

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

# Route to add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(
        task=data['task'],
        description=data.get('description', ''),
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

# Route to update an existing task (by task ID)
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    task.task = data.get('task', task.task)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)

    db.session.commit()
    return jsonify(task.to_dict())

# Route to delete a task (by task ID)
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204  # No content, successfully deleted

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
