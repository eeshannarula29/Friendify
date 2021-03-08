from __future__ import annotations

import Constants

import os
from typing import Optional, Any
from DataHandler import DataHandler

from CustomExceptions import UserDoesNotExistsError, PrintingQuestionError

from PyInquirer import prompt
import cutie

from RecommendationTree import RecommendationTree


class Screen:
    """This is a super class for other subscales for different screens"""

    def __init__(self, db, previous_screen: Optional[Screen] = None, userID: Optional[str] = None):

        self.database = db
        self.previous_screen = previous_screen

        if userID:
            if DataHandler.is_user(db, Constants.collectionName, userID):
                self.logged_in_as = userID
            else:
                raise UserDoesNotExistsError
        else:
            self.logged_in_as = None

    @staticmethod
    def print_space(lines: int):
        for _ in range(lines):
            print(' ')

    @staticmethod
    def clear_screen() -> bool:
        os.system('clear')
        return True

    def show(self, clear_screen_before_present: bool = True) -> None:

        """Show the current screen

        :param clear_screen_before_present: clear the terminal before presenting
        """

        raise NotImplementedError

    @staticmethod
    def ask_question_PyInquirer(questions: list[dict]) -> Optional[dict]:
        try:
            return prompt(questions)
        except Exception:
            raise PrintingQuestionError

    @staticmethod
    def ask_multi_choice_question_cutie(header_message: str,
                                        questions: list[dict]) -> dict[str, list[str]]:

        answers = {}

        for question in questions:
            Screen.clear_screen()

            print(header_message)
            Screen.print_space(1)
            print(question['message'])
            Screen.print_space(1)

            indices = cutie.select_multiple(question['options'],
                                            maximal_count=Constants.QuestionsLimit,
                                            hide_confirm=True)

            answers[question['header']] = [question['options'][index]
                                           for index in indices]

        return answers


