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
import logging

from arango import ArangoClient
from arango import exceptions

from globomap_api import exceptions as gmap_exceptions
from globomap_api.errors import AQL_QUERY as aql_err
from globomap_api.errors import COLLECTION as coll_err
from globomap_api.errors import DATABASE as db_err
from globomap_api.errors import EDGE as edge_err
from globomap_api.errors import GRAPH as gph_err
from globomap_api.config import MAX_PER_PAGE
# from flask import current_app as app

LOGGER = logging.getLogger(__name__)


class DB(object):
    """DB"""

    def __init__(self, config):
        self.collection = None
        self.database = None
        self.graph = None
        self.edge = None

        self.config = config
        self._connection()

    def _connection(self):
        self.username = self.config['ARANGO_USERNAME']
        self.password = self.config['ARANGO_PASSWORD']
        self.arango_protocol = self.config['ARANGO_PROTOCOL']
        self.arango_host = self.config['ARANGO_HOST']
        self.arango_port = self.config['ARANGO_PORT']

        self.conn = ArangoClient(
            protocol=self.arango_protocol,
            host=self.arango_host,
            port=self.arango_port
        )

        self.conn_database(self.config['ARANGO_DB'])

    ############
    # DATABASE #
    ############
    def conn_database(self, name=''):
        """Make a connection with a database"""
        self.database = self.conn.db(name,
                                     username=self.username,
                                     password=self.password)

    ############
    def has_database(self, name=''):
        """Return True if there database"""

        try:
            self.database.properties()
        except exceptions.DatabasePropertiesError as err:
            self.conn_database(name)
            LOGGER.error(err)
            return False
        except Exception as err:
            msg = db_err.get(0).format(name, str(err))
            LOGGER.error(msg)
            raise gmap_exceptions.DatabaseException(msg)
        else:
            return True

    def get_database(self, name=''):
        """Return database"""

        if not name:
            name = self.config['ARANGO_DB']

        if self.has_database(name):
            return self.database
        else:
            msg = db_err.get(1228).format(name)
            LOGGER.error(msg)
            raise gmap_exceptions.DatabaseNotExist(msg)

    #######
    # AQL #
    #######
    def validate_aql(self, aql):
        """Validate AQL"""

        try:
            self.database.aql.validate(aql)
        except exceptions.AQLQueryValidateError as err:

            if err.error_code == 1501:
                msg = aql_err.get(1501)
                LOGGER.error(msg)
                raise gmap_exceptions.QueryException(msg)

            else:
                msg = aql_err.get(0).format(err.message)
                LOGGER.error(msg)
                raise gmap_exceptions.QueryException(msg)

        except Exception as err:
            msg = db_err.get(0).format(str(err))
            LOGGER.error(msg)
            raise gmap_exceptions.DatabaseException(msg)

    def execute_aql(self, aql, params):
        """Execute AQL"""

        try:
            cursor = self.database.aql.execute(
                aql,
                bind_vars=params,
                count=True,
                full_count=True,
                batch_size=1,
                ttl=10,
                optimizer_rules=['+all']
            )
            return cursor

        except exceptions.AQLQueryExecuteError as err:

            msg = db_err.get(1).format(err.message)
            LOGGER.error(msg)
            raise gmap_exceptions.DatabaseException(msg)

        except Exception as err:
            msg = db_err.get(1).format(str(err))
            LOGGER.error(msg)
            raise gmap_exceptions.DatabaseException(msg)

    def count_in_document(self, collection, search=[]):
        """Get count from collection"""

        bind_vars = {}
        where = ''

        if search:
            where, bind_vars = self.prepare_search(search)

        bind_vars['@collection'] = collection

        full_query = 'FOR doc IN @@collection {} ' \
            'COLLECT WITH COUNT INTO length RETURN length'.format(where)

        try:
            cursor = self.database.aql.execute(
                full_query,
                bind_vars=bind_vars,
                count=True,
                full_count=True,
                batch_size=1,
                ttl=10,
                optimizer_rules=['+all']
            )
            return cursor

        except exceptions.AQLQueryExecuteError as err:

            msg = db_err.get(1).format(err.message)
            LOGGER.error(msg)
            raise gmap_exceptions.DatabaseException(msg)

        except Exception as err:
            msg = db_err.get(1).format(str(err))
            LOGGER.error(msg)
            raise gmap_exceptions.DatabaseException(msg)

    def search_in_collection(self, collection, search, page=1, per_page=10):
        """Search Document"""
        try:

            offset = (page - 1) * per_page
            per_page = per_page if per_page <= MAX_PER_PAGE else MAX_PER_PAGE

            where, bind_vars = self.prepare_search(search)

            bind_vars['@collection'] = collection
            bind_vars['offset'] = offset
            bind_vars['count'] = per_page

            full_query = 'FOR doc IN @@collection {} ' \
                'LIMIT @offset, @count RETURN doc'.format(where)

            LOGGER.debug('Full Query: %s' % full_query)
            cursor = self.database.aql.execute(
                full_query,
                bind_vars=bind_vars,
                count=True,
                full_count=True,
                batch_size=1,
                ttl=10,
                optimizer_rules=['+all']
            )
            return cursor

        except exceptions.AQLQueryExecuteError as err:

            if err.error_code == 1203:
                msg = db_err.get(1203).format(collection)
                LOGGER.error(msg)
                raise gmap_exceptions.CollectionNotExist(msg)

            else:
                msg = db_err.get(1).format(err.message)
                LOGGER.error(msg)
                raise gmap_exceptions.DatabaseException(msg)

        except Exception as err:
            msg = db_err.get(1).format(str(err))
            LOGGER.error(msg)
            raise gmap_exceptions.DatabaseException(msg)

    def search_in_collections(self, collections, search, page=1, per_page=10):
        """Search Document"""
        try:
            offset = (page - 1) * per_page
            per_page = per_page if per_page <= MAX_PER_PAGE else MAX_PER_PAGE
            union = ['a','b','c','e','f','g','h','i','j','k','l','m']
            search_name = search[0]
            partial_query = []

            for index_name, name in enumerate(search_name):
                where, bind_vars = self.prepare_search([[name]])
                bind_vars['offset'] = offset
                bind_vars['count'] = per_page

                queries = []
                for index_coll, collection in enumerate(collections):
                    idx = '@cl_{}'.format(index_coll)
                    bind_vars[idx] = collection
                    query = 'FOR doc IN @{} {} RETURN doc'.format(idx, where)
                    queries.append(query)

                colls = '({})'.format(','.join(queries))
                if len(queries) > 1:
                    colls = 'UNION{}'.format(colls)

                union_item = union[index_name]
                partial_query.append('FOR {} IN {} ' \
                    'SORT {}.name LIMIT @offset, @count RETURN {}'.format(
                        union_item,
                        colls,
                        union_item,
                        union_item
                    )
                )

            if len(partial_query) > 1:
                full_query = 'FOR full IN UNION({}) RETURN full'.format(','.join(partial_query))
            else:
                full_query = partial_query[0]

            LOGGER.debug('Full Query: %s' % full_query)

            cursor = self.database.aql.execute(
                full_query,
                bind_vars=bind_vars,
                count=True,
                full_count=True,
                ttl=10,
                optimizer_rules=['+all']
            )
            return cursor

        except exceptions.AQLQueryExecuteError as err:

            if err.error_code == 1203:
                msg = db_err.get(1203).format(collection)
                LOGGER.error(msg)
                raise gmap_exceptions.CollectionNotExist(msg)

            else:
                msg = db_err.get(1).format(err.message)
                LOGGER.error(msg)
                raise gmap_exceptions.DatabaseException(msg)

        except Exception as err:
            msg = db_err.get(1).format(str(err))
            LOGGER.error(msg)
            raise gmap_exceptions.DatabaseException(msg)

    def prepare_search(self, search):
        index = 0
        bind_vars = {}
        filters = []
        where = ''
        if search:
            for items in search:
                where_item = []
                for item in items:
                    if item['field'] and item['value']:
                        field_array = item['field'].split('.')
                        concat_field = 'doc'
                        for field in field_array:
                            idx = 'index_{}'.format(index)
                            bind_vars[idx] = field
                            concat_field += '.@{}'.format(idx)
                            index += 1

                        if item['operator'] == 'LIKE':
                            where_field = 'CONTAINS(LOWER({}), LOWER(\'{}\'))'.format(
                                concat_field, item['value'])
                            # Example 'doc.@1.@2 LIKE '%value%'
                        elif item['operator'] == 'IN':
                            where_field = '\'{}\' {} {}'.format(
                                item['value'], item['operator'], concat_field)
                            # Example 'value' IN 'doc.@1.@2
                        elif item['operator'] == 'NOTIN':
                            where_field = '\'{}\' NOT IN {}'.format(
                                item['value'], concat_field)
                            # Example 'value' NOT IN 'doc.@1.@2
                        elif item['operator'] == 'REGEXP':
                            where_field = 'LOWER({}) =~ LOWER(CONCAT(\'{}\', \'{}\'))'.format(
                                concat_field, item['comparison'], item['value'])
                            # Example 'doc.@1.@2 =~ '(?!^)value'
                        else:
                            where_field = 'LOWER({}) {} LOWER(\'{}\')'.format(
                                concat_field, item['operator'], item['value'])
                            # Example doc.@1.@2 == 'value'

                        where_item.append(where_field)

                if where_item:
                    filters.append(' AND '.join(where_item))
            if filters:
                where = 'FILTER ' + ' OR '.join(filters)

        return where, bind_vars

    def clear_collection(self, collection, search):
        """Clear colection by query"""

        try:
            where, bind_vars = self.prepare_search(search)

            bind_vars['@collection'] = collection

            full_query = 'FOR doc IN @@collection {} ' \
                'REMOVE doc._key in @@collection'.format(where)

            LOGGER.debug('Full Query: %s' % full_query)
            cursor = self.database.aql.execute(
                full_query,
                bind_vars=bind_vars,
                count=True,
                full_count=True,
                batch_size=1,
                ttl=10,
                optimizer_rules=['+all']
            )
            return cursor

        except exceptions.AQLQueryExecuteError as err:

            if err.error_code == 1203:
                msg = db_err.get(1203).format(collection)
                LOGGER.error(msg)
                raise gmap_exceptions.CollectionNotExist(msg)

            else:
                msg = db_err.get(1).format(err.message)
                LOGGER.error(msg)
                raise gmap_exceptions.DatabaseException(msg)

        except Exception as err:
            msg = db_err.get(1).format(str(err))
            LOGGER.error(msg)
            raise gmap_exceptions.DatabaseException(msg)

    ###############
    # COLLECTIONS #
    ###############
    def _has_collection(self, name='', edge=False):
        """Return True if there collection/edge"""

        try:
            collection = self.database.collection(name)
            res = collection.properties().get('edge') is edge
            return res
        except exceptions.CollectionPropertiesError as err:
            LOGGER.error(err)
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
            LOGGER.error(msg)
            raise gmap_exceptions.CollectionNotExist(msg)

    def create_collection(self, name='', edge=False, replication_factor=1):
        """Create Collection"""

        try:
            self.collection = self.database.create_collection(
                name=name, edge=False, replication_factor=replication_factor)
            return self.collection
        except exceptions.CollectionCreateError as err:

            if err.error_code == 1207:
                msg = coll_err.get(1207).format(name)
                LOGGER.error(msg)
                raise gmap_exceptions.CollectionAlreadyExist(msg)
            else:
                msg = coll_err.get(0).format(name, err.message)
                LOGGER.error(msg)
                raise gmap_exceptions.CollectionException(msg)

        except Exception as err:
            msg = coll_err.get(0).format(name, str(err))
            LOGGER.error(msg)
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
                LOGGER.error(msg)
                raise gmap_exceptions.CollectionNotExist(msg)

            else:
                msg = coll_err.get(0).format(name, err.message)
                LOGGER.error(msg)
                raise gmap_exceptions.CollectionException(msg)

        except Exception as err:
            msg = coll_err.get(0).format(name, str(err))
            LOGGER.error(msg)
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
            LOGGER.error(msg)
            raise gmap_exceptions.EdgeNotExist(msg)

    def create_edge(self, name='', replication_factor=1):
        """Create Edge"""

        try:
            self.edge = self.database.create_collection(
                name=name, edge=True, replication_factor=replication_factor)
            return self.edge
        except exceptions.CollectionCreateError as err:

            if err.error_code == 1207:
                msg = edge_err.get(1207).format(name)
                LOGGER.error(msg)
                raise gmap_exceptions.EdgeAlreadyExist(msg)

            else:
                msg = edge_err.get(0).format(name, err.message)
                LOGGER.error(msg)
                raise gmap_exceptions.EdgeException(msg)

        except Exception as err:
            msg = edge_err.get(0).format(name, str(err))
            LOGGER.error(msg)
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
                LOGGER.error(msg)
                raise gmap_exceptions.EdgeNotExist(msg)

            else:
                msg = edge_err.get(0).format(name, err.message)
                LOGGER.error(msg)
                raise gmap_exceptions.EdgeException(msg)

        except Exception as err:
            msg = edge_err.get(0).format(name, str(err))
            LOGGER.error(msg)
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
        except exceptions.GraphPropertiesError as err:
            LOGGER.error(err)
            return False

    def get_graph(self, name=''):
        """Return graph"""

        if self.has_graph(name):
            self.graph = self.database.graph(name)
            return self.graph
        else:
            msg = gph_err.get(1924).format(name)
            LOGGER.error(msg)
            raise gmap_exceptions.GraphNotExist(msg)

    def create_graph(self, name='', edge_definitions=None):
        """Create Graph"""

        try:
            self.graph = self.database.create_graph(name)
        except exceptions.GraphCreateError as err:

            if err.error_code == 1925:
                msg = gph_err.get(1925).format(name, err)
                LOGGER.error(msg)
                raise gmap_exceptions.GraphAlreadyExist(msg)

            else:
                msg = gph_err.get(0).format(name, err.message)
                LOGGER.error(msg)
                raise gmap_exceptions.GraphException(msg)

        except Exception as err:
            msg = gph_err.get(0).format(name, str(err))
            LOGGER.error(msg)
            raise gmap_exceptions.GraphException(msg)
        else:

            if edge_definitions:
                for edge in edge_definitions:
                    try:
                        self.graph.create_edge_definition(
                            edge_collection=edge.get('edge'),
                            from_vertex_collections=edge.get(
                                'from_collections'),
                            to_vertex_collections=edge.get('to_collections')
                        )
                    except Exception as err:
                        self.database.delete_graph(name)
                        msg = gph_err.get(1).format(name)
                        LOGGER.error(msg)
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
                LOGGER.error(msg)
                raise gmap_exceptions.GraphNotExist(msg)

            else:
                msg = gph_err.get(0).format(name, err.message)
                LOGGER.error(msg)
                raise gmap_exceptions.GraphException(msg)

        except Exception as err:
            msg = gph_err.get(0).format(name, str(err))
            LOGGER.error(msg)
            raise gmap_exceptions.GraphException(msg)
