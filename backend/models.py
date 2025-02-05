from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), nullable=False)
    desc = db.Column(db.String(255))
    priority = db.Column(db.String(50))
    task_date = db.Column(db.String(50))
    status = db.Column(db.Boolean, default=False)  # Boolean type
    
    def to_dictionary(self):
        return {
            'id': self.id,
            'task': self.task,
            'desc': self.desc,
            'priority': self.priority,
            'task_date': self.task_date,
            'status': self.status
        }
    
#this defines whats in the table and then turns it into a dictionary for easier Json 
