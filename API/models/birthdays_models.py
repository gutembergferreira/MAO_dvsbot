from app import * 

# Modelo de Aniversariantes
class Birthday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    birthday_date = db.Column(db.Date, nullable=False)
    google_chat_id = db.Column(db.String(200), nullable=False)
    webhook_id = db.Column(db.Integer, db.ForeignKey('webhook.id'), nullable=False)
    scheduler_job_id = db.Column(db.String(100))
    webhook = db.relationship('Webhook', backref=db.backref('birthdays', lazy=True))
    def __repr__(self):
        return f'<Birthday {self.name}>'