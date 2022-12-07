import os

PYREBASE_CREDENTIALS = {
    "apiKey": os.environ.get('FIREBASE_API_KEY'),
    "authDomain": "sellaci.firebaseapp.com",
    "databaseURL": "",
    "storageBucket": "sellaci.appspot.com"
}

FIREBASE_CREDENTIALS = {
    "type": "service_account",
    "project_id": os.environ.get('GOOGLE_PROJECT_ID'),
    "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-w8zsd%40sellaci-367920.iam.gserviceaccount.com"
}