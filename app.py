from static.data.consultations_to_clean import consultations_to_clean
from flask import Flask, request, jsonify, session, redirect
from config import URL_FRONT, FIREBASE_CREDENTIALS
import pandas as pd
import pyrebase
import requests
import random
import json
import os

app = Flask(__name__)
firebase = pyrebase.initialize_app(FIREBASE_CREDENTIALS)
auth = firebase.auth()
app.secret_key = 'secret'

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
            return redirect(URL_FRONT + 'play.html')
        except requests.HTTPError as e:
            error = json.loads(e.args[1])['error']['message']
            return redirect(f'{URL_FRONT}signup.html?error={error}')
    return redirect(URL_FRONT + 'signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        response = jsonify(status='logged')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return redirect(URL_FRONT + 'play.html')
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            try:
                auth.sign_in_with_email_and_password(email, password)
                session['user'] = email
                return redirect(URL_FRONT + 'play.html')
            except Exception as e:
                return redirect(URL_FRONT + 'login.html')
        else:
            return redirect(URL_FRONT + 'login.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(URL_FRONT + 'login.html')

@app.route('/hospital_data', methods=['GET'])
def consultations():
    try:
        collection = request.form.get('collection')
        data = []
        filename = os.path.join(app.static_folder, f'data/{collection}.json')
        with open(filename) as blog_file:
            data = json.load(blog_file)
        return data
    except:
        return [{'server-status': 'error'}]


@app.route('/random_player', methods=['GET'])
def random_player():
    filename = os.path.join(app.static_folder, f'data/players.json')
    with open(filename) as players_file:
        players_data = json.load(players_file)
        random_player = random.choice(players_data)
        response = jsonify(random_player)
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/players_with_clubs', methods=['GET'])
def get_players_with_clubs():
    clubs = request.args.get('clubs').lower()
    player = request.args.get('player').lower()

    clubs_list = clubs.split(',')
    filename = os.path.join(app.static_folder, f'data/players.json')
    df_players = pd.read_json(filename)
    df_players['Teams'] = df_players['Teams'].map(lambda x: list(map(str.lower, x)))
    df_players_filter = df_players[
        (df_players['Teams'].apply(lambda x: (clubs_list[0] in x) & (clubs_list[1] in x) & (clubs_list[2] in x)))
        & (df_players['Name'].str.lower() == player)
    ]

    response = jsonify(
        success=True
    ) if df_players_filter.shape[0] else jsonify(
        success=False
    )
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == '__main__':
    app.run()  # run our Flask app
