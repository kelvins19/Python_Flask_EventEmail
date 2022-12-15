from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import sqlite3
import json
import datetime

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

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

        if datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') <= datetime.datetime.now():
            # fetch email addresses based on event_id
            c.execute("SELECT * FROM email_recipients WHERE event_id=? AND is_sent=0", (eventId,))
            emailRecipients = c.fetchall()

            for j in emailRecipients:
                emailAddress = j[2]

                # Logic to send email address here
                print("Send email to " + emailAddress)
                # msg = Message(emailSubject, sender = 'kelvin.s.ks19@gmail.com', recipients = [emailAddress])
                # msg.body = emailContent
                # mail.send(msg)
                print("Email sent to " + emailAddress)

                # update is_sent flag on email_recipients table
                c.execute("UPDATE email_recipients SET is_sent = 1 WHERE event_id = ? and id = ?", (eventId, j[0]))

            # update is_sent flag on email table
            db = sqlite3.connect('email.db')
            c = db.cursor()
            c.execute("UPDATE email SET is_sent = 1 WHERE event_id = ?", (eventId,))
            db.commit()
    print("Scheduler running")
