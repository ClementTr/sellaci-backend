from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return {
        'name': 'Gabriel Jesus',
        'clubs': [
            'Palmeiras',
            'Manchester City',
            'Arsenal',
        ],
        'nationality': 'Brazil'
    }

if __name__ == '__main__':
    app.run('0.0.0.0')