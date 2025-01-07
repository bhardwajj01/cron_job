from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import re

app = Flask(__name__)

# The file token.json stores the user's access and refresh tokens,
# and is created automatically when the authorization flow completes for the first time.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens,
    # and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_event(service, summary, start_time, end_time, full_name, email, mobile_number):
    event = {
        'summary': 'Appointments',
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
        'description': f'Booked by: {full_name}\nEmail: {email}\nMobile: {mobile_number}',
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')


@app.route('/create_event', methods=['POST'])
def create_google_calendar_event():
    try:
        # Assuming you receive form data in the request body
        summary = request.form.get('summary')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        mobile_number = request.form.get('mobile_number')

        print(f'summary: {summary}')
        print(f'start_time: {start_time}')
        print(f'end_time: {end_time}')
        print(f'full_name: {full_name}')
        print(f'email: {email}')
        print(f'mobile_number: {mobile_number}')

        # Your existing Google Calendar code
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)

        create_event(service, summary, start_time, end_time, full_name, email, mobile_number)

        return jsonify({"message": "Event created successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
