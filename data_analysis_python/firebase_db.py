import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./intnoti-cc829-firebase-adminsdk-4abey-00f37cb945.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
