from __future__ import print_function
import os
from flask import Flask, render_template, redirect, url_for, request
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # OVERRIDE WHEN DEPLOYING APP
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')
    
    @app.route('/test')
    def testapi():

        # CALL API HERE
        print('entered the function')

        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('before')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='nba_5_%43leveland+%43avaliers#sports@group.v.calendar.google.com', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

        events_string = ""

        # Formatting data to be returned to html
        for event in events:
            events_string += event['summary'] + ' ' + event['start'].get('dateTime') + '<br />'

        os.remove('token.pickle')

        return events_string

    @app.route('/webtest')
    def web_test():

        # Use the client_secret.json file to identify the application requesting
        # authorization. The client ID (from that file) and access scopes are required.
        flow = Flow.from_client_secrets_file('client_secret.json', SCOPES)

        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required.
        flow.redirect_uri = 'http://localhost:5000/callback'

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type="offline",
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes="true")

        return redirect(authorization_url)

    @app.route('/callback')
    def callback():
        # gets the value of the code parameter passed in the query string of the callback route
        code = request.args.get('code')
        return 'Code to be used to call apis: ' + code

    return app
