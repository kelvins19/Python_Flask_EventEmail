from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from task import *
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import json
import datetime
import atexit

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(check_timestamp, trigger="interval", seconds=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def home():
    return 'Home'

@app.route('/save_email', methods=["POST"])
def save_email():
    db = sqlite3.connect('email.db')
    c = db.cursor()

    input = request.get_json(force=True)

    c.execute("INSERT INTO email (event_id, email_subject, email_content, timestamp, is_sent) VALUES (?, ?, ?, ?, 0)", (input['event_id'], input['email_subject'], input['email_content'], input['timestamp']))
    db.commit()
    return json.dumps("Record was successfully saved")

@app.route('/get-email-recipients', methods=['GET'])
def get_email_recipients():
    c = sqlite3.connect("email.db").cursor()
    c.execute("SELECT * FROM email_recipients")
    data = c.fetchall()
    return jsonify(data)

@app.route('/get-email-recipients/<event_id>', methods=['GET'])
def get_email_recipients_by_event_id(event_id):
    c = sqlite3.connect("email.db").cursor()
    c.execute("SELECT * FROM email_recipients WHERE event_id=?", (event_id,))
    data = c.fetchall()
    return jsonify(data)