from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime,timedelta
import datetime as dt
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask_sqlalchemy import SQLAlchemy
import os
from pytz import utc
import psutil
from config import static_dir, template_dir, Config, SCOPES, SERVICE_ACCOUNT_FILE, credentials


app = Flask(__name__,static_folder=static_dir, template_folder=template_dir)
app.config.from_object(Config)
db = SQLAlchemy(app)
scheduler = BackgroundScheduler()
scheduler.start()

from API.helpers.logger_save import save_logger
from API.helpers.schedule_message import get_database_size, get_memory_usage, load_jobs_on_startup_message,schedule_message,send_message_to_google_chats,get_scheduler_status,get_weekly_jobs, delete_schedule_message
from API.helpers.schedule_birthday import load_jobs_on_startup_birthday, schedule_birthday, delete_schedule_birthday
from API.models.webhooks_models import Webhook
from API.models.messages_models import Message
from API.models.birthdays_models import Birthday
from API.models.logs_models import Log
from API.router import webhooks_router,messages_router,htmls_router,brithdays_router,schedule_router

with app.app_context():
    db.create_all()
    try:
        load_jobs_on_startup_message()
        load_jobs_on_startup_birthday()
    except:
        pass
    
if __name__ == '__main__':
    app.run(debug=True)
