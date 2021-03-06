# /auth.py

from functools import wraps
import json
from werkzeug.exceptions import HTTPException
import http.client

from dotenv import load_dotenv, find_dotenv
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from six.moves.urllib.parse import urlencode

import app.constants as constants
import app.database as database


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = constants.AUTH0_CALLBACK_URL
AUTH0_CLIENT_ID = constants.AUTH0_CLIENT_ID
AUTH0_CLIENT_SECRET = constants.AUTH0_CLIENT_SECRET
AUTH0_DOMAIN = constants.AUTH0_DOMAIN
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = constants.AUTH0_AUDIENCE
if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = AUTH0_BASE_URL + '/userinfo'


def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


def callback_handling(auth0):
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    return redirect('/credentials')


def load_credentials():
    if 'credentials' not in session:
        # checks if user is in database, pulls credentials if so
        if database.check_user_exists(session['jwt_payload']['sub']) == True:
            session['credentials'] = database.load_database_creds(session['jwt_payload']['sub'])
        else:
            # otherwise has user authorize with google
            return redirect('/authorize')

    # if user isn't in database they are added here
    if database.check_user_exists(session['jwt_payload']['sub']) == False:
        database.add_to_database()
    return redirect('/home')


def login(auth0):
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


def logout(auth0):
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('index', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


def dashboard():
    return render_template('dashboard.html',
                           userinfo=session[constants.PROFILE_KEY],
                           userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4))


def generate_access_token():
    # Call to get access token from auth0 to use their "management API"
    conn = http.client.HTTPSConnection("shared-skies.auth0.com")
    payload = "{\"client_id\":\"%s\",\"client_secret\":\"%s\",\"audience\":\"https://shared-skies.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}" % (constants.AUTH0_CLIENT_ID, constants.AUTH0_CLIENT_SECRET)
    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    authTokenResponseString = data.decode("utf-8")
    authJson = json.loads(authTokenResponseString)
    # Returns the access token
    return authJson["access_token"]
