import pyrebase
import requests

from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from CustomExceptions import DataDidNotLoadError, UserDoesNotExistsError, UserExitsError

import Constants

import csv

from typing import Optional


class Auth:

    def __init__(self) -> None:
        self.app = pyrebase.initialize_app(Constants.PyrebaseConfig)
        self.auth = self.app.auth()

    def create_user(self, userID: str, password: str) -> bool:
        try:
            auth.create_user(uid=userID, email=userID + '@friendify.com', password=password)
            return True
        except (ValueError, FirebaseError):
            return False

    def signed_in(self, userID: str, password: str) -> bool:
        try:
            self.auth.sign_in_with_email_and_password(userID + '@friendify.com', password)
            return True
        except requests.exceptions.HTTPError:
            return False

    def is_user(self, userID: str) -> bool:
        try:
            auth.get_user(userID)
            return True
        except (ValueError, auth.UserNotFoundError):
            return False
        except FirebaseError:
            raise DataDidNotLoadError

    def delete_user(self, userID: str) -> bool:
        try:
            auth.delete_user(userID)
            return True
        except ValueError:
            return False
        except FirebaseError:
            raise DataDidNotLoadError


class DataHandler:

    def __init__(self) -> None:
        self.cred = credentials.Certificate(Constants.keysFile)
        self.app = firebase_admin.initialize_app(self.cred)

        self.db = firestore.client()

        self.auth = Auth()

    def register(self, userID: str, password: str, user_data: dict) -> bool:
        """ register a user to our app

        :param password: user's password
        :param userID: The user ID of the person
        :param user_data: the data of the user
        """
        if not self.auth.is_user(userID):

            user_data['userID'] = userID
            user_data['friends'] = []

            if self.auth.create_user(userID, password):

                try:
                    self.db.collection(Constants.collectionName).document(userID).set(user_data)
                    return True
                except (ValueError, TypeError, FirebaseError):
                    self.auth.delete_user(userID)
                    raise DataDidNotLoadError

        return False

    def sign_in(self, userID: str, password: str) -> bool:
        """ Sign in to the app, and return weather the sure successfully signed in

        :param userID: Id of the user
        :param password: password of the user
        """
        return self.auth.signed_in(userID, password)

    def get_user_data(self, userID: str) -> dict:
        """Return data for a user

        :param userID: The user ID of the person
        """
        try:
            user = self.db.collection(Constants.collectionName).document(userID).get()

            if user.exists:
                return user.to_dict()
            else:
                raise UserDoesNotExistsError

        except FirebaseError:
            raise DataDidNotLoadError

    def update_user_data(self, userID: str, user_data: dict) -> bool:
        """ Update the data of a user

        :param userID: The user ID of the person
        :param user_data: the data of the user
        """
        if self.is_user(userID):
            try:
                self.db.collection(Constants.collectionName).document(userID).set(user_data,
                                                                                  merge=True)
                return True
            except (ValueError, TypeError):
                return False
            except FirebaseError:
                raise DataDidNotLoadError

    def get_all_data(self) -> Optional[list[dict]]:
        """Return all the users data in the firebase database
        """
        data = []

        try:
            entries = self.db.collection(Constants.collectionName).get()

            for entry in entries:
                if entry.exists:
                    data.append(entry.to_dict())

        except FirebaseError:
            raise DataDidNotLoadError

        return data

    def is_user(self, userID: str) -> bool:
        """ Return whether the user in in the database

        :param userID: The user ID of the person
        """
        return self.auth.is_user(userID)

    def add_friend(self, of: str, to: str) -> None:
        """ Add friend to a user

        :param of: the user who is adding friend
        :param to: the user who is added friend
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
        """
        by_data = self.get_user_data(by)
        to_data = self.get_user_data(to)

        if to in by_data['friends'] and by in to_data['friends']:
            by_data['friends'].remove(to)
            to_data['friends'].remove(by)

            self.update_user_data(by, by_data)
            self.update_user_data(to, to_data)

    def delete_user(self, userID: str) -> None:
        """ Delete the user if it exists

        :param userID: Id of the user
        """
        if self.is_user(userID):

            user_data = self.get_user_data(userID)

            for friend in user_data['friends']:
                self.un_friend(by=userID, to=friend)

            self.db.collection(Constants.collectionName).document(userID).delete()
            self.auth.delete_user(userID)

    def generate_graph_for_user(self, userID: str, depth: int) -> list[dict]:
        """ Generate data for plotting a graph for al user

        :param userID: the ID of the user
        :param depth: depth of the network
        :return: list of dicts contacting data of the graph
        """

        if depth == 0:
            return [{'data': {'id': userID, 'label': userID}}]
        else:
            data_so_far = [{'data': {'id': userID, 'label': userID}}]

            for friend in self.get_user_data(userID)['friends']:
                data_so_far.extend(self.generate_graph_for_user(friend, depth - 1))
                data_so_far.extend([{'data': {'source': userID, 'target': friend}}])

            return data_so_far

    def generate_network(self) -> list[dict]:
        """ Generate graph for the whole app

        :return: list of dicts contacting data of the graph
        """
        data = []

        users = self.get_all_data()

        for user in users:
            data.append({'data': {'id': user['userID'], 'label': user['userID']}})

        for user in users:
            for friend in user['friends']:
                data.append({'data': {'source': user['userID'], 'target': friend}})

        return data

    def extract_data_from_csv(self, filepath: str) -> list[dict]:
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

    def format_row(self, row: list) -> dict:
        """ Format a row of the csv file, from extract_data_from_csv function
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
        """

        data = self.extract_data_from_csv(filename)

        for user in data:
            self.register(user['userID'], 'admin123456', user)


# The code below is used to register all the people from the survey we conducted:
# This code is not meant to be run


# if __name__ == '__main__':
#     data_handler = DataHandler()
#     data_handler.add_users_from_csv(Constants.DataFile)

