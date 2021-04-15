"""The file contains the screen object, which handles the UI"""

from __future__ import annotations

import os
import sys
from typing import Optional, Any
from difflib import SequenceMatcher

from PyInquirer import prompt
import cutie

import constants
from custom_exceptions import UserDoesNotExistsError, PrintingQuestionError
from authenticate import DataHandler
from recommendation_graph import Graph


class Screen:
    """This is a super class for other subscales for different screens"""
    handler: DataHandler
    previous_screen: Screen
    logged_in_as: Optional[str]

    def __init__(self, data_handler: DataHandler, previous_screen: Optional[Screen] = None,
                 userID: Optional[str] = None) -> None:

        self.handler = data_handler
        self.previous_screen = previous_screen

        if userID:
            if self.handler.is_user(userID):
                self.logged_in_as = userID
            else:
                raise UserDoesNotExistsError
        else:
            self.logged_in_as = None

    @staticmethod
    def print_space(lines: int) -> None:
        """Print empty line"""
        for _ in range(lines):
            print(' ')

    @staticmethod
    def clear_screen() -> bool:
        """clear the terminal screen"""
        if sys.platform == 'darwin' or sys.platform == 'linux':
            os.system('clear')
            return True
        else:
            os.system('cls')
            return True

    def show(self, clear_screen_before_present: bool = True) -> None:

        """Show the current screen
        :param clear_screen_before_present: clear the terminal before presenting
        """

        raise NotImplementedError

    @staticmethod
    def ask_question_py_inquirer(questions: list[dict]) -> Optional[dict]:
        """Use py-inquirer to ask questions in the terminal"""
        try:
            return prompt(questions)
        except Exception:
            raise PrintingQuestionError

    @staticmethod
    def ask_multi_choice_question_cutie(header_message: str,
                                        questions: list[dict]) -> dict[str, list[str]]:
        """Use cutie to ask questions in the terminal"""
        answers = {}

        for question in questions:
            Screen.clear_screen()

            print(header_message)
            Screen.print_space(1)
            print(question['message'])
            Screen.print_space(1)

            indices = cutie.select_multiple(question['options'],
                                            maximal_count=constants.QUESTIONSLIMIT,
                                            minimal_count=1,
                                            hide_confirm=True)

            answers[question['header']] = [question['options'][index]
                                           for index in indices]

        return answers


class HomeScreen(Screen):
    """Represents the home screen"""

    def show(self, clear_screen_before_present: bool = True) -> Optional[Screen]:

        if clear_screen_before_present:
            Screen.clear_screen()

        constants.print_logo()

        answer = Screen.ask_question_py_inquirer(constants.QUESTIONS['main_questions']). \
            get('options', 'stay')

        if answer == 'About Us':
            doc = DocumentationScreen(self.handler, self, self.logged_in_as)

            doc.add_details(constants.ABOUTUS)

            return doc

        elif answer == 'Sign-in/Register':
            return SignInUp(self.handler, previous_screen=self, userID=self.logged_in_as)

        elif answer == 'stay':
            return self

        else:
            return None


class DocumentationScreen(Screen):
    """Represents a Documentation Screen, used to read documents and text"""
    document_path_or_string: str
    is_path: bool
    custom_questions: Optional[list[(list[dir], Any)]]

    def add_details(self, document_path_or_string: str, is_path: Optional[bool] = True,
                    custom_questions: Optional[list[tuple[list[dir], Any]]] = None) -> None:
        """Add details of the document, kind of like content of the document"""
        self.document_path_or_string = document_path_or_string
        self.is_path = is_path
        self.custom_questions = custom_questions

    def show(self, clear_screen_before_present: bool = True) -> Optional[Screen]:

        if clear_screen_before_present:
            Screen.clear_screen()

        constants.print_logo()

        if self.is_path:
            try:
                with open(self.document_path_or_string) as file:
                    print(file.read())
            except FileNotFoundError:
                print(f'path {self.document_path_or_string} does not exists')
        else:
            print(self.document_path_or_string)

        if self.custom_questions:
            for question in self.custom_questions:
                answer = Screen.ask_question_py_inquirer(question[0])

                result = question[1](answer.get(question[2], 'quit'))

                if isinstance(result, Screen):
                    return result
        else:
            Screen.ask_question_py_inquirer(constants.QUESTIONS['exit_question'])

            return self.previous_screen

        return None


