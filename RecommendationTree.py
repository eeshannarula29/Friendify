from __future__ import annotations
from typing import Optional

import Constants
from authenticate import DataHandler

from random import choice

ROOT = '*'


class RecommendationTree:
    is_user: bool
    type: str
    _subtrees: list[RecommendationTree]

    def __init__(self, value: str = ROOT, is_user: bool = False) -> None:
        self.is_user = is_user
        self.value = value
        self._subtrees = []

    def get_subtrees(self) -> list[RecommendationTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def find_subtree_by_value(self, value: str) -> Optional[RecommendationTree]:
        """Return the subtree corresponding to the given value.

        Return None if no subtree corresponds to that value.
        """
        for subtree in self._subtrees:
            if subtree.value == value:
                return subtree

        return None

    def add_subtree(self, subtree: RecommendationTree) -> None:
        """Add a subtree to this Recommendation tree."""
        self._subtrees.append(subtree)

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        move_desc = f'{self.value}\n'
        s = '  ' * depth + move_desc
        if self._subtrees == []:
            return s
        else:
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def insert_user(self, user: list[str]) -> None:
        """
        Insert a user to the tree, that is one possible combination of the
        movies, music, games and food that the user likes. Each chooses
        at most 3 sub categories from these 4 categories. So we would
        be calling this function at most 3^4 times for a single user
        in our database.

        :param user: it is a possible combination of user preferences

        Preconditions:
        - user = [<movie>, <music>, <game>, <food>, <userID>]
        """

        self.insert_user_helper(user, 0)

    def insert_user_helper(self, user: list[str], current_index: int) -> None:

        if current_index < len(user):

            new_subtree = RecommendationTree(value=user[current_index])

            if current_index == len(user) - 1:
                new_subtree.is_user = True

            subtree = self.find_subtree_by_value(user[current_index])

            if subtree:
                subtree.insert_user_helper(user, current_index + 1)
            else:
                self.add_subtree(new_subtree)
                new_subtree.insert_user_helper(user, current_index + 1)

    @staticmethod
    def create_combinations_from_user(user: dict, with_id: bool = True) -> list[list]:
        """ Create all the possible combinations of user preferences for a single user

        :param user: The data of a user form our database
        :param with_id: weather to include the user id at the end of the list
        :return: a list of possible combinations of user preferences
        """
        users = []

        for movie in user['movies']:
            for music in user['music']:
                for game in user['games']:
                    for food in user['food']:
                        if with_id:
                            users.append([movie, music, game, food, user['userID']])
                        else:
                            users.append([movie, music, game, food])
        return users

    @staticmethod
    def create_combinations_from_multiple_users(data: list[dict]) -> list[list]:
        """ Returns all the possible combinations of user preferences for multiple users

        :param data: list of data of multiple users from our database
        :return: a list of possible combinations of user preferences for all the users in data
        """
        users = []

        for user in data:
            users.extend(RecommendationTree.create_combinations_from_user(user))

        return users

    @staticmethod
    def generate_tree(handler: DataHandler) -> RecommendationTree:
        """ Generate a tree by inserting all possible preferences of all the users
        in our database, with the root of a single combination being the userID.

        :return: RecommendationTree
        """
        data = handler.get_all_data()

        users = RecommendationTree.create_combinations_from_multiple_users(data)

        tree = RecommendationTree()

        for user in users:
            tree.insert_user(user)

        return tree

    def search_tree(self, sequence: list[str]) -> list[RecommendationTree]:
        """ Search for the users with the specific sequence of preferences

        :param sequence: specific sequence of preferences
        :return: a list of users who are root to this sequence
        """
        if all(subtree.is_user for subtree in self._subtrees):
            return self._subtrees
        else:
            users = []

            found_any = False

            for subtree in self._subtrees:
                if sequence[0] == subtree.value:
                    users.extend(subtree.search_tree(sequence[1:]))
                    found_any = True

            if not found_any:
                random_subtree = choice(self._subtrees)
                users.extend(random_subtree.search_tree(sequence[1:]))

            return users

    @staticmethod
    def get_recommendations_for(handler: DataHandler, userID: str) -> list[str]:
        """ Return the top recommendations for a user with userID <userID>

        :param handler: Data handler
        :param userID: user ID for the user we want the recommendations
        :return: list of user id's
        """
        tree = RecommendationTree.generate_tree(handler)

        user = handler.get_user_data(userID)

        combinations = RecommendationTree.create_combinations_from_user(user)

        users = []

        for combination in combinations:
            users.extend(tree.search_tree(combination))

        user_IDs = [user_id.value for user_id in users]

        unique_ids = set(user_IDs)

        ids_and_count = []

        for unique_id in unique_ids:
            ids_and_count.append((user_IDs.count(unique_id), unique_id))

        ids_and_count.sort()
        ids_and_count.pop()
        ids_and_count.reverse()

        return [id_and_count[1] for id_and_count in ids_and_count
                if id_and_count[0] >= Constants.MinimumSimilarityScore]

    @staticmethod
    def make_friends(handler: DataHandler) -> None:

        users = handler.get_all_data()

        for user in users:
            recommendations = RecommendationTree.get_recommendations_for(handler, user['userID'])

            if len(recommendations) > 3:
                recommendations = recommendations[:3]

            for friend in recommendations:
                handler.add_friend(user['userID'], friend)


# This code is meant to add friends for the dummy users from the survey
# This code is not meant to run.

# if __name__ == '__main__':
#     import firebase_admin
#     from firebase_admin import credentials
#     from firebase_admin import firestore
#
#     cred = credentials.Certificate(Constants.keysFile)
#     firebase_admin.initialize_app(cred)
#
#     db = firestore.client()
#
#     RecommendationTree.make_friends(db)
