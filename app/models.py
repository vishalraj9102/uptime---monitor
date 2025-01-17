from app import db
from datetime import datetime

# Website Model
class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=True)
    url = db.Column(db.String(512), nullable=False)
    check_interval_seconds = db.Column(db.Integer, default=300)
    expected_status_code = db.Column(db.Integer, default=200)
    last_status = db.Column(db.String(10), default="unknown")
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    last_status_change = db.Column(db.DateTime, default=datetime.utcnow)

    # Method to return website data as a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'check_interval_seconds': self.check_interval_seconds,
            'expected_status_code': self.expected_status_code,
            'last_status': self.last_status,
            'last_checked': self.last_checked,
            'last_status_change': self.last_status_change,
        }

    # Method to get the status history of the website
    def get_status_history(self):
        history = StatusHistory.query.filter_by(website_id=self.id).order_by(StatusHistory.timestamp.desc()).all()
        return [
            {"status": item.status, "timestamp": str(item.timestamp)} for item in history
        ]


# StatusHistory Model (Tracks status changes)
class StatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    website = db.relationship('Website', backref=db.backref('status_history', lazy=True))


class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), nullable=False)
