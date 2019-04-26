from __future__ import print_function
import os

from flask import Flask, render_template, session, request
from authlib.flask.client import OAuth
import os.path
import datetime
import json

import app.auth as auth
import app.constants as constants
import app.calendar as calendar
import app.calendar_auth as calendar_auth
import app.database as database

CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'


def create_app(test_config=None):
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # OVERRIDE WHEN DEPLOYING APP
        SECRET_KEY=constants.SECRET_KEY,
    )
    app.debug = True

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

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=auth.AUTH0_CLIENT_ID,
        client_secret=auth.AUTH0_CLIENT_SECRET,
        api_base_url=auth.AUTH0_BASE_URL,
        access_token_url=auth.AUTH0_BASE_URL + '/oauth/token',
        authorize_url=auth.AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile',
        },
    )

    @app.errorhandler(Exception)
    def handle_auth_error(ex):
        return auth.handle_auth_error(ex)

    @app.route('/')
    def index():
        if (session):
            authenticated = True
        else:
            authenticated = False
        return render_template('index.html', authenticated=authenticated)

    @app.route('/about')
    def about():
        if (session):
            authenticated = True
        else:
            authenticated = False
        return render_template('about.html', authenticated=authenticated)

    @app.route('/contact')
    def contact():
        if (session):
            authenticated = True
        else:
            authenticated = False
        return render_template('contact.html', authenticated=authenticated)

    @app.route('/home')
    def home_calendar():

        start = '2019-04-22T19:56:40-04:00'
        end = '2019-05-22T19:56:40-04:00'
        timezone = 'America/New_York'

        usercalendar = calendar.get_calendar(
            session['jwt_payload']['sub'],
            start,
            end,
            timezone
        )

        events = []
        for event in usercalendar:
            id = 0
            events.append({
                'id': id,
                'start': event.starttime,
                'end': event.endtime,
            })
            id = id + 1

        friends = database.get_friends(session['jwt_payload']['sub'])

        return render_template('homeCalendar.html', events=events, friends=friends)

    @app.route('/compare')
    def compare_calendar():
        friendID = request.args.get('id')

        print(friendID)

        start = '2019-04-22T19:56:40-04:00'
        end = '2019-05-22T19:56:40-04:00'
        timezone = 'America/New_York'

        compared_calendar = calendar.compare_user_calendars(
            session['jwt_payload']['sub'],
            friendID,
            start,
            end,
            timezone
        )

        events = []
        for event in compared_calendar:
            id = 0
            events.append({
                'id': id,
                'start': event.starttime,
                'end': event.endtime,
                'rendering': 'background'
            })
            id = id + 1

        friends = database.get_friends(session['jwt_payload']['sub'])

        return render_template('compareCalendar.html', events=events, friends=friends)        


    @app.route('/callback')
    def callback_handling():
        return auth.callback_handling(auth0)

    @app.route('/credentials')
    def load_credentials():
        return auth.load_credentials()

    @app.route('/login')
    def login():
        return auth.login(auth0)

    @app.route('/dashboard')
    @auth.requires_auth
    def dashboard():
        return auth.dashboard()

    @app.route('/logout')
    def logout():
        return auth.logout(auth0)

    @app.route('/webtest')
    def web_test():

        start = "2019-04-22T19:56:40-04:00"
        end = "2019-05-22T19:56:40-04:00"
        timezone = "America/New_York"

        usercalendar = calendar.compare_user_calendars(session['jwt_payload']['sub'], session['jwt_payload']['sub'], start, end, timezone)

        freebusy_string = ""
        for event in usercalendar:
            freebusy_string += event.starttime + ' - ' + event.endtime + '<br />'

        return freebusy_string

    @app.route('/authorize')
    def authorize():
        return calendar_auth.authorize()

    @app.route('/oauth2callback')
    def oauth2callback():
        return calendar_auth.oauth2callback()

    @app.route('/revoke')
    def revoke():
        return calendar_auth.revoke()

    @app.route('/clear')
    def clear_credentials():
        return calendar_auth.clear_credentials()

    return app
