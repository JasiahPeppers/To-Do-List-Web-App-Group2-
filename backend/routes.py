from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://todolistapp.infy.uk/"])  # Allow frontend origin

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), nullable=False)
    desc = db.Column(db.String(255))
    priority = db.Column(db.String(50))
    task_date = db.Column(db.String(50))
    status = db.Column(db.String(50), default="incomplete")

    def to_dictionary(self):
        return {
            'id': self.id,
            'task': self.task,
            'desc': self.desc,
            'priority': self.priority,
            'task_date': self.task_date,
            'status': self.status
        }

# Routes
@app.route('/tasks', methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dictionary() for task in tasks]), 200

@app.route('/tasks', methods=["POST"])
def add_task():
    data = request.json
    new_task = Task(
        task=data['task'],
        desc=data.get('desc'),
        priority=data.get('priority'),
        task_date=data.get('task_date')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
data = request.json
task = Task.query.get_or_404(task_id)
    
task.task = data.get('task', task.task)
task.desc = data.get('desc', task.desc)
task.priority = data.get('priority', task.priority)
task.task_date = data.get('task_date', task.task_date)
    
    # Check if status is 'completed', set it as True (Boolean)
if data.get('status') == 'completed':
task.status = True  # Mark as completed (Boolean True)
elif data.get('status') == 'incomplete':
task.status = False  # Mark as incomplete (Boolean False)
db.session.commit()
return jsonify({'message': 'Task updated successfully'}), 200

    
if data.get('status') =='completed';
task.status =True # this is mark as completed set to true
elif data.get('status') == 'incomplete': 
task.status = False # this is mark as compelte set to false
    
db.session.commit()
    return jsonify({'message': 'Task updated successfully'}), 200

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

if __name__ == '__main__':
    db.create_all()  # Create the tables
    app.run(debug=True)
