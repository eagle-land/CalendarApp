# /auth.py

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
import http.client
import mysql.connector

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode

from . import constants

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

#app = Flask(__name__)
"""
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='F2d17N80wx3AlRKW8ZdEdItmktPUmDgR',
    client_secret='XNRzQrSkN0J30Xgh2L36LkGR-fJ6h4z0xigAUk7rnixyadc9TZOuptCvzipEmRka',
    api_base_url='https://shared-skies.auth0.com',
    access_token_url='https://shared-skies.auth0.com/oauth/token',
    authorize_url='https://shared-skies.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)
"""

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
    userID = userinfo["sub"]


    # Store the user information in flask session.
    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    #needs to go to webtest to get credentials from google and store info in database
    mySql_output()
    return redirect('/dashboard')

def login(auth0):
    #env['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
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

def mySql_output():
    connection = mysql.connector.connect(
            user='eagleland', password='eagleland',
            host='eaglelanddb.cfvr1klcoyxo.us-east-1.rds.amazonaws.com',
            port=3306, database = 'eaglelandDB')
    mycursor = connection.cursor()
    googleToken = session['credentials']['token']
    googleRefreshToken = session['credentials']['refresh_token']
    userID = session['jwt_payload']['sub']
    nickname = session['jwt_payload']['nickname']
    
    #need to add method to verify entry doesnt exist yet, otherwise causes errors
    SQLquery = "INSERT INTO user(google_token, google_refresh_token, ID, nickname) VALUES (%s, %s, %s, %s)"
    values = (googleToken, googleRefreshToken, userID, nickname)

    mycursor.execute(SQLquery, values)
    connection.commit()
    mycursor.close
    print('data sent to amazon RDS')


def generate_access_token():
    conn = http.client.HTTPSConnection("shared-skies.auth0.com")
    payload = "{\"client_id\":\"F2d17N80wx3AlRKW8ZdEdItmktPUmDgR\",\"client_secret\":\"XNRzQrSkN0J30Xgh2L36LkGR-fJ6h4z0xigAUk7rnixyadc9TZOuptCvzipEmRka\",\"audience\":\"https://shared-skies.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    authTokenResponseString = data.decode("utf-8")
    authJson = json.loads(authTokenResponseString)
    return authJson["access_token"]