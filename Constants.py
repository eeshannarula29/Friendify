import pyfiglet

collectionName: str = "data"
keysFile: str = "keys.json"
aboutUs: str = "AboutUs.txt"

QuestionsLimit: int = 3

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
        }
    ],

    'after_sign_in_questions': [
        {
            'type': 'list',
            'name': 'options',
            'message': 'What will you like to do',
            'choices': ['see friend recommendations', 'change your preferences', 'your profile',
                        'Logout']
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

    'movie_question': '🍿 select at most 3 movies that you like',

    'music_question': '🎷 select at most 3 music categories that you like',

    'game_question': '🎯 select at most 3 games that you like',

    'food_question': '🍔 select at most 3 food categories that you like'

}

Messages = {
    'header_message': '⬆️ for up ⬇️ for down 🚀 space to select ⏯ enter to confirm your '
                      'selections ',
    'username_taken': "⛔️ The username has already been take",
    'registered_message': "Congratulations 🎉 you registered your self, now sign in with your "
                          "user id to find some friends 👯‍ ",
    'username_nonexistent': '⛔️ The username you entered is not registered',
    'profiles': 'These are your friend recommendations 👯‍, select one of them to see their '
                'profile 👨‍💼 or exit 🚪 '
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
    if 'friends'in data:
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


def printLogo() -> None:
    custom_fig = pyfiglet.figlet_format('Friendify 👯‍')
    print(custom_fig)
