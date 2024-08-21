from app import *
from API.models.webhooks_models import Webhook
from API.models.birthdays_models import Birthday

def schedule_birthday(birthday):
    try:
        scheduler.remove_job(str(birthday.scheduler_job_id))
    except:
        pass
    try:
        today = datetime.now(utc)
        birthday_date_validate = birthday.birthday_date.replace(year=today.year)
        birthday_date_job = birthday_date_validate
        # Ajuste da data para o primeiro dia útil, se o aniversário cair no fim de semana
        if birthday_date_validate.weekday() == 5:  # Sábado
            birthday_date_job += dt.timedelta(days=2)
        elif birthday.birthday_date.weekday() == 6:  # Domingo
            birthday_date_job += dt.timedelta(days=1)
        else:
            birthday_date_job = birthday_date_validate
            
        hour, minute = 8, 0  # Horário fixo às 8:00 AM
        trigger = CronTrigger(year=today.year, month=birthday_date_job.month, day=birthday_date_job.day, hour=hour, minute=minute)
        webhook = Webhook.query.get(birthday.webhook_id)
        job = scheduler.add_job(func=send_message_to_google_chats, name=f"birthday-{birthday.name}", trigger=trigger, args=[f"Parabéns, {birthday.name}!", webhook.url])
        
        # Salva o ID do job na base de dados (adicionar campo 'scheduler_job_id' no modelo Birthday, se necessário)
        birthday.scheduler_job_id = job.id
        db.session.commit()
        save_logger('ADDITION','Scheduler added for birthday','SCHEDULER', f"Birthday job for {birthday.name}")
    except (ValueError, KeyError) as e:
        print(f"Erro ao agendar mensagem de parabéns: {e}")
        
def delete_schedule_birthday(birthday):
    try:
        scheduler.remove_job(str(birthday.scheduler_job_id))
        save_logger('DELETE','Scheduler deleted successfully','SCHEDULER', f"birthday-{birthday.name}")
    except:
        pass
    
def load_jobs_on_startup_birthday():
    birthdays = Birthday.query.filter_by(active=True).all()
    for birthday in birthdays:
        schedule_birthday(birthday)