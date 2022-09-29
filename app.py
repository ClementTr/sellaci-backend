from static.data.consultations_to_clean import consultations_to_clean
from flask import Flask, request
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

if __name__ == '__main__':
    app.run('0.0.0.0')