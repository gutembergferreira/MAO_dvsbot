from app import *


@app.route('/edit/<int:message_id>', methods=['GET', 'POST'])
def edit_message(message_id):
    # Busca a mensagem no banco de dados
    message = Message.query.get_or_404(message_id)
    all_webhooks = Webhook.query.all()
    if request.method == 'POST':
        # Captura os valores do formulário enviados pelo POST
        new_message_text = request.form.get('message')
        new_days_of_week = ','.join(request.form.getlist('days_of_week'))
        new_send_time = request.form.get('send_time')
        
        # Validação dos valores do formulário
        if not new_message_text or not new_days_of_week or not new_send_time:
            return "Por favor, preencha todos os campos obrigatórios.", 400
        
        # Atualiza os campos da mensagem no banco de dados
        message.message = new_message_text
        message.days_of_week = new_days_of_week
        message.send_time = new_send_time
        
        # Salva as mudanças no banco de dados
        db.session.commit()
        save_logger('EDIT','Message edited successfully','MESSAGE')
        # Reagenda a mensagem
        schedule_message(message)
        
        # Redireciona para a página principal após salvar
        return redirect(url_for('messages'))
    
    # Se o método for GET, renderiza a página de edição com os dados atuais da mensagem
    return render_template('edit_message.html', message=message, all_webhooks=all_webhooks)

# Rota para excluir mensagem
@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    job_id = str(message_id)
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        save_logger('DELETE', 'Schedule deleted successfully', 'SCHEDULER')
    # Salvar o log
    db.session.delete(message)
    db.session.commit()
    save_logger('DELETE','Message deleted successfully','MESSAGE')
    return redirect(url_for('messages'))