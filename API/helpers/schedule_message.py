from app import *
from API.models.webhooks_models import Webhook
from API.models.messages_models import Message

def send_message_to_google_chats(message, webhook_url):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "text": message
    }
    response = requests.post(webhook_url, json=data, headers=headers)
    return response.status_code

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
        save_logger('ADDITION/EDIT','Scheduler added successfully','SCHEDULER')
    except ValueError as e:
        print(f"Erro ao agendar a mensagem: {e}")
    except KeyError as e:
        print(f"Erro ao mapear o dia da semana: {e}")
        
        
def get_scheduler_status(scheduler):
    if scheduler.running:
        return "Running"
    else:
        return "Stopped"
    
def get_weekly_jobs():
    jobs = []
    current_time = datetime.now(utc)

    for job in scheduler.get_jobs():
        job_time = job.next_run_time
        if job_time and job_time >= current_time:
            jobs.append(job)

    return jobs



def get_memory_usage():
    process = psutil.Process()
    mem_info = process.memory_info()
    return mem_info.rss  # Memory usage in bytes

import os

def get_database_size(db_path):
    return os.path.getsize(db_path)  # Tamanho em bytes

def load_jobs_on_startup():
    messages = Message.query.filter_by(active=True).all()
    for message in messages:
        schedule_message(message)
