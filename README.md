# Flask API

This project is a simple web application that is able to serve a POST endpoint. The main function of the endpoint is to store in the database an email for a particular group of recipients. The emails are then to be sent ​automatically​ at a later time.

## Stack
- Python v3.8
- SQLite 3 as the database

## How to run this application
1. Open terminal
2. Run `source bin/activate`
3. Run `flask run`. The scheduler to check on the timestamp will also run when we run this command.
4. The application will run in `127.0.0.1:5000`

## API Lists
- POST 127.0.0.1:5000/save_email
The purpose of this API is to save the email that will be sent in the later date based on timestamp that is given in the request parameters.

Request parameters:
> {
    "event_id": 1,
    "email_subject": "Email Subject",
    "email_content": "Hello World",
    "timestamp": "2022-12-14 16:30:20"
}

- GET 127.0.0.1:5000/get-email-recipients
The purpose is to return all the list of recipients email address

- GET 127.0.0.1:5000/get-email-recipients/{event_id}
The purpose is to return all the recipients email address based on certain event_id

## Need to be added / implemented
- Mailer service to enable send email functionality
- Queue task to check on which email need to be sent based on timestamp