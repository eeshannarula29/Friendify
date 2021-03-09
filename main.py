import Screen

from authenticate import DataHandler

if __name__ == '__main__':

    data_handler = DataHandler()

    current_screen = Screen.HomeScreen(data_handler)

    while current_screen is not None:
        current_screen = current_screen.show()
