from app import * 

# Modelo de Logs
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.now(utc))
    action = db.Column(db.String(50), nullable=False)
    response = db.Column(db.String(255), nullable=False)
    user = db.Column(db.String(10), nullable=False)
    feature = db.Column(db.String(30), nullable=False)
    def __init__(self, action, response,feature, user, summary):
        self.action = action
        self.summary = summary
        self.response = response
        self.feature = feature
        self.user = user