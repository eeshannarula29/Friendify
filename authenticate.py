"""The file contains DataHandler object used to handle data

By Eeshan Narula and Avnish Pasari
"""

import csv
from typing import Optional

from firebase_admin.exceptions import FirebaseError

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from custom_exceptions import DataDidNotLoadError, UserDoesNotExistsError
import constants


class DataHandler:
    """Object to handle data

    InstanceAttributes:
    - cred: a certificate used to connect to the firebase server
    - app: an object representing the firebase server
    - db: an object representing firebase firestore database
    """
    cred: credentials.Certificate
    app: firebase_admin.App
    db: firebase_admin.firestore.client

    def __init__(self) -> None:
        self.cred = credentials.Certificate(constants.KEYS)
        self.app = firebase_admin.initialize_app(self.cred)

        self.db = firestore.client()

    def register(self, user_id: str, user_data: dict) -> bool:
        """ register a user to our app

        :param user_id: The user ID of the person
        :param user_data: the data of the user
        :return: whether the process was successful
        """
        if not self.is_user(user_id):

            user_data['userID'] = user_id
            user_data['friends'] = []

            try:
                self.db.collection(constants.COLLECTION).document(user_id).set(user_data)
                return True
            except (ValueError, TypeError, FirebaseError):
                raise DataDidNotLoadError

        return False

    def sign_in(self, user_id: str) -> bool:
        """ Sign in to the app, and return weather the sure successfully signed in

        :param user_id: Id of the user
        :return: whether the process was successful
        """
        return self.is_user(user_id)

    def get_user_data(self, user_id: str) -> dict:
        """Return data for a user as a dictionary

        :param user_id: The user ID of the person
        """
        try:
            user = self.db.collection(constants.COLLECTION).document(user_id).get()

            if user.exists:
                return user.to_dict()
            else:
                raise UserDoesNotExistsError

        except FirebaseError:
            raise DataDidNotLoadError

    def update_user_data(self, user_id: str, user_data: dict) -> bool:
        """ Update the data of a user

        :param user_id: The user ID of the person
        :param user_data: the data of the user
        :return: whether the process was successful
        """
        if self.is_user(user_id):
            try:
                self.db.collection(constants.COLLECTION).document(user_id).set(user_data,
                                                                               merge=True)
                return True
            except (ValueError, TypeError):
                return False
            except FirebaseError:
                raise DataDidNotLoadError
        return False

    def get_all_data(self) -> Optional[list[dict]]:
        """Return all the users data in the firebase database
        """
        data = []

        try:
            entries = self.db.collection(constants.COLLECTION).get()

            for entry in entries:
                if entry.exists:
                    data.append(entry.to_dict())

        except FirebaseError:
            raise DataDidNotLoadError

        return data

    def is_user(self, user_id: str) -> bool:
        """ Return whether the user in in the database

        :param user_id: The user ID of the person
        """
        try:
            user = self.db.collection(constants.COLLECTION).document(user_id).get()

            if user.exists:
                return True
            else:
                return False

        except FirebaseError:
            return False

    def add_friend(self, of: str, to: str) -> None:
        """ Add friend to a user

        :param of: the user who is adding friend
        :param to: the user who is added friend

        Precondition:
        - <of> is a valid user id
        - <to> is a valid user id
        """
        of_data = self.get_user_data(of)
        to_data = self.get_user_data(to)

        if not (to in of_data['friends'] or of in to_data['friends']):
            of_data['friends'].append(to)
            to_data['friends'].append(of)

            self.update_user_data(of, of_data)
            self.update_user_data(to, to_data)

    def un_friend(self, by: str, to: str) -> None:
        """remove friend

        :param by: Id of the user who is un friending
        :param to: Id of the user who is getting un friended

        Precondition:
        - <by> is a valid user id
        - <to> is a valid user id
        """
        by_data = self.get_user_data(by)
        to_data = self.get_user_data(to)

        if to in by_data['friends'] and by in to_data['friends']:
            by_data['friends'].remove(to)
            to_data['friends'].remove(by)

            self.update_user_data(by, by_data)
            self.update_user_data(to, to_data)

    def delete_user(self, user_id: str) -> None:
        """ Delete the user if it exists

        :param user_id: Id of the user
        """
        if self.is_user(user_id):

            user_data = self.get_user_data(user_id)

            for friend in user_data['friends']:
                self.un_friend(by=user_id, to=friend)

            self.db.collection(constants.COLLECTION).document(user_id).delete()

    @staticmethod
    def extract_data_from_csv(filepath: str) -> list[dict]:
        """ Extract and format user data for registration in firebase database

        :param filepath: name of the file containing the data
        :return: formatted data valid for firebase
        """
        try:
            with open(filepath) as file:
                reader = csv.reader(file)

                data = []

                next(reader)

                for row in reader:
                    row.pop(2)
                    row.pop(0)
                    data.append(DataHandler.format_row(row))

                return data

        except FileNotFoundError:
            print('File does not exist')

    @staticmethod
    def format_row(row: list) -> dict:
        """ Format a row of the csv file,
        this is a helper function for extract_data_from_csv function

        :param row: row of the csv file
        """

        return {
            'userID': row[0].split('@')[0],
            'friends': [],

            'movies': row[1].split(';'),
            'music': row[2].split(';'),
            'games': row[3].split(';'),
            'food': row[4].split(';')
        }

    def add_users_from_csv(self, filename: str) -> None:
        """register all the users in the csv file to our app

        :param filename: name of the file containing the data

        Precondition:
        - filename is a valid path to the dataset
        """

        data = DataHandler.extract_data_from_csv(filename)

        for user in data:
            self.register(user['userID'], user)


if __name__ == '__main__':
    # The code below is used to register all the people from the survey we conducted:
    # This code is not meant to be run

    #     data_handler = DataHandler()
    #     data_handler.add_users_from_csv(Constants.DATA)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv',
                          'typing',
                          'firebase_admin',
                          'firebase_admin.exceptions',
                          'custom_exceptions',
                          'constants'],
        'allowed-io': ['extract_data_from_csv'],
        'max-line-length': 100,
        'disable': ['E1136']
    })
