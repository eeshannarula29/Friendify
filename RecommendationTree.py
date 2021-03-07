from __future__ import annotations
from typing import Optional

import Constants
from DataHandler import DataHandler

from random import choice, random

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
        We are assuming that user = [<movie>, <music>, <game>, <food>, <userID>]
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
    def create_users_from_user(user: dict, with_id:bool = True) -> list[list]:

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
    def generate_users(data: list[dict]) -> list[list]:

        users = []

        for user in data:
            users.extend(RecommendationTree.create_users_from_user(user))

        return users

    @staticmethod
    def generate_tree(database) -> RecommendationTree:
        data = DataHandler.load_all(database, Constants.collectionName)

        users = RecommendationTree.generate_users(data)

        tree = RecommendationTree()

        for user in users:
            tree.insert_user(user)

        return tree

    def search_tree(self, sequence: list[str]) -> list[RecommendationTree]:

        if all(subtree.is_user for subtree in self._subtrees):
            return self._subtrees
        else:
            users = []

            for subtree in self._subtrees:
                if sequence[0] == subtree.value:
                    users.extend(subtree.search_tree(sequence[1:]))

            return users

    @staticmethod
    def get_recommendations_for(db, userID: str):

        tree = RecommendationTree.generate_tree(db)

        user = DataHandler.load_by_userID(db, Constants.collectionName, userID)

        inputs = RecommendationTree.create_users_from_user(user)

        output = []

        for inp in inputs:
            out = tree.search_tree(inp)
            output.extend(out)

        result = [val.value for val in output]

        keys = set(result)
        d = []

        for key in keys:
            d.append((result.count(key), key))

        d.sort()
        d.pop()

        return [v[1] for v in d if v[0] >= 4]
