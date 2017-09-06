"""
   Copyright 2017 Globo.com

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
import os

from arango import ArangoClient
from arango import exceptions
from arango.aql import AQL
from flask import current_app as app

from globomap_api import exceptions as gmap_exceptions
from globomap_api.errors import COLLECTION as coll_err
from globomap_api.errors import DATABASE as db_err
from globomap_api.errors import EDGE as edge_err
from globomap_api.errors import GRAPH as gph_err


class DB(object):

    """DB"""

    collection = None
    database = None
    graph = None
    conn = None
    edge = None

    def __init__(self):

        self._connection()

    def _connection(self):

        self.username = app.config['ARANGO_USERNAME']
        self.password = app.config['ARANGO_PASSWORD']
        self.arango_protocol = app.config['ARANGO_PROTOCOL']
        self.arango_host = app.config['ARANGO_HOST']
        self.arango_port = app.config['ARANGO_PORT']

        self._conn = ArangoClient(
            protocol=self.arango_protocol,
            host=self.arango_host,
            port=self.arango_port,
            username=self.username,
            password=self.password,
            enable_logging=True
        )

    ############
    # DATABASE #
    ############
    def has_database(self, name=''):
        """Return True if there database"""

        try:
            database = self._conn.database(name)
            database.properties()
        except exceptions.DatabasePropertiesError:
            return False
        else:
            return True

    def get_database(self, name=''):
        """Return database"""

        if not name:
            name = app.config['ARANGO_DB']

        if self.has_database(name):
            self.database = self._conn.database(name)
            return self.database
        else:
            msg = db_err.get(1228).format(name)
            raise gmap_exceptions.DatabaseNotExist(msg)

    def create_database(self, name=''):
        """Create DB"""

        try:
            self.database = self._conn.create_database(name)
            return self.database
        except exceptions.DatabaseCreateError as err:

            if err.error_code == 1207:
                msg = db_err.get(1207).format(name)
                raise gmap_exceptions.DatabaseAlreadyExist(msg)
            else:
                msg = db_err.get(0).format(name, err.message)
                raise gmap_exceptions.DatabaseException(msg)

        except Exception as err:
            msg = db_err.get(0).format(name, err.message)
            raise gmap_exceptions.DatabaseException(msg)

    def delete_database(self, name=''):
        """Delete DB"""

        try:
            self._conn.delete_database(name)
            self.database = None
            return True
        except exceptions.DatabaseDeleteError as err:

            if err.error_code == 1228:
                msg = db_err.get(1228).format(name)
                raise gmap_exceptions.DatabaseNotExist(msg)

            else:
                msg = db_err.get(0).format(name, err.message)
                raise gmap_exceptions.DatabaseException(msg)

        except Exception as err:
            msg = db_err.get(0).format(name, err.message)
            raise gmap_exceptions.DatabaseException(msg)

    def search_in_database(self, collection, field, value, offset=0, count=10):
        """Search Document"""
        # TODO: To use a better way to search
        try:
            if field and value:
                where = 'FILTER LOWER(doc.`{}`) like "%{}%"'.format(
                    field, value.lower())
            else:
                where = ''

            cursor = self.database.aql.execute('''
                FOR doc IN {} {} LIMIT {}, {} RETURN doc'''.format(
                collection, where, offset, count),
                count=True,
                batch_size=1,
                ttl=10,
                optimizer_rules=['+all']
            )
            return cursor
        except Exception as err:
            msg = db_err.get(1).format(err.message)
            raise gmap_exceptions.DatabaseException(msg)

    ###############
    # COLLECTIONS #
    ###############
    def _has_collection(self, name='', edge=False):
        """Return True if there collection/edge"""

        try:
            collection = self.database.collection(name)
            res = collection.properties().get('edge') is edge
            # import pdb; pdb.Pdb().set_trace()
            # if res is edge:
            return res
        except exceptions.CollectionPropertiesError:
            return False

    def has_collection(self, name=''):
        """Return True if there collection"""
        return self._has_collection(name, False)

    def get_collection(self, name=''):
        """Return Collection"""

        if self.has_collection(name):
            self.collection = self.database.collection(name)
            return self.collection
        else:
            msg = coll_err.get(1228).format(name)
            raise gmap_exceptions.CollectionNotExist(msg)

    def create_collection(self, name='', edge=False):
        """Create Collection"""

        try:
            self.collection = self.database.create_collection(
                name=name, edge=False)
            return self.collection
        except exceptions.CollectionCreateError as err:

            if err.error_code == 1207:
                msg = coll_err.get(1207).format(name)
                raise gmap_exceptions.CollectionAlreadyExist(msg)
            else:
                msg = coll_err.get(0).format(name, err.message)
                raise gmap_exceptions.CollectionException(msg)

        except Exception as err:
            msg = coll_err.get(0).format(name, err.message)
            raise gmap_exceptions.CollectionException(msg)

        else:
            return True

    def delete_collection(self, name=''):
        """Delete Collection """

        try:
            self.database.delete_collection(name=name)
            self.collection = None
            return True
        except exceptions.CollectionDeleteError as err:

            if err.error_code == 1203:
                msg = coll_err.get(1228).format(name)
                raise gmap_exceptions.CollectionNotExist(msg)

            else:
                msg = coll_err.get(0).format(name, err.message)
                raise gmap_exceptions.CollectionException(msg)

        except Exception as err:
            msg = coll_err.get(0).format(name, err.message)
            raise gmap_exceptions.CollectionException(msg)

    def has_edge(self, name=''):
        """Return True if there edge"""
        return self._has_collection(name, True)

    def get_edge(self, name='', ):
        """Return Edge"""

        if self.has_edge(name):
            self.edge = self.database.collection(name)
            return self.edge
        else:
            msg = edge_err.get(1228).format(name)
            raise gmap_exceptions.EdgeNotExist(msg)

    def create_edge(self, name=''):
        """Create Edge"""

        try:
            self.edge = self.database.create_collection(
                name=name, edge=True)
            return self.edge
        except exceptions.CollectionCreateError as err:

            if err.error_code == 1207:
                msg = edge_err.get(1207).format(name)
                raise gmap_exceptions.EdgeAlreadyExist(msg)

            else:
                msg = edge_err.get(0).format(name, err.message)
                raise gmap_exceptions.EdgeException(msg)

        except Exception as err:
            msg = edge_err.get(0).format(name, err.message)
            raise gmap_exceptions.EdgeException(msg)

    def delete_edge(self, name=''):
        """Delete Edge """

        try:
            self.database.delete_collection(name=name)
            self.edge = None
            return True
        except exceptions.CollectionDeleteError as err:

            if err.error_code == 1203:
                msg = edge_err.get(1228).format(name)
                raise gmap_exceptions.EdgeNotExist(msg)

            else:
                msg = edge_err.get(0).format(name, err.message)
                raise gmap_exceptions.EdgeException(msg)

        except Exception as err:
            msg = edge_err.get(0).format(name, err.message)
            raise gmap_exceptions.EdgeException(msg)
        else:
            return True

    ##########
    # GRAPHS #
    ##########
    def has_graph(self, name=''):
        """Return True if there graph"""

        try:
            graph = self.database.graph(name)
            graph.properties()
            return True
        except exceptions.GraphPropertiesError:
            return False

    def get_graph(self, name=''):
        """Return graph"""

        if self.has_graph(name):
            self.graph = self.database.graph(name)
            return self.graph
        else:
            msg = gph_err.get(1924).format(name)
            raise gmap_exceptions.GraphNotExist(msg)

    def create_graph(self, name='', edge_definitions=None):
        """Create Graph"""

        try:
            self.graph = self.database.create_graph(name)
        except exceptions.GraphCreateError as err:

            if err.error_code == 1925:
                msg = gph_err.get(1925).format(name, err)
                raise gmap_exceptions.GraphAlreadyExist(msg)

            else:
                msg = gph_err.get(0).format(name, err.message)
                raise gmap_exceptions.GraphException(msg)

        except Exception as err:
            msg = gph_err.get(0).format(name, err.message)
            raise gmap_exceptions.GraphException(msg)
        else:

            if edge_definitions:
                for edge in edge_definitions:
                    try:
                        self.graph.create_edge_definition(
                            name=edge.get('edge'),
                            from_collections=edge.get('from_collections'),
                            to_collections=edge.get('to_collections')
                        )
                    except Exception as err:
                        self.database.delete_graph(name)
                        msg = gph_err.get(1).format(name)
                        raise gmap_exceptions.GraphException(msg)

        return self.graph

    def delete_graph(self, name=''):
        """Delete Graph"""

        try:
            self.database.delete_graph(name)
            return True
        except exceptions.GraphDeleteError as err:

            if err.error_code == 1924:
                msg = gph_err.get(1924).format(name)
                raise gmap_exceptions.GraphNotExist(msg)

            else:
                msg = gph_err.get(0).format(name, err.message)
                raise gmap_exceptions.GraphException(msg)

        except Exception as err:
            msg = gph_err.get(0).format(name, err.message)
            raise gmap_exceptions.GraphException(msg)
