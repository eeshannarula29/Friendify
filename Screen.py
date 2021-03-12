from __future__ import annotations

import Constants

import os
import sys
import logging
from typing import Optional, Any

from CustomExceptions import UserDoesNotExistsError, PrintingQuestionError

from PyInquirer import prompt
import cutie

import dash
import dash_html_components as html
import dash_cytoscape as cyto
import dash_core_components as dcc
from dash.dependencies import Input, Output

import webbrowser

from RecommendationTree import RecommendationTree

from authenticate import DataHandler


class Screen:
    """This is a super class for other subscales for different screens"""

    def __init__(self, data_handler: DataHandler, previous_screen: Optional[Screen] = None,
                 userID: Optional[str] = None):

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
    def print_space(lines: int):
        for _ in range(lines):
            print(' ')

    @staticmethod
    def clear_screen() -> bool:
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
                                            minimal_count=1,
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
            return DocumentationScreen(self.handler, Constants.aboutUs, previous_screen=self,
                                       userID=self.logged_in_as)

        elif answer == 'Sign-in/Register':
            return SignInUp(self.handler, previous_screen=self, userID=self.logged_in_as)

        elif answer == 'stay':
            return self

        else:
            return None


class DocumentationScreen(Screen):

    def __init__(self, data_handler, document_path_or_string: str, is_path: Optional[bool] = True,
                 previous_screen: Optional[Screen] = None, userID: Optional[str] = None,
                 custom_questions: list[(list[dir], Any)] = None) -> None:

        super().__init__(data_handler, previous_screen=previous_screen, userID=userID)
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
            return Register(self.handler, previous_screen=self, userID=self.logged_in_as)
        elif answer == 'Sign in':
            return SignIn(self.handler, self, self.logged_in_as)
        elif answer == 'stay':
            return self
        else:
            return self.previous_screen


