from config import URL_FRONT, PYREBASE_CREDENTIALS, FIREBASE_CREDENTIALS
from flask import Flask, request, jsonify, session, redirect
from firebase_admin import firestore, credentials
from flask_cors import CORS, cross_origin
import firebase_admin
import pandas as pd
import pyrebase
import requests
import random
import json
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

firebase = pyrebase.initialize_app(PYREBASE_CREDENTIALS)
auth = firebase.auth()
app.secret_key = 'hdekspzlejdn'

firebase_admin.initialize_app(credential=credentials.Certificate(FIREBASE_CREDENTIALS))
db = firestore.client()

USER_ID = ''

@app.route('/')
def main():
    return {'status': 'Welcome on Sellaci platform'}

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            auth.create_user_with_email_and_password(email, password)
            db.collection('users').document(email).set({'email': email})
            db.collection('users').document(email).update({"nb_logins": firestore.Increment(1)})
            USER_ID = email
            return redirect(URL_FRONT + 'play.html')
        except requests.HTTPError as e:
            error = json.loads(e.args[1])['error']['message']
            return redirect(f'{URL_FRONT}signup.html?error={error}')
    return redirect(URL_FRONT + 'signup.html')

@app.route('/login', methods=['POST', 'GET'])
@cross_origin()
def login():
    if 'user' in session:
        return redirect(URL_FRONT + 'play.html')
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            try:
                auth.sign_in_with_email_and_password(email, password)
                db.collection('users').document(email).update({"nb_logins": firestore.Increment(1)})
                return redirect(URL_FRONT + 'play.html')
            except Exception as e:
                return redirect(URL_FRONT + 'login.html')
        else:
            return redirect(URL_FRONT + 'login.html')

@app.route('/reset_password',  methods=['POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        auth.send_password_reset_email(email)
    return redirect(URL_FRONT + 'login.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(URL_FRONT + 'login.html')

@app.route('/test',  methods=['GET', 'POST'])
@cross_origin()
def test():
    if request.method == 'POST':
        name = request.form.get('name')
        print(name)
        print(session)
        print(USER_ID)
        db.collection('users').document(USER_ID).update({"players_find": firestore.ArrayUnion([name])})
        return redirect(URL_FRONT + 'play.html')


@app.route('/random_player', methods=['GET'])
@cross_origin()
def random_player():
    filename = os.path.join(app.static_folder, f'data/players.json')
    with open(filename) as players_file:
        players_data = json.load(players_file)
        random_player = random.choice(players_data)
        response = jsonify(random_player)
    return response

@app.route('/players_with_clubs', methods=['GET'])
@cross_origin()
def get_players_with_clubs():
    clubs = request.args.get('clubs').lower()
    player = request.args.get('player').lower()

    clubs_list = clubs.split(',')
    filename = os.path.join(app.static_folder, f'data/players.json')
    df_players = pd.read_json(filename)
    df_players['Teams'] = df_players['Teams'].map(lambda x: list(map(str.lower, x)))
    df_players_filter = df_players[
        (df_players['Teams'].apply(lambda x: (clubs_list[0] in x) & (clubs_list[1] in x) & (clubs_list[2] in x)))
        & (df_players['ShortName'].str.lower() == player)
    ]

    response = jsonify(
        success=True
    ) if df_players_filter.shape[0] else jsonify(
        success=False
    )
    return response

if __name__ == '__main__':
    app.run()  # run our Flask app
