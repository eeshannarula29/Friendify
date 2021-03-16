import pyfiglet
import sys

collectionName: str = "data"
keysFile: str = "keys.json"
aboutUs: str = "AboutUs.txt"

QuestionsLimit: int = 3

MinimumSimilarityScore = 2

Depth = 2

DataFile = 'data/Survey.csv'

thankyou_message = "Thank you for using Friendify 🙏 😀"

Categories = {

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

Questions = {

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
            'name': 'userID',
            'message': 'type a username',
        }
    ],

    'sign_in_questions': [
        {
            'type': 'input',
            'name': 'userID',
            'message': 'type your username',
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Type your password'
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

    Messages = {
        'header_message': '⬆️ for up ⬇️ for down 🚀 space to select ⏯ enter to confirm your '
                          'selections ',
        'username_taken': "⛔️ The username has already been take",
        'registered_message': "Congratulations 🎉 you registered your self, now sign in with your "
                              "user id to find some friends 👯‍ ",
        'username_nonexistent': '⛔️ The username you entered is not registered or the password is '
                                'incorrect',
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
    Messages = {
        'header_message': '(use arrow keys to move up and down, space bar to select and deselect,'
                          ' and enter to confirm your selections)',
        'username_taken': "(X) The username has already been take",
        'registered_message': "Congratulations! you registered your self, now sign in with your "
                              "user id to find some friends!",
        'username_nonexistent': '(X) The username you entered is not registered, or the password is'
                                ' incorrect',
        'profiles': 'These are your friend recommendations, select one of them to see their '
                    'profile or exit',
        'my_friends': 'select one of your friends to see their profile',
        'choose_friends': 'Select the people you want to un-friend: ',
        'no_friends': 'You have no friends :-(, click enter to Exit',
        'NoRec': 'Sorry! there are no good recommendations for you :-( come back later',
        'stop_graph': 'Press CTRL + C to end the graph',
        'short_password': 'The password you typed is shorter than 6 characters'
    }

logo = """
   ******************************************************************
   *                                                                *
   *                            Friendify👯‍                         *
   *                                                                *
   ******************************************************************
    """

ProfileQuestions = [
    {
        'header': 'movies',
        'message': Questions['movie_question'],
        'options': Categories['movies']
    },
    {
        'header': 'music',
        'message': Questions['music_question'],
        'options': Categories['music']
    },
    {
        'header': 'games',
        'message': Questions['game_question'],
        'options': Categories['games']
    },
    {
        'header': 'food',
        'message': Questions['food_question'],
        'options': Categories['food']
    }
]


def profile(data) -> str:
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


def generate_question_with_choices(choices: list[str], message: str):
    return [
        {
            'type': 'list',
            'name': 'options',
            'message': message,
            'choices': choices
        }
    ]


def generate_question_multiple_choice(choices: list[dict], message: str):
    return [
        {
            'type': 'checkbox',
            'name': 'options',
            'message': message,
            'choices': choices
        }
    ]


def printLogo() -> None:
    custom_fig = pyfiglet.figlet_format('Friendify 👯‍')
    print(custom_fig)


def change_depth(answer: object) -> int:
    choices = ['See only your friends', 'See your friends and their friends',
               "See your friends, their friends, and your friends' friends' friends"]

    if answer in choices:
        return choices.index(answer) + 1
    else:
        return -1


PyrebaseConfig = {
    'apiKey': "AIzaSyDksNZ5vwpXXRIIE43UrwuzQ5vxQixKeZo",
    'authDomain': "friendify-6a10b.firebaseapp.com",
    'projectId': "friendify-6a10b",
    'storageBucket': "friendify-6a10b.appspot.com",
    'messagingSenderId': "866913733149",
    'appId': "1:866913733149:web:144bf6a91b9bf8d13494f4",
    'databaseURL': 'friendify-6a10b.appspot.com'
}
