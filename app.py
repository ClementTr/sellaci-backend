from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return [
        {
            'name': 'Gabriel Jesus',
            'clubs': [
                'Palmeiras',
                'Manchester City',
                'Arsenal FC',
            ],
            'nationality': 'Brazil',
        },
        {
            'name': 'Martin Ødegaard',
            'clubs': [
                'Real Madrid',
                'Real Sociedad',
                'Arsenal FC',
            ],
            'nationality': 'Norwegian',
        },
    ]

if __name__ == '__main__':
    app.run('0.0.0.0')