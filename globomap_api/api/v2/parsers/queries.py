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
from flask_restplus import reqparse

post_query_parser = reqparse.RequestParser()
post_query_parser.add_argument(
    'data',
    type=str,
    required=True,
    help='Collection',
    location='json'
)

put_query_parser = reqparse.RequestParser()
put_query_parser.add_argument(
    'data',
    type=str,
    required=True,
    help='Document',
    location='json'
)

search_query_parser = reqparse.RequestParser()
search_query_parser.add_argument(
    'page',
    type=int,
    required=False,
    default=1,
    help='Page number'
)
search_query_parser.add_argument(
    'per_page',
    type=int,
    required=False,
    default=10,
    help='Items number per page'
)
# TODO
# search_query_parser.add_argument(
#     'query',
#     type=str,
#     required=False,
#     default='[[{"field":"name","operator":"LIKE","value":""}]]',
#     help='Query'
# )

execute_query_parser = reqparse.RequestParser()
execute_query_parser.add_argument(
    'variable',
    type=str,
    required=True,
    help='Variable'
)
