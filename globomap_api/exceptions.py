"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


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


class GraphTraverseException(Exception):

    def __init__(self, message):
        super(GraphTraverseException, self).__init__(message)

        self.message = message


class ConstructorException(Exception):

    def __init__(self, message):
        super(ConstructorException, self).__init__(message)

        self.message = message


class SearchException(Exception):

    def __init__(self, message):
        super(SearchException, self).__init__(message)

        self.message = message
