from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Roles: Data entry operator, Admin, Data analyst

class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    types_of_breakdown = db.Column(db.String(150), nullable=False)
    reason = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    breakdown_description = db.Column(db.Text, nullable=False)
    corrective_action = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    mr = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def export_for_gantt_chart(self):
        start_time = f"{self.date.strftime('%m-%d-%Y')} {self.start_time.strftime('%H:%M:%S')}"
        end_time = f"{self.date.strftime('%m-%d-%Y')} {self.end_time.strftime('%H:%M:%S')}"
        return { 
            "type": self.types_of_breakdown,
            "duration": self.duration,
            "name": self.reason, 
            "y": [start_time, end_time],
        },

    def serialize(self):
        return {
            'id': self.id,
            'types_of_breakdown': self.types_of_breakdown,
            'reason': self.reason,
            'date': self.date.strftime('%m-%d-%Y'),  # Convert date to string
            'breakdown_description': self.breakdown_description,
            'corrective_action': self.corrective_action,
            "duration": self.duration,
            'start_time': f"{self.date.strftime('%m-%d-%Y')} {self.start_time.strftime('%H:%M:%S')}",  # Convert date and time to string
            'end_time': f"{self.date.strftime('%m-%d-%Y')} {self.end_time.strftime('%H:%M:%S')}",  # Convert date and time to string
            'mr': self.mr,
            'user_id': self.user_id
        }
