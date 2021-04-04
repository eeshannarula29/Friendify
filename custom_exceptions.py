"""The file contains all the custom exceptions used by the app"""


class UserExitsError(Exception):
    """ custom Exception for when a person is trying
    to register with already existing user id.
    """

    def __str__(self) -> str:
        return "can not register with existing user_id"


class UserDoesNotExistsError(Exception):
    """ custom Exception for when a person is trying
    to sign in with non existing user id.
    """

    def __str__(self) -> str:
        return "can not sign in with non existing user_id"


class DataDidNotLoadError(Exception):
    """ custom Exception for when the data does not load
    """

    def __str__(self) -> str:
        return "data did not load"


class DataDidNotUploadError(Exception):
    """ custom Exception for when the data does not load
    """

    def __str__(self) -> str:
        return "data did not upload"


class RegistrationError(Exception):
    """ custom Exception for when a person is trying
    to register but error occurs
    """

    def __str__(self) -> str:
        return "Not able to register or add new data to the collection"


class PrintingQuestionError(Exception):
    """ custom Exception for when there is an error while
    asking questions with PyInquirer or cutie
    """

    def __str__(self) -> str:
        return "Error while asking questions with PyInquirer or cutie"


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
