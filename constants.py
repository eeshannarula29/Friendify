"""Contains all the constants"""

import sys
import pyfiglet

COLLECTION = "data"
KEYS = "keys.json"
ABOUTUS = "AboutUs.txt"

QUESTIONSLIMIT = 3

DEPTH = 2

DATA = 'data/Survey.csv'

THANKYOU = "Thank you for using Friendify 🙏 😀"

CATEGORIES = {

    'movies': [
        'action',
        'adventure',
        'animation',
        'comedy',
        'crime',
        'documentary',
        'drama',
        'fantasy',
        'horror',
        'mystery',
        'romance',
        'sci-fi',
        'thriller'
    ],

    'music': [
        'anime',
        'classical',
        'country',
        'edm',
        'folk',
        'hip hop',
        'indie',
        'jazz',
        'k-pop',
        'pop',
        'rnb',
        'rock'
    ],

    'games': [
        'apex legends',
        'call of duty',
        'cs:go',
        'dota 2',
        'fortnite',
        'genshin impact',
        'gta v',
        'league of legends',
        'minecraft',
        'nba 2k',
        'rocket league',
        'valorant'
    ],

    'food': [
        'american',
        'asian fusion',
        'breakfast & brunch',
        'cafes',
        'chinese',
        'french',
        'italian',
        'japanese',
        'mediterranean',
        'mexican',
        'soul food'
    ]

}

QUESTIONS = {

    'log_questions': [
        {
            'type': 'list',
            'name': 'options',
            'message': 'Do you want to register or login',
            'choices': ['Register', 'Sign in', 'exit']
        }
    ],

    'UserID_question': [
        {
            'type': 'input',
            'name': 'user_id',
            'message': 'type a username',
        }
    ],

    'sign_in_questions': [
        {
            'type': 'input',
            'name': 'user_id',
            'message': 'type your username',
        }
    ],

    'password_question': [
        {
            'type': 'password',
            'name': 'password',
            'message': 'Type your password (at least 6 characters long)'
        }
    ],

    'search': [
        {
            'type': 'input',
            'name': 'query',
            'message': 'Type in the search query: '
        }
    ],

    'after_sign_in_questions': [
        {
            'type': 'list',
            'name': 'options',
            'message': 'What will you like to do',
            'choices': ['see friend recommendations', 'View your network',
                        'change your preferences', 'My friends', 'Search for people',
                        'your profile', 'Delete account', 'Logout']
        }
    ],

    'main_questions': [
        {
            'type': 'list',
            'name': 'options',
            'message': 'Welcome to Friendify',
            'choices': ['About Us', 'Sign-in/Register', 'Exit']
        }
    ],

    'depth_question': [
        {
            'type': 'list',
            'name': 'options',
            'message': 'How deep do you want your graph to go ',
            'choices': ['See only your friends', 'See your friends and their friends',
                        "See your friends, their friends, and your friends' friends' friends",
                        'Exit']
        }
    ],

    'exit_question': [
        {
            'type': 'list',
            'name': 'quit',
            'message': '',
            'choices': ['Exit']
        }
    ],

    'add_friend_question': [
        {
            'type': 'confirm',
            'name': 'add_friend',
            'message': 'Do you want to add this user as your friend',
        }
    ],

    'are_you_sure': [
        {
            'type': 'confirm',
            'name': 'answer',
            'message': 'Are you sure you want to delete your account',
        }
    ],

    'movie_question': '🍿 select at least one and at most 3 movies that you like',

    'music_question': '🎷 select at least one and at most 3 music categories that you like',

    'game_question': '🎯 select at least one and at most 3 games that you like',

    'food_question': '🍔 select at least one and at most 3 food categories that you like'

}

if sys.platform == 'darwin' or sys.platform == 'linux':

    MESSAGES = {
        'header_message': '⬆️ for up ⬇️ for down 🚀 space to select ⏯ enter to confirm your '
                          'selections ',
        'username_taken': "⛔️ The username has already been take",
        'registered_message': "Congratulations 🎉 you registered your self, now sign in with your "
                              "user id to find some friends 👯‍ ",
        'username_nonexistent': '⛔️ The username you entered is not registered',
        'profiles': 'These are your friend recommendations 👯‍, select one of them to see their '
                    'profile 👨‍💼 or exit 🚪 ',
        'my_friends': 'select one of your friends to see their profile  👨‍💼',
        'choose_friends': '🙅 select the people you want to un-friend 🙅',
        'no_friends': 'You have no friends 😞, click enter to Exit',
        'NoRec': 'Sorry! there are no good recommendations for you 😞 come back later',
        'stop_graph': 'Press ^C (Control + C) to end the graph',
        'short_password': '⛔️ The password you typed is shorter than 6 characters'
    }

