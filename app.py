from static.data.consultations_to_clean import consultations_to_clean
from flask import Flask, request, jsonify
import pandas as pd
import random
import json
import os

app = Flask(__name__)

@app.route('/')
def main():
    return consultations_to_clean

@app.route('/hospital_data', methods=['GET'])
def consultations():
    try:
        collection = request.args.get('collection')
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
    df_players['clubs'] = df_players['clubs'].map(lambda x: list(map(str.lower, x)))
    df_players_filter = df_players[
        (df_players['clubs'].apply(lambda x: (clubs_list[0] in x) & (clubs_list[1] in x) & (clubs_list[2] in x)))
        & (df_players['name'].str.lower() == player)
    ]

    response = jsonify(
        success=True
    ) if df_players_filter.shape[0] else jsonify(
        success=False
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response

if __name__ == '__main__':
    app.run('0.0.0.0')