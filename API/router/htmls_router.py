

from app import *


@app.route('/')
def index():
    scheduler_status = get_scheduler_status(scheduler)
    weekly_jobs = get_weekly_jobs()
    memory_usage = round(get_memory_usage() / (1024 * 1024), 2)   # Convertendo para MB
    database_size = round(get_database_size(database_path) / (1024 * 1024), 2)  # Convertendo para MB

    return render_template('index.html', 
                           scheduler_status=scheduler_status,
                           weekly_jobs=weekly_jobs,
                           memory_usage=memory_usage,
                           database_size=database_size)


@app.route('/webhooks')
def webhooks():
    all_webhooks = Webhook.query.all()
    return render_template('webhooks.html', webhooks=all_webhooks)

@app.route('/messages')
def messages():
    all_messages = Message.query.all()
    all_webhooks = Webhook.query.all()
    return render_template('messages.html', messages=all_messages, webhooks=all_webhooks)

@app.route('/birthdays')
def birthdays():
    all_birthdays = Birthday.query.all()
    return render_template('birthdays.html', birthdays=all_birthdays)

@app.route('/logs')
def logs():
    all_logs = Log.query.all()
    return render_template('logs.html', logs=all_logs)

