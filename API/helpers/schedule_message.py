from app import *
from API.models.webhooks_models import Webhook

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