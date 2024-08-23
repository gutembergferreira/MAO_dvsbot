import os
from google.oauth2 import service_account

# Configurações de diretórios
template_dir = os.path.abspath('./WEB/')
static_dir = os.path.abspath('./WEB/static/')

# Configuração do caminho do banco de dados SQLite
database_path = os.path.join(os.getcwd(), 'database', 'messages.db')

# Classe de configuração do Flask
class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{database_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuração para autenticação do Google Chat
SCOPES = ["https://www.googleapis.com/auth/chat.bot"]
SERVICE_ACCOUNT_FILE = 'CREDENTIAL/credential.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)