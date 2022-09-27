from flask import Flask
from data import data

app = Flask(__name__)

@app.route('/')
def main():
    return [
        data
    ]

if __name__ == '__main__':
    app.run('0.0.0.0')