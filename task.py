from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import sqlite3
import json
import datetime
from celery_utils import get_celery_app_instance

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# celery app instance
celery = get_celery_app_instance(app)

@celery.task
def send_email(emailAddress, emailSubject, emailContent):
    msg = Message(emailSubject, sender = 'kelvin.s.ks19@gmail.com', recipients = [emailAddress])
    msg.body = emailContent
    mail.send(msg)

# Function to check on the timestamp and send email
def check_timestamp():
    c = sqlite3.connect("email.db").cursor()
    c.execute("SELECT * FROM email WHERE is_sent = 0")
    data = c.fetchall()

    for i in data:
        emailId = i[0]
        eventId = i[1]
        emailSubject = i[2]
        emailContent = i[3]
        timestamp = i[4]

        if datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') == datetime.datetime.now():
            c.execute("SELECT * FROM email_recipients WHERE event_id=? AND is_sent=0", (eventId,))
            emailRecipients = c.fetchall()

            db = sqlite3.connect('email.db')
            c = db.cursor()
            for j in emailRecipients:
                emailAddress = j[2]

                print("Send email to " + emailAddress)
                send_email().delay(emailAddress, emailSubject, emailContent)
                print("Email sent to " + emailAddress)

                c.execute("UPDATE email_recipients SET is_sent = 1 WHERE event_id = ? and id = ?", (eventId, j[0]))
                db.commit()

            c.execute("UPDATE email SET is_sent = 1 WHERE event_id = ?", (eventId,))
            db.commit()
    print("Scheduler running")