class SignInUp(Screen):
    """Represents a sign in / up choosing screen"""

    def show(self, clear_screen_before_present: bool = True) -> Optional[Screen]:

        if clear_screen_before_present:
            Screen.clear_screen()

        constants.print_logo()

        Screen.print_space(1)

        answer = Screen.ask_question_py_inquirer(constants.QUESTIONS['log_questions']). \
            get('options', 'stay')

        if answer == 'Register':
            return Register(self.handler, previous_screen=self, userID=self.logged_in_as)
        elif answer == 'Sign in':
            return SignIn(self.handler, self, self.logged_in_as)
        elif answer == 'stay':
            return self
        else:
            return self.previous_screen


class Register(Screen):
    """Represents a registration screen"""

    def show(self, clear_screen_before_present: bool = True) -> Screen:
        show_logo = Screen.clear_screen() if clear_screen_before_present else False

        if show_logo:
            constants.print_logo()

        self.logged_in_as = Screen.ask_question_py_inquirer(
            constants.QUESTIONS['UserID_question']).get('user_id', '')

        if self.handler.is_user(self.logged_in_as):
            print(constants.MESSAGES['username_taken'])

            question = constants.generate_question_with_choices(['Exit'], "")

            Screen.ask_question_py_inquirer(question)

            return self.previous_screen

        answers = Screen.ask_multi_choice_question_cutie(constants.MESSAGES['header_message'],
                                                         constants.PROFILEQUESTIONS)

        self.handler.register(self.logged_in_as, answers)

        return SignedIn(self.handler, self.previous_screen, self.logged_in_as)


class SignIn(Screen):
    """Represents a sign in screen"""

    def show(self, clear_screen_before_present: bool = True) -> Screen:
        show_logo = Screen.clear_screen() if clear_screen_before_present else False

        if show_logo:
            constants.print_logo()

        credentials = Screen.ask_question_py_inquirer(constants.QUESTIONS['sign_in_questions'])

        self.logged_in_as = credentials.get('user_id')

        if not self.handler.sign_in(self.logged_in_as):
            print(constants.MESSAGES['username_nonexistent'])

            question = constants.generate_question_with_choices(['Exit'], "")

            Screen.ask_question_py_inquirer(question)

            return self.previous_screen

        return SignedIn(self.handler, self.previous_screen, self.logged_in_as)


