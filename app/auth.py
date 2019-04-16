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
    #needs to go to webtest to get credentials from google and store info in database

    return redirect('/webtest')

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



def generate_access_token():
    #call to get access token from auth0 to use their "management API"
    conn = http.client.HTTPSConnection("shared-skies.auth0.com")
    payload = "{\"client_id\":\"%s\",\"client_secret\":\"%s\",\"audience\":\"https://shared-skies.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}" % (constants.AUTH0_CLIENT_ID, constants.AUTH0_CLIENT_SECRET)
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    authTokenResponseString = data.decode("utf-8")
    authJson = json.loads(authTokenResponseString)
    #returns the access token
    return authJson["access_token"]


def add_to_database():
    connection = mysql.connector.connect(
            user=constants.USER, password=constants.PASSWORD,
            host=constants.HOST,
            port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()

    #sets user information variables
    googleToken = session['credentials']['token']
    googleRefreshToken = session['credentials']['refresh_token']
    userID = session['jwt_payload']['sub']
    nickname = session['jwt_payload']['nickname']
    #query to add data into table
    SQLquery = "REPLACE INTO user(google_token, google_refresh_token, ID, nickname) VALUES (%s, %s, %s, %s)"
    values = (googleToken, googleRefreshToken, userID, nickname)
    #executes query and commits it to database
    mycursor.execute(SQLquery, values)
    connection.commit()
    mycursor.close
    print('data sent to amazon RDS')

#method uses ID in session to verify existence in table
def check_user_exists():
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    #query to check if ID exists in our database
    query = 'SELECT EXISTS(SELECT * FROM eaglelandDB.user WHERE ID = "%s")' % (session['jwt_payload']['sub'])
    mycursor.execute(query)
    result = mycursor.fetchone()
    mycursor.close
    #returns boolean value(true if user exists, else false)
    return (result[0] == 1)

#this function will be useful when users are searching for friends via nickname
def check_user_exists_nickname(nickname):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    #query to check if ID exists in our database
    query = 'SELECT EXISTS(SELECT * FROM eaglelandDB.user WHERE nickname = "%s")' % (nickname)
    mycursor.execute(query)
    result = mycursor.fetchone()
    mycursor.close
    #returns boolean value(true if user exists, else false)
    return (result[0] == 1)

def load_database_creds():
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    #query to get user credentials 
    query = 'SELECT * FROM eaglelandDB.user WHERE ID = "%s"' % (session['jwt_payload']['sub'])
    mycursor.execute(query)
    result = mycursor.fetchone()
    mycursor.close
    #extracts token and refresh token from SQL response
    token = result[2]
    refreshToken = result[3]

    #gets secret info from client secret file and stores credentials in flask session
    with open('client_secret.json') as json_file:  
        data = json.load(json_file)
    session['credentials'] = {
        'client_id': data['web']['client_id'],
        'client_secret': data['web']['client_secret'],
        'refresh_token': refreshToken,
        'scopes': ['https://www.googleapis.com/auth/calendar.readonly'],
        'token': token,
        'token_uri': 'https://oauth2.googleapis.com/token'
    }
def check_if_friends (friendID):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    #query to return if a user friendship exists
    query = 'SELECT EXISTS(SELECT * FROM eaglelandDB.friend WHERE user1 = "%s" AND user2 = "%s" AND pending = 0)' % (session['jwt_payload']['sub'], friendID)
    mycursor.execute(query)
    result = mycursor.fetchone()
    mycursor.close
    #returns true if used is friends with target, else false
    return (result[0] == 1)

def search_user_in_database(nickname):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    #query to get user information
    query = 'SELECT * FROM eaglelandDB.user WHERE nickname = "%s"' % (nickname)
    mycursor.execute(query)
    result = mycursor.fetchone()
    mycursor.close
    #returns userID, can be rolled into friend request functions
    return result[0]

def request_friend(friendID):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    #query to store user friend request and mark it pending
    query = 'INSERT INTO friend VALUES ("%s", "%s", 1)' % (session['jwt_payload']['sub'], friendID)
    mycursor.execute(query)
    query2 = 'INSERT INTO friend VALUES ("%s", "%s", 1)' % (friendID, session['jwt_payload']['sub'])
    mycursor.execute(query2)
    connection.commit()
    mycursor.close

def accept_friend():
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    #query to change pending value to 0 when accepted
    query = 'REPLACE INTO friend (pending) VALUES (0)'
    mycursor.execute(query)
    query2 = 'REPLACE INTO friend (pending) VALUES (0)'
    mycursor.execute(query2)
    connection.commit()
    mycursor.close

    
