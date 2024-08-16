from flask import Flask, render_template, request, redirect, url_for
import datetime
import requests
from google.oauth2 import service_account
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

# Configuração do banco de dados SQLite
# Caminho absoluto para o arquivo de banco de dados na pasta `database/`
database_path = os.path.join(os.getcwd(), 'database', 'messages.db')

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Mensagem
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    days_of_week = db.Column(db.String(200), nullable=False)
    send_time = db.Column(db.String(10), nullable=False)
    webhook_id = db.Column(db.Integer, db.ForeignKey('webhook.id'), nullable=False)

    webhook = db.relationship('Webhook', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f'<Message {self.message}>'
    
class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Webhook {self.name}>'
# Inicializar o banco de dados
with app.app_context():
    db.create_all()
    
    
@app.route('/')
def index():
    all_messages = Message.query.all()
    all_webhooks = Webhook.query.all()
    return render_template('index.html', messages=all_messages, webhooks=all_webhooks)

SCOPES = ["https://www.googleapis.com/auth/chat.bot"]
SERVICE_ACCOUNT_FILE = 'credential/bot-monitor.json'
CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/XXXX/messages?key=XXXX"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def send_message_to_google_chats(message, webhook_url):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "text": message
    }
    response = requests.post(webhook_url, json=data, headers=headers)
    return response.status_code

@app.route('/send_now', methods=['POST'])
def send_now():
    message = request.form.get('message')
    status_code = send_message_to_google_chats(message)
    if status_code == 200:
        return "Mensagem enviada com sucesso!", 200
    else:
        return "Falha ao enviar mensagem.", 500

# Função para agendar mensagens
def schedule_message(message):
    try:
        hour, minute = map(int, message.send_time.split(':'))

        # Map the full weekday names to their short form
        day_map = {
            'monday': 'mon',
            'tuesday': 'tue',
            'wednesday': 'wed',
            'thursday': 'thu',
            'friday': 'fri',
            'saturday': 'sat',
            'sunday': 'sun'
        }

        days = ','.join(day_map[day] for day in message.days_of_week.split(','))

        # Retrieve the associated webhook
        webhook = Webhook.query.get(message.webhook_id)

        # Create the cron trigger with the correct day and time
        trigger = CronTrigger(day_of_week=days, hour=hour, minute=minute)

        # Schedule the message with the correct webhook URL
        scheduler.add_job(func=send_message_to_google_chats, trigger=trigger, args=[message.message, webhook.url])

    except ValueError as e:
        print(f"Erro ao agendar a mensagem: {e}")
    except KeyError as e:
        print(f"Erro ao mapear o dia da semana: {e}")
        
        
# Rota para agendar mensagens
@app.route('/schedule_message', methods=['POST'])
def schedule_message_route():
    message_text = request.form.get('message')
    days_of_week = ','.join(request.form.getlist('days_of_week'))
    send_time = request.form.get('send_time')
    webhook_id = request.form.get('webhook_id')  # Captura o ID do webhook

    new_message = Message(
        message=message_text, 
        days_of_week=days_of_week, 
        send_time=send_time, 
        webhook_id=webhook_id  # Associa o webhook
    )
    db.session.add(new_message)
    db.session.commit()

    # Agendar a mensagem
    schedule_message(new_message)

    return redirect(url_for('index'))

@app.route('/edit/<int:message_id>', methods=['GET', 'POST'])
def edit_message(message_id):
    # Busca a mensagem no banco de dados
    message = Message.query.get_or_404(message_id)
    all_webhooks = Webhook.query.all()
    if request.method == 'POST':
        # Captura os valores do formulário enviados pelo POST
        new_message_text = request.form.get('message')
        new_days_of_week = ','.join(request.form.getlist('days_of_week'))
        new_send_time = request.form.get('send_time')
        
        # Validação dos valores do formulário
        if not new_message_text or not new_days_of_week or not new_send_time:
            return "Por favor, preencha todos os campos obrigatórios.", 400
        
        # Atualiza os campos da mensagem no banco de dados
        message.message = new_message_text
        message.days_of_week = new_days_of_week
        message.send_time = new_send_time
        
        # Salva as mudanças no banco de dados
        db.session.commit()
        
        # Reagenda a mensagem
        schedule_message(message)
        
        # Redireciona para a página principal após salvar
        return redirect(url_for('index'))
    
    # Se o método for GET, renderiza a página de edição com os dados atuais da mensagem
    return render_template('edit_message.html', message=message, all_webhooks=all_webhooks)

# Rota para excluir mensagem
@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/webhooks')
def webhooks():
    all_webhooks = Webhook.query.all()
    return render_template('webhooks.html', webhooks=all_webhooks)

@app.route('/add_webhook', methods=['POST', 'GET'])
def add_webhook():
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        new_webhook = Webhook(name=name, url=url)
        db.session.add(new_webhook)
        db.session.commit()
        return redirect(url_for('webhooks'))
    return render_template('add_webhook.html')

@app.route('/edit_webhook/<int:webhook_id>', methods=['POST', 'GET'])
def edit_webhook(webhook_id):
    webhook = Webhook.query.get_or_404(webhook_id)
    if request.method == 'POST':
        webhook.name = request.form.get('name')
        webhook.url = request.form.get('url')
        db.session.commit()
        return redirect(url_for('webhooks'))
    return render_template('edit_webhook.html', webhook=webhook)

@app.route('/delete_webhook/<int:webhook_id>', methods=['POST'])
def delete_webhook(webhook_id):
    webhook = Webhook.query.get_or_404(webhook_id)
    db.session.delete(webhook)
    db.session.commit()
    return redirect(url_for('webhooks'))


# Inicializa o agendador de tarefas
scheduler = BackgroundScheduler()
scheduler.start()

    
if __name__ == '__main__':
    app.run(debug=True)
