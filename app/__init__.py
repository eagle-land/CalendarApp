from __future__ import print_function
import os
from flask import Flask, render_template, redirect, url_for, request, session
import flask
from authlib.flask.client import OAuth
import datetime
import pickle
import os.path
import requests
from . import auth
from . import constants

import googleapiclient.discovery
import google_auth_oauthlib.flow
import google.oauth2.credentials
#from google.auth.transport.requests import Request

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
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/calendar')
    def calendar():
        return render_template('calendar.html')

    @app.route('/callback')
    def callback_handling():
        return auth.callback_handling(auth0)

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
        print(session)
        if 'credentials' not in flask.session:
            print('credentials werent in flask session')
            if (auth.check_user_exists() == True):
                auth.load_database_creds()
            else:
                return flask.redirect('authorize')
    
        
        if (auth.check_user_exists() == False):
            auth.mySql_output()


        # Load credentials from the session.
        credentials = google.oauth2.credentials.Credentials(
            **flask.session['credentials'])

        calendar = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, credentials=credentials)

        now = "2019-04-10T00:00:00.0-04:00"
        end = "2019-04-17T00:00:00.0-04:00"
        body = {
            "timeMin": now,
            "timeMax": end,
            "timeZone": "America/New_York",
            "items": [
                {
                    "id": "primary"
                }
            ],
        }

        response = calendar.freebusy().query(body=body).execute()

        freebusy_string = ""

        if not response:
            print('Error.')
        calendars = response['calendars']
        calendar = calendars[body['items'][0]['id']]
        for busytimes in calendar:
            index = 0
            for busy in calendar[busytimes]:
                freebusy_string += calendar[busytimes][index]['start'] + ' - ' + calendar[busytimes][index][
                    'end'] + '<br />'
                index += 1

        # Save credentials back to session in case access token was refreshed.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        flask.session['credentials'] = credentials_to_dict(credentials)
        return freebusy_string

    @app.route('/authorize')
    def authorize():
        # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES)

        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required.
        flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type="offline",
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes="true")

        # Store the state so the callback can verify the auth server response.
        flask.session['state'] = state

        return flask.redirect(authorization_url)

    @app.route('/oauth2callback')
    def oauth2callback():
        # Specify the state when creating the flow in the callback so that it can
        # verified in the authorization server response.
        state = flask.session['state']

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
        flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = flask.request.url
        flow.fetch_token(authorization_response=authorization_response)

        # Store credentials in the session.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        credentials = flow.credentials
        flask.session['credentials'] = credentials_to_dict(credentials)

        return flask.redirect(flask.url_for('web_test'))

    @app.route('/revoke')
    def revoke():
        if 'credentials' not in flask.session:
            return ('You need to <a href="/authorize">authorize</a> before ' +
                    'testing the code to revoke credentials.')

        credentials = google.oauth2.credentials.Credentials(
            **flask.session['credentials'])

        revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
                               params={'token': credentials.token},
                               headers={'content-type': 'application/x-www-form-urlencoded'})

        status_code = getattr(revoke, 'status_code')
        if status_code == 200:
            return ('Credentials successfully revoked.')
        else:
            return ('An error occurred.')

    @app.route('/clear')
    def clear_credentials():
        if 'credentials' in flask.session:
            del flask.session['credentials']
        return ('Credentials have been cleared.<br><br>')

    def credentials_to_dict(credentials):
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

    return app