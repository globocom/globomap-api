class DatabaseNotExist(Exception):

    def __init__(self, message):
        super(DatabaseNotExist, self).__init__(message)

        self.message = message


class DatabaseAlreadyExist(Exception):

    def __init__(self, message):
        super(DatabaseAlreadyExist, self).__init__(message)

        self.message = message


class DatabaseException(Exception):

    def __init__(self, message):
        super(DatabaseException, self).__init__(message)

        self.message = message


class CollectionNotExist(Exception):

    def __init__(self, message):
        super(CollectionNotExist, self).__init__(message)

        self.message = message


class CollectionAlreadyExist(Exception):

    def __init__(self, message):
        super(CollectionAlreadyExist, self).__init__(message)

        self.message = message


class CollectionException(Exception):

    def __init__(self, message):
        super(CollectionException, self).__init__(message)

        self.message = message


class EdgeNotExist(Exception):

    def __init__(self, message):
        super(EdgeNotExist, self).__init__(message)

        self.message = message


class EdgeAlreadyExist(Exception):

    def __init__(self, message):
        super(EdgeAlreadyExist, self).__init__(message)

        self.message = message


class EdgeException(Exception):

    def __init__(self, message):
        super(EdgeException, self).__init__(message)

        self.message = message


class DocumentNotExist(Exception):

    def __init__(self, message):
        super(DocumentNotExist, self).__init__(message)

        self.message = message


class DocumentAlreadyExist(Exception):

    def __init__(self, message):
        super(DocumentAlreadyExist, self).__init__(message)

        self.message = message


class DocumentException(Exception):

    def __init__(self, message):
        super(DocumentException, self).__init__(message)

        self.message = message


class GraphNotExist(Exception):

    def __init__(self, message):
        super(GraphNotExist, self).__init__(message)

        self.message = message


class GraphAlreadyExist(Exception):

    def __init__(self, message):
        super(GraphAlreadyExist, self).__init__(message)

        self.message = message


class GraphException(Exception):

    def __init__(self, message):
        super(GraphException, self).__init__(message)

        self.message = message


class ConstructorException(Exception):

    def __init__(self, message):
        super(ConstructorException, self).__init__(message)

        self.message = message
