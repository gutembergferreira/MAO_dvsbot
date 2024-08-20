from app import * 

# Modelo de Bots - WEBHOOKS
class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Webhook {self.name}>'