class SignedIn(Screen):
    """Represents a signed in home screen"""

    def show_start(self, clear_screen: bool) -> None:
        """Print the logo and starting of app"""
        if clear_screen:
            Screen.clear_screen()

        constants.print_logo()
        Screen.print_space(1)
        print(f'Home Screen 🏡 ({self.logged_in_as})')
        Screen.print_space(1)

    def show(self, clear_screen_before_present: bool = True) -> Optional[Screen]:

        self.show_start(clear_screen_before_present)

        answer = Screen.ask_question_py_inquirer(
            constants.QUESTIONS['after_sign_in_questions']).get('options', 'stay')

        if answer == 'see friend recommendations':

            return Recommendations(self.handler, self, self.logged_in_as)

        elif answer == 'change your preferences':

            answers = Screen.ask_multi_choice_question_cutie(constants.MESSAGES['header_message'],
                                                             constants.PROFILEQUESTIONS)

            self.handler.update_user_data(self.logged_in_as, answers)

            return self

        elif answer == 'your profile':

            data = self.handler.get_user_data(self.logged_in_as)

            doc = DocumentationScreen(self.handler, self, self.logged_in_as)

            doc.add_details(constants.profile(data), is_path=False)

            return doc

        elif answer == 'Logout':
            return self.previous_screen

        elif answer == 'stay':
            return self

        elif answer == 'My friends':
            return MyFriends(self.handler, previous_screen=self, userID=self.logged_in_as)

        elif answer == 'Delete account':

            confirmation = Screen.ask_question_py_inquirer(constants.QUESTIONS['are_you_sure']). \
                get('answer')

            if confirmation:

                self.handler.delete_user(self.logged_in_as)

                doc = DocumentationScreen(self.handler, self.previous_screen)

                doc.add_details(constants.THANKYOU, is_path=False)

                return doc

            else:
                print('nothing happens')
                return self

        elif answer == 'View your network':

            Screen.clear_screen()

            constants.print_logo()
            Screen.print_space(1)
            print(constants.MESSAGES['stop_graph'])
            Screen.print_space(1)

            answer = Screen.ask_question_py_inquirer(constants.QUESTIONS['depth_question']). \
                get('options')

            did_change = constants.change_depth(answer)

            if did_change > 0:

                constants.DEPTH = did_change

                graph = Graph.load_friends_graph(self.handler). \
                    generate_users_graph_for_user(self.logged_in_as, constants.DEPTH)

                graph.plot()

                Screen.ask_question_py_inquirer(constants.QUESTIONS['exit_question'])

                return self

            return self

        elif answer == 'Search for people':
            return SearchPeople(self.handler, self, self.logged_in_as)

        return None


class Recommendations(Screen):
    """Represents a friends Recommendation screen"""

    def show(self, clear_screen_before_present: bool = True) -> Screen:

        if clear_screen_before_present:
            Screen.clear_screen()

        constants.print_logo()

        graph = Graph.load_friends_graph(self.handler)

        recommendations = graph.recommend_friends(self.logged_in_as, 10)

        if recommendations == []:
            doc = DocumentationScreen(self.handler, self.previous_screen, self.logged_in_as)

            doc.add_details(constants.MESSAGES['NoRec'], is_path=False)

            return doc

        recommendations.extend(['Exit'])

        question = constants.generate_question_with_choices(recommendations,
                                                            constants.MESSAGES['profiles'])

        answer = Screen.ask_question_py_inquirer(question).get('options', 'stay')

        if answer == 'Exit':
            return self.previous_screen

        elif answer == 'stay':
            return self

        else:

            user = answer.split(' ')[0]

            user_data = self.handler.get_user_data(user)

            questions = [

                (constants.QUESTIONS['add_friend_question'],
                 lambda ans: self.handler.add_friend(of=self.logged_in_as, to=user)
                 if ans else None, 'add_friend'),

                (constants.QUESTIONS['exit_question'], lambda _: self, 'quit')
            ]

            doc = DocumentationScreen(self.handler, self, self.logged_in_as)

            doc.add_details(constants.profile(user_data), is_path=False, custom_questions=questions)

            return doc


class MyFriends(Screen):
    """Represents a list of user friends screen"""

    def show(self, clear_screen_before_present: bool = True) -> Screen:

        if clear_screen_before_present:
            Screen.clear_screen()

        constants.print_logo()

        friends = list(self.handler.get_user_data(self.logged_in_as).get('friends'))

        if friends == []:

            doc = DocumentationScreen(self.handler, self.previous_screen, self.logged_in_as)

            doc.add_details(constants.MESSAGES['no_friends'], is_path=False)

            return doc

        else:

            friends.append('Exit')

            question = constants.generate_question_with_choices(friends,
                                                                constants.MESSAGES['my_friends'])

            answer = Screen.ask_question_py_inquirer(question).get('options')

            if answer == 'Exit':
                return self.previous_screen

            else:

                options = ['Unfriend', 'Exit']

                question = constants.generate_question_with_choices(options,
                                                                    'What would you like to do?')

                Screen.clear_screen()

                constants.print_logo()

                print(constants.profile(self.handler.get_user_data(answer)))

                sub_answer = Screen.ask_question_py_inquirer(question).get('options')

                if sub_answer == 'Unfriend':
                    self.handler.un_friend(self.logged_in_as, answer)
                    return self

                else:
                    return self