class HomeScreen(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Optional[Screen]:
        Screen.clear_screen() if clear_screen_before_present else False

        Constants.printLogo()

        answer = Screen.ask_question_PyInquirer(Constants.Questions['main_questions']). \
            get('options', 'stay')

        if answer == 'About Us':
            return DocumentationScreen(self.database, Constants.aboutUs, previous_screen=self,
                                       userID=self.logged_in_as)

        elif answer == 'Sign-in/Register':
            return SignInUp(self.database, previous_screen=self, userID=self.logged_in_as)

        elif answer == 'stay':
            return self

        else:
            return None


class DocumentationScreen(Screen):

    def __init__(self, db, document_path_or_string: str, is_path: Optional[bool] = True,
                 previous_screen: Optional[Screen] = None, userID: Optional[str] = None,
                 custom_questions: list[(list[dir], Any)] = None) -> None:

        super().__init__(db, previous_screen=previous_screen, userID=userID)
        self.document_path_or_string = document_path_or_string
        self.is_path = is_path
        self.custom_questions = custom_questions

    def show(self, clear_screen_before_present: bool = True) -> Screen:

        Screen.clear_screen() if clear_screen_before_present else False

        Constants.printLogo()

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
                answer = Screen.ask_question_PyInquirer(question[0])

                result = question[1](answer.get(question[2], 'quit'))

                if isinstance(result, Screen):
                    return result
        else:
            Screen.ask_question_PyInquirer(Constants.Questions['exit_question'])

            return self.previous_screen


class SignInUp(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:

        Screen.clear_screen() if clear_screen_before_present else False

        Constants.printLogo()

        Screen.print_space(1)

        answer = Screen.ask_question_PyInquirer(Constants.Questions['log_questions']). \
            get('options', 'stay')

        if answer == 'Register':
            return Register(self.database, previous_screen=self, userID=self.logged_in_as)
        elif answer == 'Sign in':
            return SignIn(self.database, self, self.logged_in_as)
        elif answer == 'stay':
            return self
        else:
            return self.previous_screen


class Register(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:
        show_logo = Screen.clear_screen() if clear_screen_before_present else False

        Constants.printLogo() if show_logo else False

        self.logged_in_as = Screen.ask_question_PyInquirer(Constants.Questions['UserID_question'])[
            'userID']

        while DataHandler.is_user(self.database, Constants.collectionName, self.logged_in_as):

            print(Constants.Messages['username_taken'])

            question = Constants.generate_question_with_choices(['Try again', 'Exit'],
                                                                "Do you want to:")

            answer = Screen.ask_question_PyInquirer(question).get('options')

            if answer == 'Try again':
                self.show(clear_screen_before_present=False)
            else:
                return self.previous_screen

        answers = Screen.ask_multi_choice_question_cutie(Constants.Messages['header_message'],
                                                         Constants.ProfileQuestions)

        answers['userID'] = self.logged_in_as
        answers['friends'] = []

        DataHandler.register(self.database, Constants.collectionName, self.logged_in_as, answers)

        return SignedIn(self.database, self.previous_screen, self.logged_in_as)


class SignIn(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:
        show_logo = Screen.clear_screen() if clear_screen_before_present else False

        Constants.printLogo() if show_logo else False

        self.logged_in_as = \
            Screen.ask_question_PyInquirer(Constants.Questions['sign_in_questions']).get('userID')

        while not DataHandler.is_user(self.database, Constants.collectionName, self.logged_in_as):

            print(Constants.Messages['username_nonexistent'])

            question = Constants.generate_question_with_choices(['Try again', 'Exit'],
                                                                "Do you want to:")

            answer = Screen.ask_question_PyInquirer(question).get('options')

            if answer == 'Try again':
                self.show(clear_screen_before_present=False)
            else:
                return self.previous_screen

        return SignedIn(self.database, self.previous_screen, self.logged_in_as)


class SignedIn(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:

        Screen.clear_screen() if clear_screen_before_present else False

        Constants.printLogo()
        Screen.print_space(1)
        print(f'Home Screen 🏡 ({self.logged_in_as})')
        Screen.print_space(1)

        answer = Screen.ask_question_PyInquirer(Constants.Questions['after_sign_in_questions']).get(
            'options', 'stay')

        if answer == 'see friend recommendations':

            return Recommendations(self.database, self, self.logged_in_as)

        elif answer == 'change your preferences':

            answers = Screen.ask_multi_choice_question_cutie(Constants.Messages['header_message'],
                                                             Constants.ProfileQuestions)

            DataHandler.update_data_by_ID(self.database, Constants.collectionName,
                                          self.logged_in_as, answers)

            return self

        elif answer == 'your profile':

            data = DataHandler.load_by_userID(self.database, Constants.collectionName,
                                              self.logged_in_as)

            return DocumentationScreen(self.database, Constants.profile(data), is_path=False,
                                       previous_screen=self,
                                       userID=self.logged_in_as)

        elif answer == 'Logout':
            return self.previous_screen

        elif answer == 'stay':
            return self

        elif answer == 'Edit friends':

            friends = DataHandler.load_by_userID(self.database, Constants.collectionName,
                                                 self.logged_in_as).get('friends')

            choices = [{'name': friend} for friend in friends]

            questions = Constants.generate_question_multiple_choice(choices,
                                                                    Constants.Messages[
                                                                        'choose_friends'])

            if friends == []:
                return DocumentationScreen(self.database, Constants.Messages['no_friends'],
                                           is_path=False, previous_screen=self)

            un_friend_list = Screen.ask_question_PyInquirer(questions).get('options', [])

            for friend in un_friend_list:
                DataHandler.un_friend(self.database, Constants.collectionName,
                                      by=self.logged_in_as, to=friend)

            return self

        elif answer == 'Delete account':

            confirmation = Screen.ask_question_PyInquirer(Constants.Questions['are_you_sure']). \
                get('answer')

            if confirmation:

                DataHandler.delete_user(self.database, Constants.collectionName, self.logged_in_as)

                return DocumentationScreen(self.database, Constants.thankyou_message, is_path=False,
                                           previous_screen=self.previous_screen)

            else:
                print('nothing happens')
                return self


class Recommendations(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:

        Screen.clear_screen() if clear_screen_before_present else False

        Constants.printLogo()

        recommendations = RecommendationTree.get_recommendations_for(self.database,
                                                                     self.logged_in_as)

        if recommendations == []:
            return DocumentationScreen(self.database, Constants.Messages['NoRec'], is_path=False,
                                       previous_screen=self.previous_screen)

        if len(recommendations) > 10:
            recommendations = recommendations[:10]

        recommendations.extend(['Exit'])

        question = Constants.generate_question_with_choices(recommendations,
                                                            Constants.Messages['profiles'])

        answer = Screen.ask_question_PyInquirer(question).get('options', 'stay')

        if answer == 'Exit':
            return self.previous_screen

        elif answer == 'stay':
            return self

        else:
            user_data = DataHandler.load_by_userID(self.database, Constants.collectionName, answer)

            questions = [

                (Constants.Questions['add_friend_question'],
                 lambda ans: DataHandler.add_friend(self.database, Constants.collectionName,
                                                    of=self.logged_in_as, to=answer)
                 if ans else None, 'add_friend'),

                (Constants.Questions['exit_question'], lambda _: self, 'quit')
            ]

            return DocumentationScreen(self.database, Constants.profile(user_data), is_path=False,
                                       previous_screen=self, userID=self.logged_in_as,
                                       custom_questions=questions)
