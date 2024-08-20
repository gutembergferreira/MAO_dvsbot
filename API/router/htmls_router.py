from app import *


@app.route('/')
def index():
    return render_template('index.html')


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

