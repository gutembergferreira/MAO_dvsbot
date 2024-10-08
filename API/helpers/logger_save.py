from app import *
from API.models.logs_models import Log

def save_logger(action, response,feature,summary, user=None):
    if user is None:
        try:
            user = request.remote_addr  # Se nenhum usuário for fornecido, use o endereço IP como padrão
        except:
            user = 'localhost'
    # Criando uma nova instância de Log
    log_entry = Log(
        action=action,                # Ação realizada
        response=response,            # Resposta da ação
        user=user,               # Usuário que realizou a ação
        feature=feature,
        summary=summary
    )
    
    # Salvando o log no banco de dados
    db.session.add(log_entry)
    db.session.commit()