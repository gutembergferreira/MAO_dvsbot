from app import *

# Rota para agendar mensagens
@app.route('/schedule_message', methods=['POST'])
def schedule_message_route():
    message_text = request.form.get('message')
    days_of_week = ','.join(request.form.getlist('days_of_week'))
    send_time = request.form.get('send_time')
    if request.form.get('active') == 'on':
        active = True
    else:
        active = False
    
    # Captura o ID do webhook
    webhook_id = request.form.get('webhook_id')  # Captura o ID do webhook

    new_message = Message(
        message=message_text, 
        days_of_week=days_of_week, 
        send_time=send_time, 
        active=active,
        webhook_id=webhook_id  # Associa o webhook
    )
    db.session.add(new_message)
    db.session.commit()
    save_logger('ADDITION','Message added successfully','MESSAGE')
    # Agendar a mensagem
    schedule_message(new_message)

    return redirect(url_for('messages'))


@app.route('/send_now', methods=['POST'])
def send_now():
    message = request.form.get('message')
    status_code = send_message_to_google_chats(message)
    if status_code == 200:
        return "Mensagem enviada com sucesso!", 200
    else:
        return "Falha ao enviar mensagem.", 500
