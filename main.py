import screen

from authenticate import DataHandler

if __name__ == '__main__':

    data_handler = DataHandler()

    current_screen = screen.HomeScreen(data_handler)

    while current_screen is not None:
        current_screen = current_screen.show()
