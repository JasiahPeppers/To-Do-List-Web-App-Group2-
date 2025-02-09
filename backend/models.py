from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50), nullable=False)  # Task name should likely be required
    description = db.Column(db.String(255), nullable=True)
    priority = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Boolean, default=True)  # Default to True (e.g., task is active)
    task_date = db.Column(db.String(20), nullable=True)

    def __init__(self, task, description=None, priority=None, status=True, task_date=None):
        self.task = task
        self.description = description
        self.priority = priority
        self.status = status
        self.task_date = task_date

    def to_dictionary(self):
        return {
            "id": self.id,
            "task": self.task,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "task_date": self.task_date
        }


# This defines what's in the table and then turns it into a dictionary for easier JSON handling.
