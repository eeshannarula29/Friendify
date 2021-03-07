from typing import Optional

from CustomExceptions import DataDidNotLoadError, RegistrationError, UserDoesNotExistsError, \
    UserExitsError, DataDidNotUploadError

from firebase_admin import exceptions


class DataHandler:

    @staticmethod
    def load_all(database, from_collection: str) -> Optional[list[dict]]:
        """Load all the data in the collection

        :param database: the firebase database client object
        :param from_collection: collection from which we want to extract the data
        :return: data contained in the collection
        """
        data = []

        try:
            entries = database.collection(from_collection).get()

            for entry in entries:
                if entry.exists:
                    data.append(entry.to_dict())

        except exceptions.FirebaseError:
            raise DataDidNotLoadError

        return data

    @staticmethod
    def load_by_userID(database, from_collection: str, userID: str) -> Optional[dict]:
        """Load data for a user

        :param database: the firebase database client object
        :param userID: The user ID of the person
        :param from_collection: collection from which we want to extract the data
        :return: dictionary containing the users data
        """
        try:
            user = database.collection(from_collection).document(userID).get()

            if user.exists:
                return user.to_dict()
            else:
                raise UserDoesNotExistsError

        except exceptions.FirebaseError:
            raise DataDidNotLoadError

    @staticmethod
    def is_user(database, from_collection: str, userID: str) -> bool:
        """
        :param database: the firebase database client object
        :param userID: The user ID of the person
        :param from_collection: collection from which we want to extract the data
        :return: Return whether the user in in the database
        """
        try:
            DataHandler.load_by_userID(database, from_collection=from_collection, userID=userID)
            return True
        except (ValueError, DataDidNotLoadError, UserDoesNotExistsError):
            return False

    @staticmethod
    def register(database, from_collection: str, userID: str,
                 userData: Optional[dict] = None) -> None:
        """ register a user to our app

        :param database: the firebase database client object
        :param from_collection: collection from which we want to extract the data
        :param userID: The user ID of the person
        :param userData: the data of the user
        """
        try:
            user = DataHandler.load_by_userID(database, from_collection, userID)
        except (ValueError, DataDidNotLoadError, UserDoesNotExistsError):
            user = None

        if not user:  # if userid in use not used before
            if not userData:
                userData = {'userID': userID, 'friends': []}
            try:
                database.collection(from_collection).document(userID).set(userData)
            except (ValueError, TypeError, exceptions.FirebaseError):
                raise RegistrationError
        else:
            raise UserExitsError

    @staticmethod
    def update_data_by_ID(database, from_collection: str, userID: str, userData: dict) -> None:
        """ Update the data of a user

        :param database: the firebase database client object
        :param from_collection: collection from which we want to extract the data
        :param userID: The user ID of the person
        :param userData: the data of the user
        """
        if DataHandler.is_user(database, from_collection, userID):
            try:
                database.collection(from_collection).document(userID).set(userData, merge=True)
            except (ValueError, TypeError, exceptions.FirebaseError):
                raise DataDidNotUploadError

    @staticmethod
    def add_friend(database, collection: str, of: str, to: str) -> None:
        """ Add friend to a user

        :param database: the firebase database
        :param collection: collection in database containing data
        :param of: the user who is adding friend
        :param to: the user who is added friend
        """
        of_data = DataHandler.load_by_userID(database, collection, of)
        to_data = DataHandler.load_by_userID(database, collection, to)

        if not (to in of_data['friends'] or of in to_data['friends']):
            of_data['friends'].append(to)
            to_data['friends'].append(of)

            DataHandler.update_data_by_ID(database, collection, of, of_data)
            DataHandler.update_data_by_ID(database, collection, to, to_data)

    @staticmethod
    def un_friend(database, collection, by: str, to: str) -> None:
        """remove friend

        :param database: the firebase database
        :param collection: collection in database containing data
        :param by: Id of the user who is un friending
        :param to: Id of the user who is getting un friended
        """
        by_data = DataHandler.load_by_userID(database, collection, by)
        to_data = DataHandler.load_by_userID(database, collection, to)

        if to in by_data['friends'] and by in to_data['friends']:
            by_data['friends'].remove(to)
            to_data['friends'].remove(by)

        DataHandler.update_data_by_ID(database, collection, by, by_data)
        DataHandler.update_data_by_ID(database, collection, to, to_data)

    @staticmethod
    def delete_user(database, from_collection: str, userID: str) -> None:
        """ Delete the user account

        :param database: the firebase database
        :param from_collection: collection in database containing data
        :param userID: Id of the user who is deleting the account
        """
        user_data = DataHandler.load_by_userID(database, from_collection, userID)

        for friend in user_data['friends']:
            DataHandler.un_friend(database, from_collection, by=userID, to=friend)

        database.collection(from_collection).document(userID).delete()
