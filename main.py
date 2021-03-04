import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import Constants

import Screen

if __name__ == '__main__':

    cred = credentials.Certificate(Constants.keysFile)
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    current_screen = Screen.HomeScreen(db)

    while current_screen is not None:
        current_screen = current_screen.show()
