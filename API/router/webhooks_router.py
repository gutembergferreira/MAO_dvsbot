
from app import *


@app.route('/add_webhook', methods=['POST', 'GET'])
def add_webhook():
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        new_webhook = Webhook(name=name, url=url)
        db.session.add(new_webhook)
        db.session.commit()
        save_logger('ADDITION','Bot added successfully','WEBHOOK', name)
        return redirect(url_for('webhooks'))
    return render_template('add_webhook.html')


@app.route('/edit_webhook/<int:webhook_id>', methods=['POST', 'GET'])
def edit_webhook(webhook_id):
    webhook = Webhook.query.get_or_404(webhook_id)
    if request.method == 'POST':
        webhook.name = request.form.get('name')
        webhook.url = request.form.get('url')
        db.session.commit()
        save_logger('EDIT','Bot edited successfully','WEBHOOK', webhook.name)
        return redirect(url_for('webhooks'))
    return render_template('edit_webhook.html', webhook=webhook)


@app.route('/delete_webhook/<int:webhook_id>', methods=['POST'])
def delete_webhook(webhook_id):
    webhook = Webhook.query.get_or_404(webhook_id)
    db.session.delete(webhook)
    db.session.commit()
    save_logger('DELETE','Bot deleted successfully','WEBHOOK', webhook.name)
    return redirect(url_for('webhooks'))