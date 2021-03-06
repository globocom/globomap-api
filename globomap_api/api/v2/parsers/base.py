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


search_parser = reqparse.RequestParser()
search_parser.add_argument(
    'page',
    type=int,
    required=False,
    default=1,
    help='Page number'
)
search_parser.add_argument(
    'per_page',
    type=int,
    required=False,
    default=10,
    help='Items number per page'
)
search_parser.add_argument(
    'query',
    type=str,
    required=False,
    default='[[{"field":"name","operator":"LIKE","value":""}]]',
    help='Query'
)
