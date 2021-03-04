from __future__ import annotations

import Constants

import os
from typing import Optional
from DataHandler import DataHandler

from CustomExceptions import UserDoesNotExistsError, PrintingQuestionError

from PyInquirer import prompt
import cutie

import tkinter


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

        print(Constants.logo)

        answer = Screen.ask_question_PyInquirer(Constants.Questions['main_questions'])['options']

        if answer == 'About Us':
            return DocumentationScreen(self.database, Constants.aboutUs, previous_screen=self,
                                       userID=self.logged_in_as)

        elif answer == 'Sign-in/Register':
            return SignInUp(self.database, previous_screen=self, userID=self.logged_in_as)

        else:
            return None


class DocumentationScreen(Screen):

    def __init__(self, db, document_path_or_string: str, is_path: Optional[bool] = True,
                 previous_screen: Optional[Screen] = None, userID: Optional[str] = None) -> None:

        super().__init__(db, previous_screen=previous_screen, userID=userID)
        self.document_path_or_string = document_path_or_string
        self.is_path = is_path

    def show(self, clear_screen_before_present: bool = True) -> Screen:

        Screen.clear_screen() if clear_screen_before_present else False

        print(Constants.logo)

        if self.is_path:
            try:
                with open(self.document_path_or_string) as file:
                    print(file.read())
            except FileNotFoundError:
                print(f'path {self.document_path_or_string} does not exists')
        else:
            print(self.document_path_or_string)

        Screen.ask_question_PyInquirer(Constants.Questions['exit_question'])

        return self.previous_screen


class SignInUp(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:

        Screen.clear_screen() if clear_screen_before_present else False

        print(Constants.logo)

        Screen.print_space(1)

        answer = Screen.ask_question_PyInquirer(Constants.Questions['log_questions'])['options']

        if answer == 'Register':
            return Register(self.database, previous_screen=self, userID=self.logged_in_as)
        elif answer == 'Sign in':
            return SignIn(self.database, self, self.logged_in_as)
        else:
            return self.previous_screen


class Register(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:
        show_logo = Screen.clear_screen() if clear_screen_before_present else False

        print(Constants.logo) if show_logo else False

        self.logged_in_as = Screen.ask_question_PyInquirer(Constants.Questions['UserID_question'])[
            'userID']

        while DataHandler.is_user(self.database, Constants.collectionName, self.logged_in_as):
            print(Constants.Messages['username_taken'])
            self.show(clear_screen_before_present=False)

        answers = Screen.ask_multi_choice_question_cutie(Constants.Messages['header_message'],
                                                         Constants.ProfileQuestions)

        answers['userID'] = self.logged_in_as

        DataHandler.register(self.database, Constants.collectionName, self.logged_in_as, answers)

        return SignedIn(self.database, self.previous_screen, self.logged_in_as)


class SignIn(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:
        show_logo = Screen.clear_screen() if clear_screen_before_present else False

        print(Constants.logo) if show_logo else False

        self.logged_in_as = \
            Screen.ask_question_PyInquirer(Constants.Questions['sign_in_questions'])['userID']

        while not DataHandler.is_user(self.database, Constants.collectionName, self.logged_in_as):
            print(Constants.Messages['username_nonexistent'])
            self.show(clear_screen_before_present=False)

        return SignedIn(self.database, self.previous_screen, self.logged_in_as)


class SignedIn(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:

        Screen.clear_screen() if clear_screen_before_present else False

        print(Constants.logo)
        Screen.print_space(1)
        print(f'Home Screen 🏡 ({self.logged_in_as})')
        Screen.print_space(1)

        answer = Screen.ask_question_PyInquirer(Constants.Questions['after_sign_in_questions'])[
            'options']

        if answer == 'see friend recommendations':
            # TODO: implement this condition
            return self

        elif answer == 'change your preferences':
            # TODO: implement this condition
            return self

        elif answer == 'your profile':

            data = DataHandler.load_by_userID(self.database, Constants.collectionName,
                                              self.logged_in_as)

            return DocumentationScreen(self.database, Constants.profile(data), is_path=False,
                                       previous_screen=self,
                                       userID=self.logged_in_as)

        else:
            return self.previous_screen
