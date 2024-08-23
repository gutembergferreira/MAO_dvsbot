from app import *

@app.route('/')
def index():
    scheduler_status = get_scheduler_status(scheduler)
    weekly_jobs = get_weekly_jobs()
    memory_usage = round(get_memory_usage() / (1024 * 1024), 2)   # Convertendo para MB
    database_size = round(get_database_size(database_path) / (1024 * 1024), 2)  # Convertendo para MB

    return render_template('pages/index/index.html', 
                           scheduler_status=scheduler_status,
                           weekly_jobs=weekly_jobs,
                           memory_usage=memory_usage,
                           database_size=database_size)


@app.route('/webhooks')
def webhooks():
    all_webhooks = Webhook.query.all()
    return render_template('pages/webhooks/webhooks.html', webhooks=all_webhooks)

@app.route('/messages')
def messages():
    all_messages = Message.query.all()
    all_webhooks = Webhook.query.all()
    return render_template('pages/messages_weekly/messages.html', messages=all_messages, webhooks=all_webhooks)

@app.route('/birthdays')
def birthdays():
    all_birthdays = Birthday.query.all()
    all_webhooks = Webhook.query.all()
    return render_template('pages/birthdays/birthdays.html', birthdays=all_birthdays, webhooks=all_webhooks)

@app.route('/logs')
def logs():
    all_logs = Log.query.all()
    return render_template('pages/logs/logs.html', logs=all_logs)

@app.route('/settings')
def settings():
    return render_template('pages/settings/settings.html')

