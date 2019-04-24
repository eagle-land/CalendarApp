import mysql.connector
import json
import os
import sys
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

import http.client
import urllib.parse

import app.constants as constants

basedir = os.path.abspath(os.path.dirname(__file__))
if sys.platform == 'win32':
    CLIENT_SECRETS_FILE = basedir+'\\\\client_secret.json'
else:
    CLIENT_SECRETS_FILE = basedir + '/client_secret.json'


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
    email = get_user_email(generate_access_token())
    #query to add data into table
    SQLquery = "REPLACE INTO user(google_token, google_refresh_token, ID, nickname, email) VALUES (%s, %s, %s, %s, %s)"
    values = (googleToken, googleRefreshToken, userID, nickname, email)
    #executes query and commits it to database
    mycursor.execute(SQLquery, values)
    connection.commit()
    mycursor.close
    print('data sent to amazon RDS')


# method uses ID in session to verify existence in table
def check_user_exists(userID):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    # query to check if ID exists in our database
    query = 'SELECT EXISTS(SELECT * FROM eaglelandDB.user WHERE ID = "%s")' % (userID)
    mycursor.execute(query)
    result = mycursor.fetchone()
    mycursor.close
    # returns boolean value(true if user exists, else false)
    return (result[0] == 1)


# this function will be useful when users are searching for friends via nickname
def check_user_exists_nickname(nickname):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    # query to check if ID exists in our database
    query = 'SELECT EXISTS(SELECT * FROM eaglelandDB.user WHERE nickname = "%s")' % (nickname)
    mycursor.execute(query)
    result = mycursor.fetchone()
    mycursor.close
    # returns boolean value(true if user exists, else false)
    return result[0] == 1


def load_database_creds(userid):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    # query to get user credentials
    query = 'SELECT * FROM eaglelandDB.user WHERE ID = "%s"' % (userid)
    mycursor.execute(query)
    result = mycursor.fetchone()
    mycursor.close
    # extracts token and refresh token from SQL response
    token = result[2]
    refreshToken = result[3]

    # gets secret info from client secret file and stores credentials in flask session
    with open(CLIENT_SECRETS_FILE) as json_file:  
        data = json.load(json_file)
    return {
        'client_id': data['web']['client_id'],
        'client_secret': data['web']['client_secret'],
        'refresh_token': refreshToken,
        'scopes': ['https://www.googleapis.com/auth/calendar.readonly'],
        'token': token,
        'token_uri': 'https://oauth2.googleapis.com/token'
    }

    # gets secret info from client secret file and stores credentials in flask session
    with open(CLIENT_SECRETS_FILE) as json_file:  
        data = json.load(json_file)
    session['credentials'] = {
        'client_id': data['web']['client_id'],
        'client_secret': data['web']['client_secret'],
        'refresh_token': refreshToken,
        'scopes': ['https://www.googleapis.com/auth/calendar.readonly'],
        'token': token,
        'token_uri': 'https://oauth2.googleapis.com/token'
    }


def check_if_friends (userID, friendID):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    # query to return if a user friendship exists
    query = 'SELECT EXISTS(SELECT * FROM eaglelandDB.friend WHERE user1 = "%s" AND user2 = "%s" AND pending = 0)' % (userID, friendID)
    mycursor.execute(query)
    result = mycursor.fetchone()
    mycursor.close
    # returns true if used is friends with target, else false
    return (result[0] == 1)


def search_user_by_email(email):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    # query to get user information
    query = 'SELECT * FROM eaglelandDB.user WHERE email = "%s"' % (email)
    mycursor.execute(query)
    result = mycursor.fetchone()
    mycursor.close
    # returns userID, can be rolled into friend request functions
    return result[0]


def request_friend(friendID):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    # query to store user friend request and mark it pending
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
    # query to change pending value to 0 when accepted
    query = 'REPLACE INTO friend (pending) VALUES (0)'
    mycursor.execute(query)
    query2 = 'REPLACE INTO friend (pending) VALUES (0)'
    mycursor.execute(query2)
    connection.commit()
    mycursor.close


def get_friends(userID):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    # query to change pending value to 0 when accepted
    query = 'SELECT user2 FROM friend WHERE user1 = "%s" AND pending = 0' % (userID)
    mycursor.execute(query)
    friendlist = []
    for x in mycursor.fetchall():
        friendlist.append(x[0])
    
    
    friendDict = {}
    for userID in friendlist:
        getNickname = 'SELECT nickname FROM user WHERE ID = "%s"' % (userID)
        mycursor.execute(getNickname)
        value = mycursor.fetchone()
        friendDict[userID] = value[0]


    # returns list of accepted friend userIDs from friend table
    return friendDict


def get_pending_friends(user):
    connection = mysql.connector.connect(
        user=constants.USER, password=constants.PASSWORD,
        host=constants.HOST,
        port=constants.PORT, database=constants.DATABASE)
    mycursor = connection.cursor()
    # query to change pending value to 0 when accepted
    query = 'SELECT user2 from friend where user1 = "%s" AND pending = 1' % (user)
    mycursor.execute(query)
    friendlist = []
    for x in mycursor.fetchall():
        friendlist.append(x[0])
    # returns list of pending friend userIDs from friend table


    friendDict = {}
    for userID in friendlist:
        getNickname = 'SELECT nickname FROM user WHERE ID = "%s"' % (userID)
        mycursor.execute(getNickname)
        value = mycursor.fetchone()
        friendDict[userID] = value[0]
    return friendDict


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


def get_user_email(token):
    #connects to auth0 api server to pull user email
    conn = http.client.HTTPSConnection("shared-skies.auth0.com")
    headers = { 'authorization': "Bearer %s" % (token) }
    requestString = urllib.parse.quote(session['jwt_payload']['sub'])
    conn.request("GET", "/api/v2/users/%s" % (requestString), headers=headers)
    res = conn.getresponse()
    data = res.read()
    #conveerts server response to json and extracts email string
    response = json.loads(data.decode("utf-8"))
    print(response["email"])
    return response["email"]

