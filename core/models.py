from datetime import datetime
from extensions.database import db

class Blacklist(db.Model):
    email = db.Column(db.String(255), primary_key=True)
    app_uuid = db.Column(db.String(255), nullable=False)
    blocked_reason = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(255), nullable=False)  
    request_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Blacklist {self.email}>"
