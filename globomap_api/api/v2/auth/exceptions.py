
class AuthException(Exception):

    def __init__(self, message):
        super(AuthException, self).__init__(message)

        self.message = message
