from app import *

@app.route('/add_birthday', methods=['POST', 'GET'])
def add_birthday():
    if request.method == 'POST':
        name = request.form.get('name')
        active = request.form.get('active') == 'true'
        birthday_date = dt.datetime.strptime(request.form.get('birthday_date'), '%Y-%m-%d').date()
        google_chat_id = request.form.get('google_chat_id')
        webhook_id = request.form.get('webhook_id')
        new_birthday = Birthday(name=name, active=active, birthday_date=birthday_date, google_chat_id=google_chat_id, webhook_id=webhook_id)
        db.session.add(new_birthday)
        db.session.commit()
        save_logger('ADDITION','Birthdays added successfully','BIRTHDAY','Birthdays '+ name )
        if active:
            schedule_birthday(new_birthday)
        return redirect(url_for('birthdays'))
    
    return render_template('add_birthday.html')

@app.route('/edit_birthday/<int:birthday_id>', methods=['POST', 'GET'])
def edit_birthday(birthday_id):
    birthday = Birthday.query.get_or_404(birthday_id)
    all_webhooks = Webhook.query.all()   
    if request.method == 'POST':
        birthday.name = request.form.get('name')
        birthday.active = request.form.get('active')
        birthday.birthday_date = dt.datetime.strptime(request.form.get('birthday_date'), '%Y-%m-%d').date()
        birthday.google_chat_id = request.form.get('google_chat_id')
        
        db.session.commit()
        save_logger('EDIT','Birthdays edited successfully','BIRTHDAY','Birthdays '+ birthday.name)
        if birthday.active:
            schedule_birthday(birthday)
        return redirect(url_for('birthdays'))
    
    return render_template('edit_birthday.html', birthday=birthday, webhooks=all_webhooks)

@app.route('/delete_birthday/<int:birthday_id>', methods=['POST'])
def delete_birthday(birthday_id):
    birthday = Birthday.query.get_or_404(birthday_id)
    db.session.delete(birthday)
    db.session.commit()
    save_logger('DELETE','Birthdays deleted successfully','BIRTHDAY', birthday.name)
    delete_schedule_birthday(birthday)
    return redirect(url_for('birthdays'))