class SearchPeople(Screen):
    """Represents a searching screen"""

    def show(self, clear_screen_before_present: bool = True) -> Optional[Screen]:

        if clear_screen_before_present:
            Screen.clear_screen()

        constants.print_logo()

        query = Screen.ask_question_py_inquirer(constants.QUESTIONS['search']).get('query')

        users = []

        for user_data in self.handler.get_all_data():
            users.append(user_data['userID'])

        search = self.search(users, query, 10)

        search.extend(['Search again', 'Exit'])

        question = constants.generate_question_with_choices(search, ' ')

        answer = Screen.ask_question_py_inquirer(question).get('options', 'stay')

        if answer == 'Search again':
            return self
        elif answer == 'Exit':
            return self.previous_screen
        elif answer == 'stay':
            return self
        else:
            options = ['Exit']
            user_data = self.handler.get_user_data(answer)

            if answer in self.handler.get_user_data(self.logged_in_as).get('friends'):
                options.insert(0, f'Unfriend {answer}')
            else:
                if answer != self.logged_in_as:
                    options.insert(0, f'Friend {answer}')

            Screen.clear_screen()
            constants.print_logo()

            print(constants.profile(user_data))

            sub_answer = Screen.ask_question_py_inquirer(
                constants.generate_question_with_choices(options, ' ')).get('options', ' ')

            if sub_answer == 'Exit':
                return self.previous_screen
            elif sub_answer == f'Unfriend {answer}':
                self.handler.un_friend(self.logged_in_as, answer)
                return self.previous_screen
            elif sub_answer == f'Friend {answer}':
                self.handler.add_friend(self.logged_in_as, answer)
                return self.previous_screen

        return None

    def search(self, users: list[str], query: str, limit: int) -> list[str]:
        """ Use merge sort to sort users according to our query

        :param users: the list of users to search form
        :param query: the query to search for
        :param limit: the maximum number of results to return
        :return: The list of results matching our query
        """
        lst = self._mergesort_string(users, query)
        lst.reverse()

        return lst[:limit]

    def _mergesort_string(self, lst: list, query: str) -> list:

        if len(lst) < 2:
            return lst.copy()
        else:

            mid = len(lst) // 2
            left_sorted = self._mergesort_string(lst[:mid], query)
            right_sorted = self._mergesort_string(lst[mid:], query)

            return SearchPeople._merge(left_sorted, right_sorted, query)

    @staticmethod
    def _merge(lst1: list, lst2: list, query: str) -> list:
        """Return a sorted list with the elements in lst1 and lst2.

        Preconditions:
            - is_sorted(lst1)
            - is_sorted(lst2)
        """
        i1, i2 = 0, 0
        sorted_so_far = []

        while i1 < len(lst1) and i2 < len(lst2):

            if SearchPeople.similar(lst1[i1], query) <= SearchPeople.similar(lst2[i2], query):
                sorted_so_far.append(lst1[i1])
                i1 += 1
            else:
                sorted_so_far.append(lst2[i2])
                i2 += 1

        if i1 == len(lst1):
            return sorted_so_far + lst2[i2:]
        else:
            return sorted_so_far + lst1[i1:]

    @staticmethod
    def similar(a: str, b: str) -> float:
        """ Return similarity score between two strings
        """
        return SequenceMatcher(None, a, b).ratio()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['os',
                          'constants',
                          'sys',
                          'typing',
                          'custom_exceptions',
                          'PyInquirer',
                          'cutie',
                          'authenticate',
                          'recommendation_graph',
                          'difflib'],
        'allowed-io': ['ask_question_py_inquirer',
                       'ask_multi_choice_question_cutie',
                       'show',
                       'print_space',
                       'show_start'],
        'max-line-length': 100,
        'disable': ['E1136']
    })
