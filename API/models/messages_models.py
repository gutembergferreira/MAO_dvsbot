from app import * 

# Modelo de Mensagem
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(100))
    message = db.Column(db.String(200), nullable=False)
    days_of_week = db.Column(db.String(200), nullable=False)
    send_time = db.Column(db.String(10), nullable=False)
    webhook_id = db.Column(db.Integer, db.ForeignKey('webhook.id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    scheduler_job_id = db.Column(db.String(100))
    webhook = db.relationship('Webhook', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f'<Message {self.message}>'