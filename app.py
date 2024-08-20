from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime 
import datetime as dt
import requests
from google.oauth2 import service_account
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask_sqlalchemy import SQLAlchemy
import os
from pytz import utc

app = Flask(__name__)

# Configuração do banco de dados SQLite
# Caminho absoluto para o arquivo de banco de dados na pasta `database/`
database_path = os.path.join(os.getcwd(), 'database', 'messages.db')

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
        
# Inicializar o banco de dados
with app.app_context():
    db.create_all()

SCOPES = ["https://www.googleapis.com/auth/chat.bot"]
SERVICE_ACCOUNT_FILE = 'credential/bot-monitor.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Inicializa o agendador de tarefas
scheduler = BackgroundScheduler()
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)

from API.helpers.logger_save import save_logger
from API.helpers.schedule_message import schedule_message,send_message_to_google_chats
from API.models.webhooks_models import Webhook
from API.models.messages_models import Message
from API.models.birthdays_models import Birthday
from API.models.logs_models import Log

from API.router import webhooks_router
from API.router import messages_router
from API.router import htmls_router
from API.router import brithdays_router
from API.router import schedule_router