else:
    MESSAGES = {
        'header_message': '(use arrow keys to move up and down, space bar to select and deselect,'
                          ' and enter to confirm your selections)',
        'username_taken': "(X) The username has already been take",
        'registered_message': "Congratulations! you registered your self, now sign in with your "
                              "user id to find some friends!",
        'username_nonexistent': '(X) The username you entered is not registered incorrect',
        'profiles': 'These are your friend recommendations, select one of them to see their '
                    'profile or exit',
        'my_friends': 'select one of your friends to see their profile',
        'choose_friends': 'Select the people you want to un-friend: ',
        'no_friends': 'You have no friends :-(, click enter to Exit',
        'NoRec': 'Sorry! there are no good recommendations for you :-( come back later',
        'stop_graph': 'Press CTRL + C to end the graph',
        'short_password': 'The password you typed is shorter than 6 characters'
    }

LOGO = """
   ******************************************************************
   *                                                                *
   *                            Friendify👯‍                         *
   *                                                                *
   ******************************************************************
    """

PROFILEQUESTIONS = [
    {
        'header': 'movies',
        'message': QUESTIONS['movie_question'],
        'options': CATEGORIES['movies']
    },
    {
        'header': 'music',
        'message': QUESTIONS['music_question'],
        'options': CATEGORIES['music']
    },
    {
        'header': 'games',
        'message': QUESTIONS['game_question'],
        'options': CATEGORIES['games']
    },
    {
        'header': 'food',
        'message': QUESTIONS['food_question'],
        'options': CATEGORIES['food']
    }
]


def profile(data: dict) -> str:
    """Return string representation of a profile"""
    string_so_far = f'Username: {data["userID"]} \n \n'
    if 'movies' in data:
        string_so_far += 'Favourite Movie categories: ' + ', '.join(data['movies']) + '\n \n'
    if 'music' in data:
        string_so_far += 'Favourite music categories: ' + ', '.join(data['music']) + '\n \n'
    if 'food' in data:
        string_so_far += 'Favourite food categories: ' + ', '.join(data['food']) + '\n \n'
    if 'games' in data:
        string_so_far += 'Favourite games: ' + ', '.join(data['games']) + '\n \n'
    if 'friends' in data:
        string_so_far += 'Friends: \n' + '\n'.join(data['friends'])

    return string_so_far


def generate_question_with_choices(choices: list[str], message: str) -> list[dict]:
    """Generate a question multiple choice single select"""
    return [
        {
            'type': 'list',
            'name': 'options',
            'message': message,
            'choices': choices
        }
    ]


def generate_question_multi_choice(choices: list[dict], message: str) -> list[dict]:
    """Generate a question multiple choice multiple select"""
    return [
        {
            'type': 'checkbox',
            'name': 'options',
            'message': message,
            'choices': choices
        }
    ]


def print_logo() -> None:
    """print the logo"""
    custom_fig = pyfiglet.figlet_format('Friendify 👯‍')
    print(custom_fig)


def change_depth(answer: object) -> int:
    """change the depth variable to visualize friends until that depth"""
    choices = ['See only your friends', 'See your friends and their friends',
               "See your friends, their friends, and your friends' friends' friends"]

    if answer in choices:
        return choices.index(answer) + 1
    else:
        return -1


PYREBASECONFIG = {
    'apiKey': "AIzaSyDksNZ5vwpXXRIIE43UrwuzQ5vxQixKeZo",
    'authDomain': "friendify-6a10b.firebaseapp.com",
    'projectId': "friendify-6a10b",
    'storageBucket': "friendify-6a10b.appspot.com",
    'messagingSenderId': "866913733149",
    'appId': "1:866913733149:web:144bf6a91b9bf8d13494f4",
    'databaseURL': 'friendify-6a10b.appspot.com'
}

if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['sys',
                          'pyfiglet'],  # the names (strs) of imported modules
        'allowed-io': ['print_logo'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
