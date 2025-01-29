from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50), nullable=True) 
    desc = db.Column(db.String(255), nullable=True)  
    priority = db.Column(db.String(50), nullable=True)  
    status = db.Column(db.Boolean, default=True)  
    task_date = db.Column(db.String(20), nullable=True)  

    def to_dictionary(self):
        return {
            "id": self.id,
            "task": self.task, 
            "desc": self.desc,
            "priority": self.priority,
            "status": self.status,
            "task_date": self.task_date
        }

    
#this defines whats in the table and then turns it into a dictionary for easier Json 