class Register(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:
        show_logo = Screen.clear_screen() if clear_screen_before_present else False

        Constants.printLogo() if show_logo else False

        self.logged_in_as = Screen.ask_question_PyInquirer(Constants.Questions['UserID_question']).\
            get('userID', '')

        while self.handler.is_user(self.logged_in_as):

            print(Constants.Messages['username_taken'])

            question = Constants.generate_question_with_choices(['Exit'], "")

            Screen.ask_question_PyInquirer(question)

            return self.previous_screen

        password = Screen.ask_question_PyInquirer(Constants.Questions['password_question']).\
            get('password', '')

        while len(password) < 6:

            print(Constants.Messages['short_password'])

            question = Constants.generate_question_with_choices(['Try again', 'Exit'], "")

            answer = Screen.ask_question_PyInquirer(question).get('options', 'stay')

            if answer == 'Try again':
                password = Screen.ask_question_PyInquirer(Constants.Questions['password_question'])\
                    .get('password', '')
            else:
                return self.previous_screen

        answers = Screen.ask_multi_choice_question_cutie(Constants.Messages['header_message'],
                                                         Constants.ProfileQuestions)

        self.handler.register(self.logged_in_as, password, answers)

        return SignedIn(self.handler, self.previous_screen, self.logged_in_as)


class SignIn(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:
        show_logo = Screen.clear_screen() if clear_screen_before_present else False

        Constants.printLogo() if show_logo else False

        credentials = Screen.ask_question_PyInquirer(Constants.Questions['sign_in_questions'])

        self.logged_in_as = credentials.get('userID')
        password = credentials.get('password')

        while not self.handler.sign_in(self.logged_in_as, password):

            print(Constants.Messages['username_nonexistent'])

            question = Constants.generate_question_with_choices(['Exit'], "")

            Screen.ask_question_PyInquirer(question)

            return self.previous_screen

        return SignedIn(self.handler, self.previous_screen, self.logged_in_as)


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

            return Recommendations(self.handler, self, self.logged_in_as)

        elif answer == 'change your preferences':

            answers = Screen.ask_multi_choice_question_cutie(Constants.Messages['header_message'],
                                                             Constants.ProfileQuestions)

            self.handler.update_user_data(self.logged_in_as, answers)

            return self

        elif answer == 'your profile':

            data = self.handler.get_user_data(self.logged_in_as)

            return DocumentationScreen(self.handler, Constants.profile(data), is_path=False,
                                       previous_screen=self,
                                       userID=self.logged_in_as)

        elif answer == 'Logout':
            return self.previous_screen

        elif answer == 'stay':
            return self

        elif answer == 'Edit friends':

            friends = self.handler.get_user_data(self.logged_in_as).get('friends')

            choices = [{'name': friend} for friend in friends]

            questions = Constants.generate_question_multiple_choice(choices,
                                                                    Constants.Messages[
                                                                        'choose_friends'])

            if friends == []:
                return DocumentationScreen(self.handler, Constants.Messages['no_friends'],
                                           is_path=False, previous_screen=self)

            un_friend_list = Screen.ask_question_PyInquirer(questions).get('options', [])

            for friend in un_friend_list:
                self.handler.un_friend(by=self.logged_in_as, to=friend)

            return self

        elif answer == 'Delete account':

            confirmation = Screen.ask_question_PyInquirer(Constants.Questions['are_you_sure']). \
                get('answer')

            if confirmation:

                self.handler.delete_user(self.logged_in_as)

                return DocumentationScreen(self.handler, Constants.thankyou_message, is_path=False,
                                           previous_screen=self.previous_screen)

            else:
                print('nothing happens')
                return self

        elif answer == 'View your network':

            Screen.clear_screen()

            Constants.printLogo()
            Screen.print_space(1)
            print(Constants.Messages['stop_graph'])
            Screen.print_space(1)

            answer = Screen.ask_question_PyInquirer(Constants.Questions['depth_question']).\
                get('options')

            did_change = Constants.change_depth(answer)

            if did_change > 0:

                Constants.Depth = did_change

                graph_data = self.handler.generate_graph_for_user(self.logged_in_as,
                                                                  Constants.Depth)
                app = dash.Dash(__name__)

                log = logging.getLogger('werkzeug')
                log.disabled = True

                @app.callback(Output('cytoscape', 'layout'),
                              Input('dropdown', 'value'))
                def update_layout(layout) -> dict:
                    return {
                        'name': layout,
                        'animate': True
                    }

                app.layout = html.Div([
                    html.P("Friendify Network"),
                    dcc.Dropdown(
                        id='dropdown',
                        value='breadthfirst',
                        clearable=False,
                        options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['breadthfirst', 'grid', 'random', 'circle', 'cose',
                                         'concentric']
                        ]
                    ),
                    cyto.Cytoscape(
                        id='cytoscape',
                        elements=graph_data,
                        layout={'name': 'breadthfirst'},
                        style={'width': '1500px', 'height': '800px'}
                    ),
                ])

                webbrowser.open_new('http://127.0.0.1:5000/')
                app.run_server(port=5000)

                Screen.ask_question_PyInquirer(Constants.Questions['exit_question'])

                return self

            else:
                return self


class Recommendations(Screen):

    def show(self, clear_screen_before_present: bool = True) -> Screen:

        Screen.clear_screen() if clear_screen_before_present else False

        Constants.printLogo()

        recommendations = RecommendationTree.get_recommendations_for(self.handler,
                                                                     self.logged_in_as)

        if recommendations == []:
            return DocumentationScreen(self.handler, Constants.Messages['NoRec'], is_path=False,
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
            user_data = self.handler.get_user_data(answer)

            questions = [

                (Constants.Questions['add_friend_question'],
                 lambda ans: self.handler.add_friend(of=self.logged_in_as, to=answer)
                 if ans else None, 'add_friend'),

                (Constants.Questions['exit_question'], lambda _: self, 'quit')
            ]

            return DocumentationScreen(self.handler, Constants.profile(user_data), is_path=False,
                                       previous_screen=self, userID=self.logged_in_as,
                                       custom_questions=questions)
